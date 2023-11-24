import yaml
import sys
import os
class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True

with open('./crypto-config.yaml') as f:
    crypto = yaml.load(f, Loader=yaml.FullLoader)





##### the number of orderer, the number of organization #########
#n_orderer = int(sys.argv[1])
#n_org = int(sys.argv[2])
#n_peer = int(sys.argv[3])
##### the number of orderer, the number of organization #########
##### location of peer node #################
with open('./NodeDeployment.yaml') as f:
    deployment = yaml.load(f, Loader=yaml.FullLoader)

n_orderer = deployment['Deployment']['orderer']
n_org = deployment['Deployment']['organization']
n_peer = deployment['Deployment']['peer']



server_ip = {}
for server_list in deployment['Deployment']['deployment']:

    temp = server_list['configuration'] 
    for i in temp:
        server_ip[i] = server_list['ip']
        #os.system('sh ./manage-etc-hosts.sh add {} {}.example.com'.format(server_list['ip'], i))

print(server_ip)

#####initialize orderer,peer list########

orderer_list = []
org_list = []

for i in range(0,n_orderer):
    if i == 0:
        orderer_list.append('orderer.example.com:7050')
    else:
        orderer_list.append('orderer{}.example.com:705{}'.format(i + 1, i))

for i in range(1,n_org+1):
    org_list.append('Org{}'.format(i))


#####orderer part########################


#initialize
del crypto['OrdererOrgs'][0]['Specs'][2]
del crypto['OrdererOrgs'][0]['Specs'][1]
del crypto['OrdererOrgs'][0]['Specs'][0]

#select
for i in orderer_list:
    temp = i.find('.')
    temp2 = i.find(':')
    temp_orderer = {'Hostname':i[:temp],'SANS':['localhost','127.0.0.1',i[:temp2]]}
    crypto['OrdererOrgs'][0]['Specs'].append(temp_orderer)


#####peer part###########################


#initialize
print(crypto['PeerOrgs'])
del crypto['PeerOrgs'][1]
del crypto['PeerOrgs'][0]

#select
for i in org_list:
    temp_org = {'Name':i,'Domain':'{}.example.com'.format(i.lower()),'EnableNodeOUs':True, 'Template':{'Count':n_peer,'SANS':['localhost','127.0.0.1',"{{.Hostname}}.{}.example.com".format(i.lower())]},'Users':{'Count':1}}
    crypto['PeerOrgs'].append(temp_org)
print(crypto['PeerOrgs'])
                
with open('organizations/cryptogen/crypto-config.yaml', 'w') as f:
    yaml.dump(crypto, f,Dumper=NoAliasDumper, sort_keys=False)