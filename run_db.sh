#!/bin/bash

sudo docker run --detach \
				--name mnist-mariadb \
				--env MARIADB_USER=mnist \
				--env MARIADB_PASSWORD=1234 \
				--env MARIADB_DATABASE=mnistdb \
				--env MARIADB_ROOT_PASSWORD=root  \
				-p 53306:3306 \
				mariadb:latest
