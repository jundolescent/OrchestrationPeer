 #!/bin/bash

 mkdir result
 for i in $(seq 1 2)
 do
  npx caliper launch manager --caliper-workspace ./ --caliper-networkconfig networks/networkConfig.yaml --caliper-benchconfig benchmarks/samples/fabric/fabcar/config.yaml --caliper-flow-only-test --caliper-fabric-gateway-enabled

  cp report.html ./result/${i}.html
  rm report.html
 done