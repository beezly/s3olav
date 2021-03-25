s3olav
======

S3 Object Lambda - ClamAV Virus Scanning

Get going
---------

1. Build the container with and push it into an ECR repository. See https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html for more information on how to do to this. You can also use CodeBuild with the included `buildspec` to build and push into ECR - see the buildspec for parameters.
2. Create a new Lambda. The IAM role for the Lambda will need the AWSLambdaExecute role and S3 Object Lambda GetObject and WriteGetObjectResponse permissions. For the lambda function, point Lambda at the container image in ECR. I recommend that you configure the lambda to have plenty of RAM. In use it seems to use just over 1GB, but it will benefit from having at least 1vCPU to run on, so consider using 1769MB (see https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html). 
3. Create an S3 Access Point pointing at the S3 bucket you want to scan.
4. Create an S3 Object Lambda Access Point pointing at the S3 Access Point and use the previously configured Lambda function as the lambda function to call.
5. Profit (or call the s3 object lambda access point with `aws s3api get-object --bucket <access point arn> --key <key> <outputfile>` to test. You can use the eicar.com file available from https://www.eicar.org/?page_id=3950 as a test "infected" file. 

Caveats
-------

This was written as a test and I did the minimum required to see if it would work. 

The lambda takes about 20 seconds to start from cold. This is because it libclamav has to compile it's detection engine each time it starts up.

The lambda won't deal well with large files (over c. 500MB). This is because it does not stream content through the lambda. Instead it downloads to a temporary file, scans and then returns the object to the caller. It's possible that this could be made more efficient if I can work out how to get libclamav to scan a stream.

The build process pulls in the latest anti-virus definitions at runtime. If you want to update them, rebuild the container
