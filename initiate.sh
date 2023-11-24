#!/bin/bash

python3 cryptoconfig.py 
python3 configuration.py 
python3 compose.py 

./bin/cryptogen generate --config=./organizations/cryptogen/crypto-config.yaml --output=organizations
export FABRIC_CFG_PATH=${PWD}/configtx
./bin/configtxgen -profile TwoOrgsOrdererGenesis -channelID system-channel -outputBlock ./system-genesis-block/genesis.block
./bin/configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel1.tx -channelID channel1



# docker-compose --project-name cli -f ./docker/docker-compose-cli.yaml up -d 
# docker-compose --project-name orderer -f ./docker/docker-compose-orderer.example.com.yaml up -d 
# docker-compose --project-name orderer2 -f ./docker/docker-compose-orderer2.example.com.yaml up -d 
# docker-compose --project-name orderer3 -f ./docker/docker-compose-orderer3.example.com.yaml up -d 
# docker-compose --project-name peer0org1 -f ./docker/docker-compose-peer0.org1.example.com.yaml up -d 
# docker-compose --project-name peer1org1 -f ./docker/docker-compose-peer1.org1.example.com.yaml up -d 
# docker-compose --project-name peer0org2 -f ./docker/docker-compose-peer0.org2.example.com.yaml up -d 
# docker-compose --project-name peer1org2 -f ./docker/docker-compose-peer1.org2.example.com.yaml up -d 
# docker-compose --project-name peer0org3 -f ./docker/docker-compose-peer0.org3.example.com.yaml up -d 
# docker-compose --project-name peer1org3 -f ./docker/docker-compose-peer1.org3.example.com.yaml up -d 
# docker-compose -f ./docker/docker-compose.yaml up -d