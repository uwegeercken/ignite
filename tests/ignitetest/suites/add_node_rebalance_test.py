# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ducktape.tests.test import Test

from ignitetest.services.ignite.ignite import IgniteService
from ignitetest.services.ignite_client_app import IgniteClientApp


class AddNodeRebalanceTest(Test):
    NUM_NODES = 3
    REBALANCE_TIMEOUT = 600

    """
    Test performs rebalance tests.
    """
    def __init__(self, test_context):
        super(AddNodeRebalanceTest, self).__init__(test_context=test_context)
        self.ignite = IgniteService(test_context, num_nodes=AddNodeRebalanceTest.NUM_NODES)

    def setUp(self):
        # starting all nodes except last.
        for i in range(AddNodeRebalanceTest.NUM_NODES-1):
            self.ignite.start_node(self.ignite.nodes[i])

    def teardown(self):
        self.ignite.stop()

    def test_add_node(self):
        """
        Test performs add node rebalance test which consists of following steps:
            * Start cluster.
            * Put data to it via CacheDataProducer.
            * Start one more node.
            * Await for rebalance to finish.
        """
        self.logger.info("Start add node rebalance test.")

        # This client just put some data to the cache.
        IgniteClientApp(self.test_context).run()

        self.ignite.start_node(self.ignite.nodes[AddNodeRebalanceTest.NUM_NODES-1],
                               timeout_sec=AddNodeRebalanceTest.REBALANCE_TIMEOUT,
                               wait_for_rebalance = True)
