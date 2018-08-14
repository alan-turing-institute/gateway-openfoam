"""
Test the job start endpoint.
"""

import requests
import time
import os
import sys
import json
from posixpath import join as urljoin


JOB_MANAGER_URL = 'http://manager:5001'

job_data = {
    "scripts" : [
      {
          "source" : "https://simulate.blob.core.windows.net/openfoam-test-cases/damBreak/0/alpha.water.orig" ,
          "action" : "null",
          "destination" : "0/alpha.water.orig",
          "patch" : False
      },
      {
          "source" : "https://simulate.blob.core.windows.net/openfoam-test-cases/damBreak/Allrun",
          "action" : "null",
          "destination" : "Allrun",
          "patch" : False
      }
    ],
    "username" : "testuser",
    "fields_to_patch": [ ]
}


def test_copy_scripts():
    """
    try to start a job
    """
    # wait a bit for the service to come up
    time.sleep(1)

    # none of the scripts have a "RUN" action, therefore the following
    # request to /start won't actually trigger a run
    r = requests.post(
        urljoin(JOB_MANAGER_URL, 'job/f6fdc57b-43c6-41f6-8a4b-1b5bb74d85ad/start'),
        json=job_data)
    print(r.content)
    rjson = json.loads(r.content.decode("utf-8"))
    assert(rjson["status"] == 200)


job_data_with_run = {
    "scripts" : [
      {
          "source" : "https://simulate.blob.core.windows.net/openfoam-test-cases/minimal/test_cmd.sh",
          "action" : "RUN",
          "destination" : "test_cmd.sh",
          "patch" : False
      }
    ],
    "username" : "testuser",
    "fields_to_patch": [ ]
}

def test_run_cmd():
    """
    try to start a job
    """
    # wait a bit for the service to come up
    time.sleep(1)
    r = requests.post(
        urljoin(JOB_MANAGER_URL, 'job/0bc72a99-390e-4929-a23f-d8e91b85dd34/start'),
        json=job_data_with_run)
    print(r.content)
    rjson = json.loads(r.content.decode("utf-8"))
    print(rjson["data"])
    assert(rjson["status"] == 200)
