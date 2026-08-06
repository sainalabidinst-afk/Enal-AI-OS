def deploy_lambda():
    # Hardcoded credentials
    LAMBDA_KEY = "lambda_key_12345"
    # No VPC
    # No encryption
    lambda_client.create_function(FunctionName='my-func', Runtime='python3.8', Role='', Handler='index.handler')