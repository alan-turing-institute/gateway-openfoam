"""
Test the job start endpoint. 
"""

import requests
import time
import os
import sys
import json

JOB_MANAGER_URL = 'http://job-manager-openfoam:5001'

job_data = {
    "scripts" : [
      {
          "source" : "https://sgmiddleware.blob.core.windows.net/testopenfoamapi/damBreak/0/alpha.water" ,
          "action" : "null",
          "destination" : "damBreak/0/alpha.water",
          "patch" : False
      },
      {
          "source" : "https://sgmiddleware.blob.core.windows.net/testopenfoamapi/damBreak/Allrun",
          "action" : "null",
          "destination" : "damBreak/Allrun",
          "patch" : False
      }
    ],
    "username" : "testuser",
    "fields_to_patch": [ ]
}

def test_job_start_api():
    """
    try to start a job
    """
    # wait a bit for the service to come up
    time.sleep(5)
    r = requests.post(JOB_MANAGER_URL+"/job/12345/start",json=job_data)
    print(r.content)
    rjson = json.loads(r.content.decode("utf-8"))
    assert(rjson["status"] == 0)

