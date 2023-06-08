#!/usr/bin/env fish

argparse 'c/in-container' 'v/verbose' -- $argv; or return
if set -q _flag_verbose
  set verbose $_flag_verbose
end

function vecho
  if set -q verbose
    echo (echo $argv | string split ' ')
  end
end

set -l container_name gitlab
set -q GITLAB_HOSTNAME; or set GITLAB_HOSTNAME gitlab.local
set -q SECRET_MANAGER_URL; or set SECRET_MANAGER_URL http://secretmanager/
set endpoint $GITLAB_HOSTNAME

function encode_json_item
  set -f splitted (string split --max 1 '=' $argv[1])
  set -f key $splitted[1]
  set -f value $splitted[2]
  if not contains $value true false null; and string match -qr '\D' $value
    set -f value "\"$value\""
  end
  echo -n "\"$key\": $value"
end

function build_json
  echo -n "{$(encode_json_item "$argv[1]")"
  for arg in $argv[2..]
    echo -n ", $(encode_json_item "$arg")"
  end
  echo -n '}'
end

if set -q _flag_in_container
  for variant in config logs data
    set -l name gitlab-data-$variant
    if not podman volume exists $name
      echo "Create volume $name"
      podman volume create $name
    else
      echo "Volume $name exists"
    end
  end

  if not podman container exists $container_name
    podman run --detach --restart=unless-stopped \
     --publish 2080:80 --publish 2022:22 \
     --name $container_name --hostname=$HOSTNAME \
     --volume gitlab-data-config:/etc/gitlab \
     --volume gitlab-data-logs:/var/log/gitlab \
     --volume gitlab-data-data:/var/opt/gitlab \
     --detach \
     --shm-size=256m \
     docker.io/gitlab/gitlab-ce

    echo -n "Waiting $container_name start"
    while not curl -f localhost:2080/ &> /dev/null
      echo -n '.'
      sleep 2
    end
    echo

    echo "$container_name started"
    set -l password_line (podman exec $container_name grep 'Password: ' /etc/gitlab/initial_root_password)
    set -l password (echo $password_line | awk '{ print $2 }')
    echo "Root password: '$password'"

  else if podman container ps -f name="^$container_name\$" > /dev/null
    echo "Start $container_name"
    podman container start $container_name

    echo -n "Waiting $container_name start"
    while not curl -f localhost:2080/ &> /dev/null
      echo -n '.'
      sleep 2
    end
    echo

    echo "$container_name started"
  else
    echo "Container $container_name exists and running"
  end

  set endpoint localhost:2080
  set GITLAB_HOSTNAME localhost
  set GITLAB_SSH localhost
  set GITLAB_SSH_PORT 2022
else
  set GITLAB_SSH (string replace -r "https?://" "" $GITLAB_HOSTNAME)
end

set api $endpoint/api/v4
set repo_path ucuhunter

function curl_opts
  if test (count $argv) -eq 0
    set -f method "GET"
  else
    set -f method $argv[1]
  end
  string trim -- -L --silent -X $method --fail-with-body -H "PRIVATE-TOKEN: $private_token"
  if not set -q verbose
    string trim -- -o /dev/null
  else
    string trim -- -v
  end
  if contains $method POST PUT
    string trim -- -H 'Content-Type: application/json'
  end
end

function disable_sign_up
  echo "Update sign up settings"
  curl (curl_opts PUT) \
    --data "$(build_json signup_enabled=false)" \
    $api/application/settings/
  vecho
end

function setup_repository
  if curl -o /dev/null (curl_opts) "$api/projects/root%2F$repo_path"
    echo 'Repository exists'
  end
  set -l data $(build_json \
    path=$repo_path \
    forking_access_level=enabled \
    lfs_enabled=false \
    auto_devops_enabled=false \
    merge_requests_access_level=private \
    pages_access_level=disabled \
    releases_access_level=private \
    snippets_enabled=false \
    emails_disabled=true \
    analytics_access_level=disabled \
    container_registry_access_level=disabled \
    shared_runners_enabled=true \
    public_builds=true \
    visibility=public)
  echo "Create project with $data"
  curl (curl_opts POST) \
    --data "$data" \
    $api/projects/
  vecho
end


function setup_ci_variables
  echo "Update instance CI variables"
  curl (curl_opts POST) \
    --data "$(build_json key=SHRON_URL value=$SECRET_MANAGER_URL)" \
    $api/admin/ci/variables
  vecho
  echo "Update project CI variables"
  curl (curl_opts POST) \
    --data "$(build_json \
      key=SHRON_PASSWORD \
      value=real-password \
      masked=true)" \
    $api/projects/root%2F$repo_path/variables
  vecho
end

function setup_ssh
  set -l ssh_key (ssh-add -L)
  if test -z ssh_key
    echo 'Configure ssh agent, please'
    return 1
  end

  echo "Use $ssh_key"

  set -l data (build_json title=setup key=$ssh_key)
  curl (curl_opts POST) \
    --data $data \
    $api/user/keys
  vecho
end

function upload_repo
  set -l path (mktemp -d --tmpdir tecret-repo.XXX)
  find ./repo -type f -exec cp -t $path {} +
  set -l old_pwd (pwd)
  if not set -q GITLAB_SSH_PORT
    set GITLAB_SSH_PORT 22
  end
  echo "
  Host gitlab
  Hostname $GITLAB_SSH
  User root
  Port $GITLAB_SSH_PORT
  UserKnownHostsFile $old_pwd/knownhosts
  " > ./sshconfig
  cd $path
  git init
  git add .
  git commit -m 'initial commit'
  git remote add origin git@gitlab:root/$repo_path.git
  GIT_SSH_COMMAND="ssh -F $old_pwd/sshconfig" git push -u -f origin master
  cd $old_pwd
  rm -rf $path knownhosts sshconfig
  echo "Unprotect master branch in 2 secs..."
  sleep 2
  curl (curl_opts DELETE) \
    $api/projects/root%2F$repo_path/protected_branches/master
  vecho
end

read -gsP "Enter private token: " private_token; or return

disable_sign_up
and setup_repository
and setup_ssh
and setup_ci_variables
and upload_repo
