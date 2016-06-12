eval $(docker-machine env bl-backend)
echo "starting exis node containers"
docker build -t exis-node ./node
docker build -t haproxy ./haproxy
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-01 -t exis-node 
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-02 -t exis-node 
echo "starting ha proxy"
docker run -d -p 8000:8000 -p 1936:1936 -p 80:80 --name haproxy haproxy