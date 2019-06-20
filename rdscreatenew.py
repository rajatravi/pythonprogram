#!/bin/python

import boto3
import time
import sys
import botocore

from botocore.config import Config


env= sys.argv[1]
db_identifier= sys.argv[2]
print(type(env))
print(db_identifier)

boto_config = Config(retries=dict(max_attempts=20))
client = boto3.client('rds', region_name='us-east-1', config=boto_config)
#### Create a new RDS instance ######
def create_rds(env,db_identifier,client):
       db_dev = {
           "DBName": "dev01",
           "DBInstanceIdentifier": db_identifier,
           "AllocatedStorage": 10,
           "DBInstanceClass": "db.t2.small",
           "Engine": "MySQL",
           "MasterUsername": "root",
           "MasterUserPassword": "Devops143",
           "VpcSecurityGroupIds": [
                   "sg-0707a21b4408bf30a",
           ],
           "DBSubnetGroupName": "default-vpc-0ab06776a7776d16e",
           "DBParameterGroupName": "default",
           "BackupRetentionPeriod": 7,
           "MultiAZ": False,
           "EngineVersion": "5.7.19",
           "PubliclyAccessible": False,
           "StorageType": "gp2",
       }

       db_qa = {
           "DBName": "qa01",
           "DBInstanceIdentifier": db_identifier,
           "AllocatedStorage": 10,
           "DBInstanceClass": "db.t2.small",
           "Engine": "MySQL",
           "MasterUsername": "root",
           "MasterUserPassword": "Devops143",
           "VpcSecurityGroupIds": [
                   "sg-0707a21b4408bf30a",
           ],
           "DBSubnetGroupName": "default-vpc-0ab06776a7776d16e",
           "DBParameterGroupName": "default",
           "BackupRetentionPeriod": 7,
           "MultiAZ": False,
           "EngineVersion": "5.7.19",
           "PubliclyAccessible": False,
           "StorageType": "gp2",
       }

       if sys.argv[1] == 'dev':
           try:
                   client.create_db_instance(**db_dev)
                   print("Creating rds instance with id : {}".format(db_identifier))
           except botocore.exceptions.ClientError as e:
                   if 'DBInstanceAlreadyExists' in e.message:
                       print("DB instance {} exists already".format(db_identifier))
                   else:
                       raise

       elif env == 'qa':
           try:
                   client.create_db_instance(**db_qa)
                   print("Creating rds instance with id : {}".format(db_identifier))
           except botocore.exceptions.ClientError as e:
                   if 'DBInstanceAlreadyExists' in e.message:
                       print("DB instance {} exists already".format(db_identifier))
                   else:
                       raise
       else:
           print("Pass arguments: dev|qa ")

       running = True
       while running:
           instances = client.describe_db_instances(DBInstanceIdentifier=db_identifier)
           status = instances.get('DBInstances')[0].get('DBInstanceStatus')
           print("Last DB status: {}".format(status))

           time.sleep(30)
           if status == 'available':
               rds_host = instances.get('DBInstances')[0].get('Endpoint').get('Address')

               print("DB instance ready with host: {}".format(rds_host))
               running = False
       return add_cname_record('test-devdb.tt.internal', rds_host)      


create_rds(env,db_identifier,client)
def add_cname_record(source, rds_host):
  try:
    response = client.change_resource_record_sets(
    HostedZoneId='Z4B8H857IIL5P',
    ChangeBatch= {
            'Comment': 'add %s -> %s' % (source, rds_host),
            'Changes': [
              {
               'Action': 'UPSERT',
               'ResourceRecordSet': {
                 'Name': source,
                 'Type': 'CNAME',
                 'TTL': 300,
                 'ResourceRecords': [{'Value': rds_host}]
              }
            }]

    })
  except Exception as e:
    print e
 
  