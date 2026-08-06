def create_bucket():
    # Hardcoded credentials
    AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
    # No encryption
    # No versioning
    s3.create_bucket(Bucket='my-bucket')
    return True

def set_bucket_policy():
    # Public access
    s3.put_bucket_policy(Bucket='my-bucket', Policy=public_policy)