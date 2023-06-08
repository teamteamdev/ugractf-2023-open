set -l network gitlab-runner-network

if not docker network inspect $network &> /dev/null
  docker network create $network; or exit 2
end

if docker container inspect secretmanager &> /dev/null
  docker stop secretmanager
end

docker build secretmanager -t secretmanager

docker run --restart always -d \
  --name secretmanager \
  --network $network \
  secretmanager
