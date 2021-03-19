FROM public.ecr.aws/lambda/python:3.8
RUN yum -y install amazon-linux-extras
RUN cp -r /lib/python2.7/site-packages/amazon_linux_extras /var/lang/lib/python3.8/site-packages
RUN amazon-linux-extras install epel
RUN yum -y install clamav
COPY lambda.py ./
COPY requirements.txt ./ 
RUN pip install -U -r requirements.txt -t .
RUN freshclam
CMD ["lambda.lambda_handler"]
