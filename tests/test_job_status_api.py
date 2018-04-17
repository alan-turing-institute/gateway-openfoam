"""
Test the job start endpoint.
"""

import requests
import time
import os

JOB_MANAGER_URL = 'http://job-manager-openfoam:5001'

def test_job_status():
    """
    try to start a job
    """
    # wait a bit for the service to come up
    time.sleep(5)
    r = requests.get(JOB_MANAGER_URL+"/job/1/status")
    print(r.content)


