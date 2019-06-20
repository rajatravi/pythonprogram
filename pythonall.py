#!/usr/bin/python
import sys
import os
import string
import time
import datetime
import getopt

#############
# CONFIG
#############
DB_NAME='mydb'
DB_PASSWORD='111111'
DB_USER='root'
DB_HOST='mylinux0'
SQL_DB_SCHEMA=os.path.abspath("db_schema.sql")
SQL_CREATE_TABLE=os.path.abspath("000.sql")
CLONE_TABLES=['MyJobs','MyUsers']

#############
# GLOBALS
#############
backup_db=False
migration=False
config=None
verbose=False
delete=False
remote=False

def sql_cmd(cmd):
    if remote:
        return 'mysql -h %s -u %s -p%s -e " %s " %s' % (DB_HOST,DB_USER,DB_PASSWORD,cmd,DB_NAME)
    return 'mysql -u %s -p%s -e " %s " %s' % (DB_USER,DB_PASSWORD,cmd,DB_NAME)

def sql_script(script):
    if remote:
        return 'mysql -h %s -u %s -p%s %s < %s' % (DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,script)
    return 'mysql -u %s -p%s %s < %s' % (DB_USER,DB_PASSWORD,DB_NAME,script)


def make_sql_to_create_table():
    s=open(SQL_DB_SCHEMA).read()
    for t in CLONE_TABLES:
        s=s.replace(t,t+'2')
    open(SQL_CREATE_TABLE,'w').write(s)

def backup_database():
    fname="%s-%s.dump.gz" % (DB_NAME,time.strftime('%Y%m%d%H%M%S', time.gmtime()))
    if remote:
        cmd="mysqldump -h %s -u %s -p%s --compact %s|gzip -9 > %s" % (DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,fname)
    else:
        cmd="mysqldump -u %s -p%s --compact %s|gzip -9 > %s" % (DB_USER,DB_PASSWORD,DB_NAME,fname)

    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

def delete_db_records():
    cmd=sql_cmd("delete from sources;delete from cameras;")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

def package():
    cmd="tar zcvf migrate-db.tar.gz *.sql migrate.py .migrate_*"
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

def read_config(config):
    global DB_NAME
    global DB_PASSWORD
    global DB_USER
    global DB_HOST
    f=open(config,"r")
    for line in f:
        a=line.split("=")
        if len(a)!=2:
            continue
        n=a[0].strip()
        v=a[1].strip()
        if n=="DB_NAME":
            DB_NAME=v
        elif n=="DB_PASSWORD":
            DB_PASSWORD=v
        elif n=="DB_USER":
            DB_USER=v
        elif n=="DB_HOST":
            DB_HOST=v

def usage():
    print '''
USAGE: python migrate.py [OPTIONS]

OPTIONS:
    -h, --help
        print this help

    -b, --backup-database
        backup the old database before migration (recommended)

    -m, --migrate
        donot start migration

    -v, --verbose
        print database related information

    -p, --package
        packge all the scripts into migrate-db.tar.gz

    -d, --delete-db-records
        delete database records so we can restart migration

    -c, --config

SAMPLES:
    python migrate.py -b                        #back database and exit
    python migrate.py -m                        #start migration right now
    python migrate.py -b -m                     #backup the database and start the migration (recommended)
    python migrate.py -v                        #print database information and exit
    python migrate.py -c .migrate_staging -v    #print staging database information and exit
'''

def show_info():
    print '''
==Database Information
name:{name}
password:{password}
user:{user}
host:{host}
'''.format(name=DB_NAME, password=DB_PASSWORD,user=DB_USER,host=DB_HOST)

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'WARNING: DONOT run me twice and migration CANNOT be rolled back, GO?'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

if __name__=="__main__":
    '''
    @see http://linux.byexamples.com/archives/366/python-how-to-run-a-command-line-within-python/
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hbmvpdc:r", ["help", "backup-database","--migrate","--verbose","--package","--delete-db-records","--config=","--remote"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        exit(2)

    if len(opts)==0:
        usage()
        exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-v", "--verbose"):
            verbose=True
        elif o in ("-c", "--config"):
            config=a
            print config
        elif o in ("-d", "--delete-db-records"):
            delete=True
        elif o in ("-p", "--package"):
            package()
            exit(0)
        elif o in ("-b", "--backup-database"):
            backup_db=True
        elif o in ("-m", "--migrate"):
            migration=True
        elif o in ("-r", "--remote"):
            remote=True
        else:
            assert False, "unhandled option"

    if config!=None:
        read_config(config)

    if delete:
        delete_db_records()
        sys.exit()

    if verbose:
        show_info()
        sys.exit()

    if backup_db:
        backup_database()

    if migration==False:
        exit(0)

    if confirm()==False:
        print "Aborting ..."
        exit(0)

    make_sql_to_create_table()

    print "==START MIGRATION"

    # test data base connection
    cmd=sql_cmd('show databases;use %s;' % (DB_NAME))
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    cmd=sql_script("000.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('001.sql')"))
    cmd=sql_script("001.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('002.sql')"))
    cmd=sql_script("002.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('003.sql')"))
    cmd=sql_script("003.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('004.sql')"))
    cmd=sql_script("004.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('005.sql')"))
    cmd=sql_script("005.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('006.sql')"))
    cmd=sql_script("006.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    os.system(sql_cmd("insert into migrate (Action) values ('100.sql')"))
    cmd=sql_script("100.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    cmd=sql_script("insert_sample_sources.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    cmd=sql_script("app_config.sql")
    print "==WILL RUN [ %s ]" % (cmd)
    os.system(cmd)
    print "==DONE"

    print "==END MIGRATION"
# vim: set expandtab tabstop=4 shiftwidth=4: