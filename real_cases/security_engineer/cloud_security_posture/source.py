import boto3

s3 = boto3.client('s3')

def list_buckets():
    response = s3.list_buckets()
    return response['Buckets']

def upload_file(bucket, file):
    # Hardcoded credentials
    AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    # No server-side encryption
    s3.upload_file(file, bucket, file)
    # Public access allowed
    s3.put_bucket_acl(ACL='public-read')

def create_instance():
    ec2 = boto3.client('ec2')
    # Security group allowing all traffic
    sg = ec2.create_security_group(
        GroupName='open-all',
        IpPermissions=[
            {'IpProtocol': '-1', 'FromPort': 0, 'ToPort': 65535, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    return sg