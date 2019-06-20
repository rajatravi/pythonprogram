#!/usr/bin/python
import os.path
import time;
DIRNAME = '/home/tt/top2'
CODE_PATH = '/home/tt/current2'
REPO = 'https://github.com/thockin/test.git'

def CreateDirIfNotExist():
    if not os.path.exists(DIRNAME):
       os.makedirs(DIRNAME, 0755)

def deploy(): 
    ts = str(time.time())
    print (ts)
    os.chdir(DIRNAME)
    os.system("git clone  https://github.com/thockin/test.git %s" % ts)
    if os.path.islink(CODE_PATH):
       os.unlink(CODE_PATH)
    os.symlink(DIRNAME + "/" + ts, CODE_PATH)

def cleanup():
    os.chdir(DIRNAME)
    os.system("rm -rf $(ls -rt | head -n -3)")

CreateDirIfNotExist()
deploy()
cleanup()
