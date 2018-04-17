"""
Test the simulator connection.
"""

import sys
sys.path[0:0] = ["gateway-job-manager-openfoam"]
import config
from connection import simulator

class DummyCredentials(object):
    """
    mimic a flask app's config object - allow 
    attributes to be retrieved via get()
    """
    def __init__(self,config):
        self.config = config
    def get(self, attr):
        return self.config.__getattribute__(value)


#from connection.simulator import Connection

def test_simulator_connection():
    my_config = config.DevelopmentConfig()
    credentials = DummyCredentials(my_config)
    con = simulator.SimulatorConnection(credentials)
    return con
    #   connection = Connection()
    assert(True)
    # out, err, exit_code = connection._run_remote_command('echo hello')
    # print(out, err, exit_code)
    # print(connection.hostname)
