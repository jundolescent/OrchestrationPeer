#!/bin/bash

function one_line_pem {
    echo "`awk 'NF {sub(/\\n/, ""); printf "%s\\\\\\\n",$0;}' $1`"
}

function json_ccp {
    local PP=$(one_line_pem $6)
    local CP=$(one_line_pem $7)
    sed -e "s/\${ORG}/$1/" \
        -e "s/\${P0PORT1}/$2/" \
        -e "s/\${CAPORT}/$3/" \
        -e "s/\${P0PORT2}/$4/" \
        -e "s/\${IP}/$5/" \
        -e "s#\${PEERPEM}#$PP#" \
        -e "s#\${CAPEM}#$CP#" \
        ccp-template.json
}

# function yaml_ccp {
#     local PP=$(one_line_pem $6)
#     local CP=$(one_line_pem $7)
#     sed -e "s/\${ORG}/$1/" \
#         -e "s/\${P0PORT1}/$2/" \
#         -e "s/\${CAPORT}/$3/" \
#         -e "s/\${P0PORT2}/$4/" \
#         -e "s/\${IP}/$5/" \
#         -e "s#\${PEERPEM}#$PP#" \
#         -e "s#\${CAPEM}#$CP#" \
#         ccp-template.yaml | sed -e $'s/\\\\n/\\\n          /g'
# }


IP=$1
ORG=$2
P0PORT1=$3
CAPORT1=$4
P0PORT2=$5
PEERPEM=organizations/peerOrganizations/org${ORG}.example.com/tlsca/tlsca.org${ORG}.example.com-cert.pem
CAPEM=organizations/peerOrganizations/org${ORG}.example.com/ca/ca.org${ORG}.example.com-cert.pem

echo "$(json_ccp $ORG $P0PORT1 $CAPORT1 $P0PORT2 $IP $PEERPEM $CAPEM)" > organizations/peerOrganizations/org${ORG}.example.com/connection-org${ORG}.json
#echo "$(yaml_ccp $ORG $P0PORT1 $CAPORT1 $P0PORT2 $PEERPEM $CAPEM)" > organizations/peerOrganizations/org1.example.com/connection-org1.yaml
