import yaml
import sys
import os
from itertools import permutations

def generate_peer_combinations(ns, np):
    cb = permutations(range(1, np +1), ns)
    valid_cb = []
    for c in cb:
        if len(set(c)) == ns  and sum(c) == np:
            valid_cb.append(c)
    return valid_cb

bandwidth_list = [100, 200, 300, 400, 500]

# only for 2 server.
for bw in bandwidth_list:
    ##### the number of orderer, the number of organization #########
    ##### location of peer node #################
    with open('./NodeDeployment.yaml') as f:
        deployment = yaml.load(f, Loader=yaml.FullLoader)

    for ns in range(2,3): # if ns > 3, should change mininet script
        for np in range(2,10):
            deployment['Deployment']['server'] = ns
            deployment['Deployment']['peer'] = np
            #n_orderer = deployment['Deployment']['orderer']
            #n_org = deployment['Deployment']['organization']
            n_peer = deployment['Deployment']['peer']
            n_server = deployment['Deployment']['server']
            deployment['Deployment']['deployment'].clear()
            #print(deployment['Deployment']['deployment'])
            deployment['Deployment']['bandwidth'] = bw

            valid_peer_cb = generate_peer_combinations(n_server, n_peer)
            for c in valid_peer_cb:
                total = 0
                for server in range(1,n_server + 1):
                    peer_list = []
                    if server == 1:
                        peer_list.append('orderer')
                    for p in range(total,c[server - 1] + total):
                        peer_list.append('peer{}.org1'.format(p))
                    total = total + c[server - 1]
                    temp = {'Host': server, \
                            'configuration':peer_list,\
                            'ip': '10.0.0.{}'.format(server)}
                    deployment['Deployment']['deployment'].append(temp)
                with open('result.yaml', 'w') as f:
                    yaml.dump(deployment, f, sort_keys=False)
                ################################################
                os.system('sudo mn -c')
                os.system('python3 orchestration.py')

                ################################################
                deployment['Deployment']['deployment'].clear()
