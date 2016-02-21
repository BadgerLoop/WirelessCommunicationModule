eval $(docker-machine env bl-backend)
echo "stopping and removing all containers"
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)