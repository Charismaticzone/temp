"""
(oneapp) shiyanlou:~/ $ cd ~
(oneapp) shiyanlou:~/ $ rm -rf temp
(oneapp) shiyanlou:~/ $ git clone https://github.com/my8100/temp.git
(oneapp) shiyanlou:~/ $ cp -r temp/* .
"""
from distutils.dir_util import copy_tree
import os
from shutil import rmtree
import sys
import time

from requests import Session

CWD = os.path.dirname(os.path.abspath(__file__))
BASE = 'http://localhost:8080/'
# BASE = 'http://localhost:6800/'
session = Session()


def status():
    print(session.get(BASE + 'daemonstatus.json').json())


def start():
    print("starting spiders")
    for (project, spider) in [
        ('demo_short', 'test_short'),
        ('demo_short', 'test_short'),
        ('demo_long', 'test_long'),
        ('demo_short', 'test_short'),
    ]:
        print(session.post(BASE + 'schedule.json', data=dict(project=project, spider=spider)).json())
        time.sleep(2)


def stop():
    print("stopping spiders")
    projects = session.get(BASE + 'listprojects.json').json()['projects']
    for project in projects:
        result = session.get(BASE + 'listjobs.json?project=%s' % project).json()
        print(result)
        for status in ['pending', 'running']:
            for job_ in result[status]:
                for i in range(2):
                    print(status, project, job_['spider'], job_['id'])
                    print(session.post(BASE + 'cancel.json', data=dict(project=project, job=job_['id'])).json())


def restore():
    print("restoring projects eggs")
    os.chdir(CWD)
    eggs_path = os.path.join(CWD, 'eggs')
    rmtree(os.path.join(CWD, 'eggs'), ignore_errors=True)
    print("dir eggs removed")
    copy_tree(os.path.join(CWD, 'eggs_backup'), os.path.join(CWD, 'eggs'))
    print("dir eggs_backup copied to dir eggs")


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['status', 'start', 'stop', 'restore']:
        sys.exit("""
            Run 'python scrapyd.py start' to start spiders;
            Run 'python scrapyd.py stop' to stop spiders;
            Run 'python scrapyd.py restore' to restore projects eggs.
        """)
    if sys.argv[1] == 'status':
        status()
    elif sys.argv[1] == 'start':
        start()
    elif sys.argv[1] == 'stop':
        stop()
    else:
        restore()
