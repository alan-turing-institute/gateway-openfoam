"""
Test the simulator connection.
"""

import time
import os
import sys
import json
import unittest.mock as mock

# add manager to import search path
sys.path[0:0] = ['gateway-job-manager-openfoam']

from connection import simulator
from preprocessor import file_putter

RESOURCE_DIR = os.path.join("tests","resources")

def mock_get_simulator_connection():
    """
    get the simulator connection, without needing a running app.
    """

    modified_config = json.load(open('gateway-job-manager-openfoam/config.testing.json'))
    # overwrite path to SSH key
    modified_config['SSH_PRIVATE_KEY_PATH'] = \
        'gateway-job-manager-openfoam/keys/simulator_key'

    credentials = simulator.SSH_Credentials(modified_config)
    connect = simulator.SimulatorConnection(credentials)
    return connect

def test_exec_command():
    """
    use the credentials in gateway-job-manager to ssh to simulator
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
    job_id = '66e0de89-925b-4f00-abf8-a400ea644ce4'
    copied_ok, message = file_putter.copy_scripts_to_backend(dambreak_dir,
                                                             simulation_root,
                                                             job_id)

    assert(copied_ok)

    # verify that we did copy something
    destination_dir = os.path.join(simulation_root, job_id)
    out, err, exit_code = connect.run_remote_command('ls ' + destination_dir)

    assert("0" in out)
    assert("Allclean" in out)

    subdir = os.path.join(destination_dir, "0")
    out, err, exit_code = connect.run_remote_command('ls ' + subdir)
    assert("alpha.water.orig" in out)
