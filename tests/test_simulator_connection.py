"""
Test the simulator connection.
"""

import time
import os
import sys
import unittest.mock as mock

sys.path[0:0] = ["gateway-job-manager-openfoam"]
import config
from connection import simulator
from preprocessor import file_putter

RESOURCE_DIR = os.path.join("tests","resources")


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


def mock_get_simulator_connection():
    """
    get the simulator connection, without needing a running app.
    """
    dev_config = config.DevelopmentConfig()
    dummy_config = DummyConfig(dev_config)
    credentials = simulator.SSH_Credentials(dummy_config)
    connect = simulator.SimulatorConnection(credentials)
    return connect

def test_exec_command():
    """
    use the credentials in gateway-job-manager/config.py to ssh to simulator
    test that we can get the simulator to echo 'hello'
    """
    connect = mock_get_simulator_connection()
    out, err, exit_code = connect.run_remote_command('echo hello')
    assert(out.strip() == "hello")


@mock.patch('preprocessor.file_putter.get_simulator_connection',
            side_effect=mock_get_simulator_connection)
def test_script_transfer(mock_get_simulator_connection):
    """
    copy a directory full of scripts, with some directory structure, and
    check that they are there.
    """
    # get our own ssh connection so we can clear directory before starting,
    # and later check the results of the copy
    connect = mock_get_simulator_connection()
    # source and dest dirs
    dambreak_dir = os.path.join(RESOURCE_DIR, "damBreak")
    simulation_root = '/tmp'

    # now call the actual function
    job_id = '7d839169-9588-4a8d-8416-5dc32cde113e'
    copied_ok, message = file_putter.copy_scripts_to_backend(dambreak_dir,
                                                             simulation_root,
                                                             job_id)

    print('DEBUG')
    print(copied_ok)
    print(message)

    # assert(copied_ok)

    # verify that we did copy something
    destination_dir = os.path.join(simulation_root, job_id)
    out, err, exit_code = connect.run_remote_command('ls ' + destination_dir)

    print('ls {}'.format(destination_dir))
    print(out)

    # assert("0" in out)
    # assert("Allclean" in out)

    subdir = os.path.join(destination_dir, "0")
    out, err, exit_code = connect.run_remote_command('ls ' + subdir)
    # assert("alpha.water.orig" in out)

    print('ls {}'.format(subdir))
    print(out)
