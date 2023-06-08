argparse 'v/volumes' 'n#number' 'k/network' -- $argv; or exit 1
if not set -q _flag_n
  echo 'Specify runner number'
  exit 1
end

set -l n $_flag_n

docker rm -f gitlab-runner-$n
if set -q _flag_v 
  docker volume rm gitlab-runner-config-$n
end

if set -q _flag_k
  docker network rm gitlab-runner-network
end
