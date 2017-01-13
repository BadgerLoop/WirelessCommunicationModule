#!/usr/bin/env bash

echo "Starting $1 Exis node containers"
for ((i=0; i<$(($1 + 0)); i++))
do
	echo "$var"
    docker run -d --restart=on-failure -e TCP_PORTS=8000 -p 900$i:8000 -e EXIS_PERMISSIONS=off -e EXIS_AUTHENTICATION=off --name=exis-node-$(($i+1)) -t exis-node
done
