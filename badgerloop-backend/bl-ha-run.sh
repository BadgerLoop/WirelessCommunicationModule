eval $(docker-machine env bl-backend)
echo "starting exis node containers"
docker build -t exis-node ./node
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-01 -t exis-node 
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-02 -t exis-node 
docker run -d --restart=on-failure -e TCP_PORTS=8000 -e VIRTUAL_HOST="ws://xs.demo.badgerloop.bldashboard" -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-03 -t exis-node
echo "starting ha proxy"
docker run -d --restart=on-failure -p 80:80 -p 8000:8000 --name=haproxy --link exis-node-01:exis-node-01 --link exis-node-02:exis-node-02 --link exis-node-03:exis-node-03 -e STATS_AUTH="auth:auth" -e BALANCE="first" -e STATS_PORT=1936 -p 1936:1936 tutum/haproxy