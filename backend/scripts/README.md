# Scripts
This is your one stop shop for all things badgerloop backend and WCM


###Scripts

	./run-db.sh

Runs Mongodb in a docker container - nuc 2

	./exis-node-build.sh

Builds the exis node docker container from the /exis-node directory - nuc 1 + nuc 2

	./exis-node-run.sh {number of nodes you want to run}

Runs 2 instances of the exis node docker container exposed on ports 9000 + - nuc 1 + nuc 2

	./stop-all.sh

Stops all running docker containers

	./start-ha.sh {nuc number}

Starts haproxy and keepalived according to the configs in the /configs directory
Haproxy directs network requests to and from the exis-nodes, dashboard and logger
Keepalived enables host failover on the configured virtual ip address 




