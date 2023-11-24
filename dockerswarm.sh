#!/bin/bash

ip1=$1

docker swarm init --advertise-addr $ip1
echo -e "\n" >> ./hello.sh
docker swarm join-token manager | grep "docker swarm" >> ./hello.sh
docker network create --attachable --driver overlay testnet