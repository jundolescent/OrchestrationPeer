/*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

const owners = ['0'.repeat(13000), '1'.repeat(13000)];

/**
 * Workload module for the benchmark round.
 */
class ChangeCarOwnerWorkload extends WorkloadModuleBase {
    /**
     * Initializes the workload module instance.
     */
    constructor() {
        super();
        this.txIndex = 0;
    }

    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
    async submitTransaction() {
        this.txIndex++;
        let carNumber = 'Client' + this.workerIndex + '_CAR' + this.txIndex.toString();
        let newCarOwner = owners[Math.floor(Math.random() * owners.length)];

        let args = {
            contractId: 'fabcar',
            contractVersion: 'v1',
            contractFunction: 'changeCarOwner',
            contractArguments: [carNumber, newCarOwner],
            timeout: 60
        };

        if (this.txIndex === this.roundArguments.assets) {
            this.txIndex = 0;
        }

        await this.sutAdapter.sendRequests(args);
    }
}

/**
 * Create a new instance of the workload module.
 * @return {WorkloadModuleInterface}
 */
function createWorkloadModule() {
    return new ChangeCarOwnerWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
