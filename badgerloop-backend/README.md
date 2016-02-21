#Badger Loop HA (High Availability) Backend

The badger loop backend uses an [Exis fabric node](https://github.com/exis-io/node) to store/cache pod data in real time on a local area network.  The following scripts spin up and run a [docker](https://www.docker.com/) instance and runs 3 Exis node containers along with an HAProxy container that routes traffic to the primary healthy Exis node.  If the primary Exis node becomes unhealthy and unable to manage the incoming/outgoing pod data HA proxy elects a new primary node and traffic is immediately routed to that node while the unhealthy Exis node container restarts itself and comes back online (hopefully, this is still in testing).  Data persists in a mongodb instance which is still being "dockerized", configured and added to the init and run scripts.

*Note this backend will be hosted on dedicated machine(s) during the pod runs and is intended to allow us to reliably transfer data from the pod to the Exis node backend(s) and transfer data from the Exis Node Backend to the dashboard with minimal latency and downtime in case of error.    

## Requirements

[docker](https://docs.docker.com/engine/installation/) 

[docker toolbox](https://www.docker.com/products/docker-toolbox)

* Note these must be installed in order to run the scripts properly.  It would also be useful to become familiar with the docker and docker toolbox CLIs

## Running
*Note this has been tested on Mac only and some adjustments need to made in order for it to work for linux.

To initialize the Badger Loop HA backend run:

	./bl-ha-init.sh 

This will start a docker machine instance (Basically a Virtual Machine) called "bl-backend" and start running 3 Exis node containers and an ha proxy container on that docker-machine instance.  

To stop the containers from running run:

	./bl-ha-stop.sh

To run the containers once you have initialized the backend docker machine and stopped the containers run:

	./bl-ha-run.sh

*Note: When everything is done installing/running, you can run 

	docker-machine ls

to view the docker machine instance and local IP address that should allow incoming and outgoing Exis messages (on port 8000 configured currently).  We are working on getting this to be a recognizable virtual host domain name over the local area network such as "xs.badgerloop.backend". That all dashboard instances and pod communications from the WCM can point to.  Also on port 1936 there is a front end for ha proxy that displays the status of the node containers and eventually the mongodb database container.

#Misc

* Please note that this is still a work in progress and the configuration and backend we are using are subject to change.  Significant testing needs to happen in order to determine the validity of this configuration.  Also if you have any questions contact Kyle Grieger (Kgrieger on slack).
