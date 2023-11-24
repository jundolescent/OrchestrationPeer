import yaml
import sys
import os

##### the number of orderer, the number of organization #########
##### location of peer node #################
with open('./NodeDeployment.yaml') as f:
    deployment = yaml.load(f, Loader=yaml.FullLoader)

n_orderer = deployment['Deployment']['orderer']
n_org = deployment['Deployment']['organization']
n_peer = deployment['Deployment']['peer']
n_server = deployment['Deployment']['server']

# server_list = []
# extra_hosts = []
# for i in range(0, n_server):
#     server_list.append(deployment['Deployment']['deployment'][i]['configuration'])
#     for j in deployment['Deployment']['deployment'][i]['configuration']:
#         extra_hosts.append('{}.example.com:{}'.format(j,deployment['Deployment']['deployment'][i]['ip']))
server_list = []
extra_hosts = []
total = []
total_hosts = []
for i in range(0, n_server):
    extra_hosts = []
    server_list.append(deployment['Deployment']['deployment'][i]['configuration'])
    for j in deployment['Deployment']['deployment'][i]['configuration']:
        extra_hosts.append('{}.example.com:{}'.format(j,deployment['Deployment']['deployment'][i]['ip']))
        total.append('{}.example.com:{}'.format(j,deployment['Deployment']['deployment'][i]['ip']))
    total_hosts.append(extra_hosts)
#total_hosts = list(set(temp) - set(extra_hosts))
result = []
for j in total_hosts:
    j = list(set(total) - set(j))
    result.append(j)


for index, server in enumerate(server_list):
    volumes = {}
    if index == 0:
        volumes['cli'] = {}
    for node in server:
        volumes['{}.example.com'.format(node)] = {}

    head_dict = {'version': '3.7', 'volumes':volumes,'networks':{'test':{'name':'testnet', 'external':True}}}
    with open('./docker/docker-compose-{}.yaml'.format(index), 'w') as f:
        yaml.dump(head_dict,f,sort_keys=False)



######case1 orderer #########################
for i in range(0,n_orderer):
    if i == 0:
        orderer_name = 'orderer.example.com'
    else:
        orderer_name = 'orderer{}.example.com'.format(i + 1)
    orderer_port = '705{}'.format(i)
    operation_port = '3000{}'.format(i)
    container_name = orderer_name
    image = 'hyperledger/fabric-orderer:2.2.5'

    working_dir = '/opt/gopath/src/github.com/hyperledger/fabric'
    command = 'orderer'
    if i == 0:
        temp_volume = 'orderer.example.com:/var/hyperledger/production/orderer'
        temp_volume2 = '../organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp:/var/hyperledger/orderer/msp'
        temp_volume3 = '../organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/:/var/hyperledger/orderer/tls'
    else:
        temp_volume = 'orderer{}.example.com:/var/hyperledger/production/orderer'.format(i+1)
        temp_volume2 = '../organizations/ordererOrganizations/example.com/orderers/orderer{}.example.com/msp:/var/hyperledger/orderer/msp'.format(i+1)
        temp_volume3 = '../organizations/ordererOrganizations/example.com/orderers/orderer{}.example.com/tls/:/var/hyperledger/orderer/tls'.format(i+1)
    volumes = ['../system-genesis-block/genesis.block:/var/hyperledger/orderer/orderer.genesis.block',\
            temp_volume2,\
            temp_volume3,\
            temp_volume,\
            '../configtx/:/var/hyperledger/config']
    
    ####port part
    ports = []
    temp = '{}:{}'.format(int(orderer_port),int(orderer_port))
    ports.append(temp)
    temp = '{}:{}'.format(int(operation_port),int(operation_port))
    ports.append(temp)

    networks = []
    networks.append('test')
    environment = []

    loggig_spec = 'FABRIC_LOGGING_SPEC=INFO'
    general_listenaddress ='ORDERER_GENERAL_LISTENADDRESS=0.0.0.0'
    general_listenport = 'ORDERER_GENERAL_LISTENPORT={}'.format(orderer_port)
    general_genesismethod = 'ORDERER_GENERAL_GENESISMETHOD=file'
    general_genesisfile = 'ORDERER_GENERAL_GENESISFILE=/var/hyperledger/orderer/orderer.genesis.block'
    general_localmspid = 'ORDERER_GENERAL_LOCALMSPID=OrdererMSP'
    general_localmspdir = 'ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp'
    operations_listenaddress = 'ORDERER_OPERATIONS_LISTENADDRESS=0.0.0.0:{}'.format(operation_port)
    # enabled TLS
    general_tls_enabled = 'ORDERER_GENERAL_TLS_ENABLED=true'
    general_tls_privatekey = 'ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key'
    general_tls_cerificate = 'ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt'
    general_tls_rootcas = 'ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]'
    general_cluster_clientcertificate = 'ORDERER_GENERAL_CLUSTER_CLIENTCERTIFICATE=/var/hyperledger/orderer/tls/server.crt'
    general_cluster_clientprivatekey = 'ORDERER_GENERAL_CLUSTER_CLIENTPRIVATEKEY=/var/hyperledger/orderer/tls/server.key'
    general_cluster_rootcas = 'ORDERER_GENERAL_CLUSTER_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]'

    environment.append(loggig_spec)
    environment.append(general_listenaddress)
    environment.append(general_listenport)
    environment.append(general_genesismethod)
    environment.append(general_genesisfile)
    environment.append(general_localmspid)
    environment.append(general_localmspdir)
    environment.append(operations_listenaddress)
    environment.append(general_tls_enabled)
    environment.append(general_tls_privatekey)
    environment.append(general_tls_cerificate)
    environment.append(general_tls_rootcas)
    environment.append(general_cluster_clientcertificate)
    environment.append(general_cluster_clientprivatekey)
    environment.append(general_cluster_rootcas)



    #select server
    for index, server in enumerate(server_list):
        for node in server:
            if orderer_name.replace('.example.com','') == node:
                orderer_dict = {
                    'services': {orderer_name:{'container_name':container_name,'image':image,'environment':environment,'working_dir':working_dir,\
                                            'volumes':volumes,'command':command,'ports':ports,'networks':networks}}
                                            }
                with open('./docker/docker-compose-{}.yaml'.format(index), 'a') as f:
                    yaml.dump(orderer_dict,f,sort_keys=False)


