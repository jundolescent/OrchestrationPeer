import os
import yaml

with open('./NodeDeployment.yaml') as f:
    deployment = yaml.load(f, Loader=yaml.FullLoader)

n_orderer = deployment['Deployment']['orderer']
n_org = deployment['Deployment']['organization']
n_peer = deployment['Deployment']['peer']
n_server = deployment['Deployment']['server']
chaincode = deployment['Deployment']['chaincode']

os.system('docker exec cli peer lifecycle chaincode package {}.tar.gz \
          --lang golang \
          --path /opt/gopath/src/github.com/hyperledger/fabric/peer/caliper-benchmarks/src/fabric/samples/{}/go \
          --label {}'.format(chaincode, chaincode, chaincode))

#install chaincode
os.system('docker exec cli peer lifecycle chaincode install {}.tar.gz'.format(chaincode))
os.system('docker exec \
          -e CORE_PEER_ADDRESS=peer1.org1.example.com:8101 \
          -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer1.org1.example.com/tls/ca.crt \
          cli peer lifecycle chaincode install {}.tar.gz'.format(chaincode))

for org in range(2, n_org + 1):
    for peer in range(0, n_peer):
        peer_port = 8000 + org * 100 ## 8100, 8200. 8300
        peer_port = peer_port + peer
        os.system('docker exec \
                  -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/users/Admin@org{}.example.com/msp \
                  -e CORE_PEER_ADDRESS=peer{}.org{}.example.com:{} \
                  -e CORE_PEER_LOCALMSPID="Org{}MSP" \
                  -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/peers/peer{}.org{}.example.com/tls/ca.crt \
                  cli peer lifecycle chaincode install {}.tar.gz'.format(org, org, peer, org, peer_port, org, org, peer, org, chaincode))
        

os.system('docker exec cli peer lifecycle chaincode queryinstalled')
result = os.popen('docker exec cli peer lifecycle chaincode queryinstalled | grep {} | cut -d ":" -f 2,3 | cut -d "," -f 1'.format(chaincode)).read()


#commit chaincode

os.system('docker exec cli peer lifecycle chaincode approveformyorg \
          --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem \
          --channelID channel1 \
          --name {} --version 1 --sequence 1 --waitForEvent --package-id {}'.format(chaincode, result))

for org in range(2, n_org + 1):
    peer_port = 8000 + org * 100 ## 8100, 8200. 8300
    os.system('docker exec \
              -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/users/Admin@org{}.example.com/msp \
              -e CORE_PEER_ADDRESS=peer0.org{}.example.com:{} \
              -e CORE_PEER_LOCALMSPID="Org{}MSP" \
              -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/peers/peer0.org{}.example.com/tls/ca.crt \
              cli peer lifecycle chaincode approveformyorg \
              --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem \
              --channelID channel1 --name {} --version 1 --sequence 1 --waitForEvent --package-id {}'.format(org, org, org, peer_port, org, org, org, chaincode, result))
    

#commit
head_commit = 'docker exec cli peer lifecycle chaincode commit \
          -o orderer.example.com:7050 \
          --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem '
tail_commit = '--channelID channel1 --name {} --version 1 --sequence 1'.format(chaincode)
temp = '--peerAddresses peer0.org1.example.com:8100 \
          --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt '

for org in range(2, n_org + 1):
    peer_port = 8000 + org * 100 ## 8100, 8200. 8300
    temp = temp + '--peerAddresses peer0.org{}.example.com:{} \
          --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/peers/peer0.org{}.example.com/tls/ca.crt '.format(org, peer_port, org, org)
    
commit_sentence = head_commit + temp + tail_commit
    
os.system(commit_sentence)

#querycommitted
os.system('docker exec cli peer lifecycle chaincode querycommitted --channelID channel1 --name {}'.format(chaincode))

# docker exec cli peer lifecycle chaincode package fabcar.tar.gz --lang golang --path /opt/gopath/src/github.com/hyperledger/fabric/peer/caliper-benchmarks/src/fabric/samples/fabcar/go --label fabcar

# docker exec cli peer lifecycle chaincode install fabcar.tar.gz

# docker exec -e CORE_PEER_ADDRESS=peer1.org1.example.com:17051 -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer1.org1.example.com/tls/ca.crt cli peer lifecycle chaincode install fabcar.tar.gz

# docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp -e CORE_PEER_ADDRESS=peer0.org2.example.com:9051 -e CORE_PEER_LOCALMSPID="Org2MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt cli peer lifecycle chaincode install fabcar.tar.gz

# docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp -e CORE_PEER_ADDRESS=peer1.org2.example.com:19051 -e CORE_PEER_LOCALMSPID="Org2MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt cli peer lifecycle chaincode install fabcar.tar.gz

# docker exec cli peer lifecycle chaincode queryinstalled

# RESULT=$(docker exec cli peer lifecycle chaincode queryinstalled | grep 'fabcar' | cut -d ":" -f 2,3 | cut -d "," -f 1)

# echo $RESULT

# docker exec cli peer lifecycle chaincode approveformyorg --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --channelID channel1 --name fabcar --version 1 --sequence 1 --waitForEvent --package-id $RESULT

# docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp -e CORE_PEER_ADDRESS=peer0.org2.example.com:9051 -e CORE_PEER_LOCALMSPID="Org2MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt cli peer lifecycle chaincode approveformyorg --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --channelID channel1 --name fabcar --version 1 --sequence 1 --waitForEvent --package-id $RESULT

# docker exec cli peer lifecycle chaincode commit -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt --channelID channel1 --name fabcar --version 1 --sequence 1

# docker exec cli peer lifecycle chaincode querycommitted --channelID channel1 --name fabcar