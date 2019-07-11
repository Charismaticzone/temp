from distutils.dir_util import copy_tree
import os
from shutil import rmtree
import sys

from requests import Session

CWD = os.path.dirname(os.path.abspath(__file__))
BASE = 'http://localhost:8080/'
# BASE = 'http://localhost:6800/'
session = Session()

if len(sys.argv) != 2 or sys.argv[1] not in ['start', 'stop', 'restore']:
    sys.exit("""
        Run 'python scrapyd.py start' to start spiders;
        Run 'python scrapyd.py stop' to stop spiders;
        Run 'python scrapyd.py restore' to restore projects eggs.
    """)

if sys.argv[1] == 'start':
    print("starting spiders")
    for (project, spider) in [
        ('demo_short', 'test_short'),
        ('demo_short', 'test_short'),
        ('demo_long', 'test_long'),
        ('demo_short', 'test_short'),
    ]:
        print(session.post(BASE + 'schedule.json', data=dict(project=project, spider=spider)).json())
elif sys.argv[1] == 'stop':
    print("stopping spiders")
    projects = session.get(BASE + 'listprojects.json').json()['projects']
    for project in projects:
        result = session.get(BASE + 'listjobs.json?project=%s' % project).json()
        for status in ['pending', 'running']:
            for job_ in result[status]:
                for i in range(2):
                    print(session.post(BASE + 'cancel.json', data=dict(project=project, job=job_['id'])).json())
else:
    print("restoring projects eggs")
    os.chdir(CWD)
    eggs_path = os.path.join(CWD, 'eggs')
    rmtree(os.path.join(CWD, 'eggs'), ignore_errors=True)
    copy_tree(os.path.join(CWD, 'eggs_backup'), os.path.join(CWD, 'eggs'))
