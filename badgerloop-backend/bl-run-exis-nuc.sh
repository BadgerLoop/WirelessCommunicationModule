docker run -d --restart=on-failure -e TCP_PORTS=8000 -p 9000:8000 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-01 -t exis-node
docker run -d --restart=on-failure -e TCP_PORTS=8000 -p 9001:8000 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-02 -t exis-node
