import boto3
import requests
import tempfile
import os
from py_clamav import ClamAvScanner

scanner = ClamAvScanner()
scanner.load()

print("boto3 version:"+boto3.__version__)

def lambda_handler(event, context):
    print(event)

    object_get_context = event["getObjectContext"]
    request_route = object_get_context["outputRoute"]
    request_token = object_get_context["outputToken"]
    s3_url = object_get_context["inputS3Url"]

    # Get object from S3
    response = requests.get(s3_url)
    with tempfile.NamedTemporaryFile(mode='w+b',buffering=0) as scanfile:
        scanfile.write(response.content)

        scanfile.flush()
        os.fsync(scanfile.fileno()) 
        scanfile.seek(0)

        infected, vir_name = scanner.scan_file(scanfile.name)
        print(f'infected: {infected}')
        print(f'vir_name: {vir_name}')

        s3 = boto3.client('s3') 
        if infected:
            print('file was infected')
            s3.write_get_object_response(
                Body='',
                RequestRoute=request_route,
                RequestToken=request_token,
                StatusCode=403,
                ErrorCode='Forbidden',
                ErrorMessage='Forbidden')
            
        else:
            print('file was not infected')
            # Write object back to S3 Object Lambda
            s3 = boto3.client('s3')
            s3.write_get_object_response(
                Body=scanfile,
                RequestRoute=request_route,
                RequestToken=request_token)

    return {'status_code': 200}
