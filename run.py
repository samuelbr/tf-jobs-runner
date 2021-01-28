#!/usr/bin/python3.6

import time
import sys
import shutil
import subprocess

from pathlib import Path


SEARCH_PATH = Path(sys.argv[-1])

OUTPUT_LOG = SEARCH_PATH.joinpath('logs')
if not OUTPUT_LOG.exists():
    OUTPUT_LOG.mkdir(parents=True)

while True:
    jobs = SEARCH_PATH.glob('*')
    jobs = list(filter(lambda x: x.suffix == '.queue', jobs))
    if len(jobs) == 0:
        time.sleep(60)
        continue
    
    job = jobs[0]
    
    renamed_job = job.parent.joinpath(f'{job.stem}.run')
    completed_job = job.parent.joinpath(f'{job.stem}.completed')

    log_prefix = time.strftime("%Y%m%d_%H%M", time.gmtime())
    log_file = OUTPUT_LOG.joinpath(f'{log_prefix}_{job.stem}.log')

    shutil.move(job, renamed_job)
    if renamed_job.exists():
        #run job
        command = f'sh -f {str(renamed_job)}'
        print(f'Run job {job}')
        with open(log_file, 'wb') as log:
            try:
                rc = subprocess.call(f'sh -f {str(renamed_job)}', shell=True, stderr=log, stdout=log)
            except Exception as e:
                log.write('Exception: '+str(e))
                print('Job failed: '+str(e))
        print('Job finished')
        shutil.move(renamed_job, completed_job)
