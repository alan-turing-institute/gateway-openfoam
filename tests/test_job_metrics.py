"""
Test the job start endpoint.
"""

import requests
import time
import os
import sys
import json
from posixpath import join as urljoin


JOB_MANAGER_URL = "http://manager:5001"
# JOB_MANAGER_URL = "http://localhost:5001"

scripts = [
    {
        "source": "https://simulate.blob.core.windows.net/openfoam-test-cases/damBreak/Simulate/metrics.py",
        "action": "METRICS",
        "destination": "Simulate/metrics.py",
        "patch": False,
    },
    {
        "source": "https://simulate.blob.core.windows.net/openfoam-test-cases/damBreak/Simulate/state/job_id",
        "action": "",
        "destination": "Simulate/state/job_id",
        "patch": True,
    },
]

job_data = {
    "scripts": scripts,
    "username": "testuser",
    "fields_to_patch": [
        {"name": "job_id", "value": "95d1028c-809e-4bc4-9999-6b74353bfda9"}
    ],
}


job_data_metrics = {"username": "testuser", "scripts": scripts}


def test_metrics():
    """
    Copy mock metrics script and run it.
    """
    # wait a bit for the service to come up
    time.sleep(1)

    # action "RUN" is not present, hence first request below only copies the file
    requests.post(
        urljoin(JOB_MANAGER_URL, "job/95d1028c-809e-4bc4-9999-6b74353bfda9/start"),
        json=job_data,
    )

    r = requests.post(
        urljoin(JOB_MANAGER_URL, "job/95d1028c-809e-4bc4-9999-6b74353bfda9/metrics"),
        json=job_data_metrics,
    )
    rjson = json.loads(r.content.decode("utf-8"))
    print(rjson)
    assert rjson["status"] == 200