if os.path.isdir('docker') == False:
    os.system('mkdir docker')

######case2 peer #########################
for o in range(1,n_org +1):
    for p in range(0,n_peer):
        peer_name = 'peer{}.{}.example.com'.format(p,'org{}'.format(o))
        peer_port = 8000 + o * 100 ## 8100, 8200. 8300
        peer_port = str(peer_port + p)
        chaincode_port = str(20000 + o * 100 + p)
        operation_port = str(32000 + o * 100 + p)
        container_name = peer_name
        image = 'hyperledger/fabric-peer:2.2.5'

        working_dir = '/opt/gopath/src/github.com/hyperledger/fabric'



        peer_volume = '../organizations/peerOrganizations/org{}.example.com/peers/peer{}.org{}.example.com/msp:/etc/hyperledger/fabric/msp'.format(o,p,o)
        peer_volume2 = '../organizations/peerOrganizations/org{}.example.com/peers/peer{}.org{}.example.com/tls:/etc/hyperledger/fabric/tls'.format(o,p,o)

        command = 'peer node start'
        volumes = ['/var/run/docker.sock:/host/var/run/docker.sock',\
                peer_volume,\
                peer_volume2,\
                '{}:/var/hyperledger/production'.format(peer_name),\
                '../configtx/:/var/hyperledger/config']
        ports = []
        temp = '{}:{}'.format(peer_port,peer_port)
        ports.append(temp)
        temp = '{}:{}'.format(chaincode_port,chaincode_port)
        ports.append(temp)
        temp = '{}:{}'.format(operation_port,operation_port)
        ports.append(temp)

        networks = []
        networks.append('test')



        environment = []

        ####environment part #######################
        if p == 0:
            gossip_bootstrap_port = 8000 + o * 100 + 1
            bootstrap_address = 'peer{}.org{}.example.com:{}'.format(1,o,gossip_bootstrap_port)
        else:
            gossip_bootstrap_port = 8000 + o * 100
            bootstrap_address = 'peer{}.org{}.example.com:{}'.format(0,o,gossip_bootstrap_port)


        vm_endpoint = 'CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock'
        vm_docker_hostconfig_networkmode = 'CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=testnet'
        logging_spec = 'FABRIC_LOGGING_SPEC=INFO'
        peer_tls_enabled = 'CORE_PEER_TLS_ENABLED=true'
        peer_profile_enabled = 'CORE_PEER_PROFILE_ENABLED=true'
        peer_tls_cert_file = 'CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt'
        peer_tls_key_file = 'CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key'
        peer_tls_rootcert_file = 'CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt'
        peer_id = 'CORE_PEER_ID={}'.format(peer_name)
        peer_address = 'CORE_PEER_ADDRESS={}:{}'.format(peer_name,peer_port)
        peer_listenaddress = 'CORE_PEER_LISTENADDRESS=0.0.0.0:{}'.format(peer_port)
        peer_chaincodeaddress = 'CORE_PEER_CHAINCODEADDRESS={}:{}'.format(peer_name,chaincode_port)
        peer_chaincodelistenaddress = 'CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:{}'.format(chaincode_port)
        peer_gossip_bootstrap = 'CORE_PEER_GOSSIP_BOOTSTRAP={}'.format(bootstrap_address)
        peer_gossip_externalendpoint = 'CORE_PEER_GOSSIP_EXTERNALENDPOINT={}:{}'.format(peer_name,peer_port)
        peer_localmspid = 'CORE_PEER_LOCALMSPID=Org{}MSP'.format(o)
        operations_listenaddress = 'CORE_OPERATIONS_LISTENADDRESS={}:{}'.format(peer_name, operation_port)

        environment.append(vm_endpoint)
        environment.append(vm_docker_hostconfig_networkmode)
        environment.append(logging_spec)
        environment.append(peer_tls_enabled)
        environment.append(peer_profile_enabled)
        environment.append(peer_tls_cert_file)
        environment.append(peer_tls_rootcert_file)
        environment.append(peer_tls_key_file)
        environment.append(peer_id)
        environment.append(peer_address)
        environment.append(peer_listenaddress)
        environment.append(peer_chaincodeaddress)
        environment.append(peer_chaincodelistenaddress)
        environment.append(peer_gossip_bootstrap)
        environment.append(peer_gossip_externalendpoint)
        environment.append(peer_localmspid)
        environment.append(operations_listenaddress)


        re = 0
        for index, i in enumerate(server_list):
            for j in i:
                na = peer_name.replace('.example.com', '')
                if j == na:
                    re = index
        extra_host = result[re]

        #select server
        for index, server in enumerate(server_list):
            for node in server:
                if peer_name.replace('.example.com','') == node:
                    with open('./docker/docker-compose-{}.yaml'.format(index)) as f:
                        service = yaml.load(f, Loader=yaml.FullLoader)
                        service['services'][peer_name] = {'container_name':container_name,'image':image,'environment':environment,'working_dir':working_dir,\
                                                'volumes':volumes,'command':command,\
                                                'extra_hosts': extra_host, 'ports':ports,'networks':networks}

                    with open('./docker/docker-compose-{}.yaml'.format(index), 'w') as f:
                        yaml.dump(service,f,sort_keys=False)



        #peer_dict = {'version': '3.7', 'volumes':{container_name:{}}, 'networks':{'test':{'name':'testnet', 'external':True}}, \
                        #'services': {peer_name:{'container_name':container_name,'image':image,'environment':environment,'working_dir':working_dir,\
                                      #          'volumes':volumes,'command':command,'ports':ports,'networks':networks}}}

        #with open('docker/docker-compose-{}.yaml'.format(peer_name), 'w') as f:
        #    yaml.dump(peer_dict,f,sort_keys=False)


