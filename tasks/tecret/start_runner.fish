argparse 'n#number' -- $argv; or exit 1
if not set -q _flag_n
  echo 'Specify runner number'
  exit 1
end

set -l n $_flag_n

set -l network gitlab-runner-network
set -l config gitlab-runner-config-$n

if not docker network inspect $network &> /dev/null
  docker network create $network; or exit 2
end

if not docker volume inspect $config &> /dev/null
  docker volume create $config; or exit 2
end

set -l name "gitlab-runner-$n"
if docker container inspect $name &> /dev/null
  echo "$name already exists, skip"
else
  echo "Starting $name..."
  docker run -d --name $name --restart always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $config:/etc/gitlab-runner \
    --network $network \
    gitlab/gitlab-runner

  echo "Started!"
  echo "Now run 'docker exec -it $name gitlab-runner register' and answer question. Then modify runner configuration to use 'network_mode = gitlab-runner-network'"
  echo "After this run 'docker restart $name'"
end
