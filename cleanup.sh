#!/bin/bash

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -qf dangling=true)

rm -rf ./channel-artifacts
rm -rf ./system-genesis-block
rm -rf ./organizations/peerOrganizations
rm -rf ./organizations/ordererOrganizations
rm -rf ./docker/*