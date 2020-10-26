import glob
import time

import sys
import shutil

import tempfile
import subprocess

import os

from pathlib import Path


SEARCH_PATH = Path(sys.argv[-1])

while True:
    jobs = SEARCH_PATH.glob('*')
    jobs = list(filter(lambda x: not x.name.endswith('.run') and not x.name.endswith('.completed'), jobs))
    
    if len(jobs) == 0:
        time.sleep(60)
        continue
    
    job = jobs[0]
    
    renamed_job = job.parent.joinpath(f'{job.name}.run')
    completed_job = job.parent.joinpath(f'{job.name}.completed')
    shutil.move(job, renamed_job)
    if renamed_job.exists():
        #run job
        command = f'sh -f {str(renamed_job)}'
        with tempfile.NamedTemporaryFile(delete=False) as f:
            print(f'Run job {job} stdout: {f.name}')
            rc = subprocess.call(f'sh -f {str(renamed_job)}', shell=True, stderr=subprocess.PIPE, stdout=f)
            print('Job finished')
            shutil.move(renamed_job, completed_job)
