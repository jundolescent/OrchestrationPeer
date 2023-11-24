import yaml
import sys

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True

with open('./configtx.yaml') as f:
    configtx = yaml.load(f, Loader=yaml.FullLoader)

"""
print(configtx['Organizations'])
print(configtx['Capabilities'])
print(configtx['Application'])
print(configtx['Orderer'])
print(configtx['Channel'])
print(configtx['Profiles'])
"""



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

print(org_list)

#####orderer part########################

#initialize
configtx['Organizations'][0]['OrdererEndpoints'].clear()
configtx['Orderer']['Addresses'].clear()
configtx['Orderer']['EtcdRaft']['Consenters'].clear()


#select
for i in orderer_list:
    configtx['Organizations'][0]['OrdererEndpoints'].append(i)
    configtx['Orderer']['Addresses'].append(i) 
    temp = i.find(':')
    temp_address = i[:temp]
    temp_port = int(i[temp+1:])
    temp_Cert = '../organizations/ordererOrganizations/example.com/orderers/{}/tls/server.crt'.format(temp_address)
    consenter_dict = {'Host':temp_address,'Port':temp_port,'ClientTLSCert':temp_Cert,'ServerTLSCert':temp_Cert}
    configtx['Orderer']['EtcdRaft']['Consenters'].append(consenter_dict)



#####peer part###########################


print(configtx['Organizations'][2])
#initialize
del configtx['Organizations'][3]
del configtx['Organizations'][2]
del configtx['Organizations'][1]

del configtx['Profiles']['TwoOrgsOrdererGenesis']['Consortiums']['SampleConsortium']['Organizations'][2]
del configtx['Profiles']['TwoOrgsOrdererGenesis']['Consortiums']['SampleConsortium']['Organizations'][1]
del configtx['Profiles']['TwoOrgsOrdererGenesis']['Consortiums']['SampleConsortium']['Organizations'][0]

del configtx['Profiles']['TwoOrgsChannel']['Application']['Organizations'][2]
del configtx['Profiles']['TwoOrgsChannel']['Application']['Organizations'][1]
del configtx['Profiles']['TwoOrgsChannel']['Application']['Organizations'][0]

#select
for i in org_list:
    temp_name = '{}MSP'.format(i)
    temp_MSPDir = '../organizations/peerOrganizations/{}.example.com/msp'.format(i.lower())
    temp_readers = "OR(\'{}MSP.admin\', \'{}MSP.peer\', \'{}MSP.client\')".format(i,i,i)
    temp_writers = "OR(\'{}MSP.admin\', \'{}MSP.client\')".format(i,i)
    temp_admins = "OR(\'{}MSP.admin\')".format(i)
    temp_endorsement = "OR(\'{}MSP.peer\')".format(i)
    temp_org = {'Name':temp_name,'ID':temp_name,'MSPDir':temp_MSPDir,'Policies':{'Readers':{'Type':'Signature','Rule':temp_readers},\
                                                                                                  'Writers':{'Type':'Signature','Rule':temp_writers},\
                                                                                                  'Admins':{'Type':'Signature','Rule':temp_admins},\
                                                                                                  'Endorsement':{'Type':'Signature','Rule':temp_endorsement}},\
                                                                                                    'AnchorPeers':[{'Host':'peer0.{}.example.com'.format(i.lower()),'Port':8000+int(i[-1]) * 100}]}
    
    configtx['Organizations'].append(temp_org)
    configtx['Profiles']['TwoOrgsOrdererGenesis']['Consortiums']['SampleConsortium']['Organizations'].append(temp_org)
    configtx['Profiles']['TwoOrgsChannel']['Application']['Organizations'].append(temp_org)

print(configtx['Organizations'])



with open('configtx/configtx.yaml', 'w') as f:
    yaml.dump(configtx, f, sort_keys=False)
    #yaml.dump(configtx, f,Dumper=NoAliasDumper, sort_keys=False)