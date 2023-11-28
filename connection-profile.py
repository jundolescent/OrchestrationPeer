import json
import yaml
import os

with open('./NodeDeployment.yaml') as f:
    deployment = yaml.load(f, Loader=yaml.FullLoader)

n_orderer = deployment['Deployment']['orderer']
n_org = deployment['Deployment']['organization']
n_peer = deployment['Deployment']['peer']
n_server = deployment['Deployment']['server']
server_ip = {}
for server_list in deployment['Deployment']['deployment']:

    temp = server_list['configuration'] 
    for i in temp:
        server_ip[i] = server_list['ip']
        #os.system('sh ./manage-etc-hosts.sh add {} {}.example.com'.format(server_list['ip'], i))

print(server_ip)

with open("ccp-template.json", "r") as f:
     connection = json.load(f)

print(connection['peers'])

     #    "peer1.org${ORG}.example.com": {
     #        "url": "grpcs://${IP}:${P0PORT2}",
     #        "tlsCACerts": {
     #            "pem": "${PEERPEM}"
     #        },
     #        "grpcOptions": {
     #            "ssl-target-name-override": "peer1.org${ORG}.example.com",
     #            "hostnameOverride": "peer1.org${ORG}.example.com"
     #        }
     #    }

#          "organizations": {
#         "Org${ORG}": {
#             "mspid": "Org${ORG}MSP",
#             "peers": [
#                 "peer0.org${ORG}.example.com",
#                 "peer1.org${ORG}.example.com"
#             ],
#             "certificateAuthorities": [
#                 "ca.org${ORG}.example.com"
#             ]
#         }
#     },

# for peer0 and peer1
connection['peers']['peer0.org${ORG}.example.com']['url'] = "grpcs://{}:{}".format(server_ip['peer0.org1'], 8100)
connection['peers']['peer1.org${ORG}.example.com']['url'] = "grpcs://{}:{}".format(server_ip['peer1.org1'], 8101)

for peer in range(2, n_peer):
     connection['organizations']['Org${ORG}']['peers'].append('peer{}.org${{ORG}}.example.com'.format(peer))
     peer_port = 8100 + peer 
     peer_ip = server_ip['peer{}.org1'.format(peer)]
     temp_peer = {"peer{}.org${{ORG}}.example.com".format(peer):{
                                             "url":"grpcs://{}:{}".format(peer_ip, peer_port),\
                                             "tlsCACerts":{
                                                  "pem": "${PEERPEM}"
                                             },\
                                             "grpcOptions": {
                                                  "ssl-target-name-override": "peer{}.org${{ORG}}.example.com".format(peer),
                                                  "hostnameOverride": "peer{}.org${{ORG}}.example.com".format(peer)
                                             }}}
     connection['peers'].update(temp_peer) 

print(connection['organizations']['Org${ORG}']['peers'])



print(connection['peers'])

with open("ccp-template2.json", "w") as json_file:
     json.dump(connection, json_file, indent=4)

os.system('./generateccp.sh 1')