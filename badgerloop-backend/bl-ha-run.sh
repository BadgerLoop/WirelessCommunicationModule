eval $(docker-machine env bl-backend)
echo "starting exis node containers"
docker build -t exis-node ./node
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-01 -t exis-node 
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-02 -t exis-node 
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-03 -t exis-node
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-04 -t exis-node
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e VIRTUAL_HOST_WEIGHT=1 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-05 -t exis-node
echo "starting ha proxy"
docker run -d --restart=on-failure -p 80:80 -p 8000:8000 --name=haproxy --link exis-node-01:exis-node-01 --link exis-node-02:exis-node-02 --link exis-node-03:exis-node-03 --link exis-node-04:exis-node-04 --link exis-node-05:exis-node-05 -e STATS_AUTH="auth:auth" -e BALANCE="first" -e TIMEOUT="connect 10, client 50000, server 50000" -e STATS_PORT=1936 -p 1936:1936 tutum/haproxy