#########cli part #########################

peer_name = 'cli'
image = 'hyperledger/fabric-tools:2.2.5'
command = '/bin/bash'
working_dir = '/opt/gopath/src/github.com/hyperledger/fabric/peer'
volumes = []
volumes.append('/var/run/:/host/var/run/')
volumes.append('../organizations:/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations')
volumes.append('../channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts')
volumes.append('../caliper-benchmarks:/opt/gopath/src/github.com/hyperledger/fabric/peer/caliper-benchmarks')
networks = []
networks.append('test')

environment = []
environment.append('GOPATH=/opt/gopath')
environment.append('CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock')
environment.append('FABRIC_LOGGING_SPEC=INFO')
environment.append('SYS_CHANNEL=system-channel')
environment.append('CORE_PEER_ID=cli')
environment.append('CORE_PEER_ADDRESS=peer0.org1.example.com:8100')
environment.append('CORE_PEER_LOCALMSPID=Org1MSP')
environment.append('CORE_PEER_TLS_ENABLED=true')
environment.append('CORE_PEER_PROFILE_ENABLED=true')
environment.append('CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.crt')
environment.append('CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.key')
environment.append('CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt')
environment.append('CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp')



peer_dict = {'version': '3.7', 'networks':{'test':{'name':'testnet', 'external':True}}, \
                'services': {peer_name:{'container_name':'cli','image':image, 'tty':True, 'stdin_open':True, 'environment':environment,'working_dir':working_dir,\
                                        'volumes':volumes,'command':command,'networks':networks}}}



with open('./docker/docker-compose-0.yaml') as f:
    service = yaml.load(f, Loader=yaml.FullLoader)
    service['services'][peer_name] = {'container_name':'cli','image':image, 'tty':True, 'stdin_open':True, 'environment':environment,'working_dir':working_dir,\
                                        'volumes':volumes,'command':command,'networks':networks}

with open('./docker/docker-compose-0.yaml', 'w') as f:
    yaml.dump(service,f,sort_keys=False)