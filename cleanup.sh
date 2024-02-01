#!/bin/bash

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker images | grep 'dev-peer' | awk '{print $3}' | xargs docker rmi -f
docker volume rm $(docker volume ls -qf dangling=true)

rm -rf ./channel-artifacts
rm -rf ./system-genesis-block
rm -rf ./organizations/peerOrganizations
rm -rf ./organizations/ordererOrganizations
rm -rf ./docker/*
rm -rf ./configtx/configtx.yaml
rm -rf ./ccp-template2.json
