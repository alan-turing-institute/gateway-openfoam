"""
Test the simulator connection.
"""

import time
import os

import sys
sys.path[0:0] = ["gateway-job-manager-openfoam"]
import config
from connection import simulator

class DummyConfig(object):
    """
    mimic a flask app's config object - allow 
    attributes to be retrieved via get()
    """
    def __init__(self,config):
        """
        constructor takes an instance of one of the classes in config.py
        just need to modify where the simulator_key is found
        """
        self.config = config
        self.config.SSH_PRIVATE_KEY_PATH = 'gateway-job-manager-openfoam/keys/simulator_key'
        
    def get(self, attribute):
        """
        return an attribute if it is in the config dictionary, otherwise None.
        """
        if attribute in self.config.__dir__():
            return self.config.__getattribute__(attribute)
        else:
            return None

        
def test_simulator_connection():
    """
    use the credentials in gateway-job-manager/config.py to ssh to simulator
    test that we can get the simulator to echo 'hello'
    """
    dev_config = config.DevelopmentConfig()
    dummy_config = DummyConfig(dev_config)
    credentials = simulator.SSH_Credentials(dummy_config)
    connect = simulator.SimulatorConnection(credentials)
    out, err, exit_code = connect._run_remote_command('echo hello')
    print(out, err, exit_code)
    assert(out.strip() == "hello")

