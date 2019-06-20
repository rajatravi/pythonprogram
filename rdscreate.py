import boto3
from botocore.config import Config

boto_config = Config(retries=dict(max_attempts=20))
client = boto3.client(
    'rds', region_name='us-east-1', config=boto_config
)
db_name = input
db_vars = {
    "DBName": "db_name",
    "DBInstanceIdentifier": "instance_name",
    "AllocatedStorage": 20,
    "DBInstanceClass": "db.m3.medium",
    "Engine": "mysql",
    "MasterUsername": "username",
    "MasterUserPassword": "password",
    "VpcSecurityGroupIds": [
        "sg-0007c6489efbd9bca",
    ],
    "DBSubnetGroupName": "my-subnet",
    "Port": "3306",
    "DBParameterGroupName": "",
    "BackupRetentionPeriod": 2,
    "MultiAZ": True,
    "EngineVersion": "9.7.19",
    "PubliclyAccessible": False,
    "StorageType": "ssd",
}
client.create_db_instance(**db_vars)
source = boto3.client('rds', region_name='us-east-1')
instances = source.describe_db_instances(DBInstanceIdentifier=db_instance)
rds_host = instances.get('DBInstances')[0].get('Endpoint').get('Address')
print (rds_host)

client = boto3.client('route53')
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
add_cname_record('test-devdb.tt.internal', rds_host)		