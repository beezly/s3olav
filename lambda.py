import boto3
import requests
import tempfile
from py_clamav import ClamAvScanner

scanner = ClamAvScanner()

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

        infected, vir_name = scanner.scan_file(scanfile.name)

        if infected:
            return {'status_code': 403}
        else:
            # Write object back to S3 Object Lambda
            s3 = boto3.client('s3')
            s3.write_get_object_response(
                Body=tempfile,
                RequestRoute=request_route,
                RequestToken=request_token)

            return {'status_code': 200}
