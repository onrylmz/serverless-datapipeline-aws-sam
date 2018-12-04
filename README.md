# Sample Serverless Data Pipeline

This is a sample template for a serverless data pipeline - Below is a brief explanation of what I have generated for you:

```bash
.
├── README.md                       <-- This instructions file
├── pipeline                        <-- Source code for lambda functions
|   |   |── appliance
|   |   |    |── __init__.py
|   |   |    |── provision.py       <-- Provision event code
|   |   |    |── disconnected.py    <-- Disconnected event code
|   |   |── stream
|   |   |    |── __init__.py
|   |   |    |── backup.py          <-- Backup event code
│   ├── __init__.py
│   ├── utils.py                    <-- Util functions
│── requirements.txt                <-- Python dependencies
├── template.yaml                   <-- SAM Template
└── tests                           <-- Unit tests
    
```

## Requirements

* AWS CLI already configured with at least PowerUser permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Setup process

### Building the project

[AWS Lambda requires a flat folder](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) with the application as well as its dependencies. When you make changes to your source code or dependency manifest,
run the following command to build your project local testing and deployment:
 
```bash
sam build
```

If your dependencies contain native modules that need to be compiled specifically for the operating system running on AWS Lambda, use this command to build inside a Lambda-like Docker container instead:
```bash
sam build --use-container
```
 
By default, this command writes built artifacts to `.aws-sam/build` folder.


## Packaging and deployment

AWS Lambda Python runtime requires a flat folder with all dependencies including the application. SAM will use `CodeUri` property to know where to look up for both application and dependencies:

```yaml
...
  ProcessApplianceProvisioned:
    Type: 'AWS::Serverless::Function'
    Properties:
      CodeUri: pipeline/
      Handler: appliance/provision.lambda_handler
      Runtime: python3.6
        ...
```

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name sample-eesd \
    --capabilities CAPABILITY_IAM
```

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**

After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:

```bash
aws cloudformation describe-stacks \
    --stack-name sample-eesd \
    --query 'Stacks[].Outputs'
``` 

## Testing

```bash
python tests/test_kinesis.py provisioned disconnected
```

**NOTE**: It is recommended to use a Python Virtual environment to separate your application development from  your system Python installation.

# Appendix

### Python Virtual environment
**In case you're new to this**, python3 comes with `virtualenv` library by default so you can simply run the following:

1. Create a new virtual environment
2. Install dependencies in the new virtual environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```


**NOTE:** You can find more information about Virtual Environment at [Python Official Docs here](https://docs.python.org/3/tutorial/venv.html). Alternatively, you may want to look at [Pipenv](https://github.com/pypa/pipenv) as the new way of setting up development workflows
## AWS CLI commands

AWS CLI commands to package, deploy and describe outputs defined within the cloudformation stack:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME

sam deploy \
    --template-file packaged.yaml \
    --stack-name sample-eesd \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides MyParameterSample=MySampleValue

aws cloudformation describe-stacks \
    --stack-name sample-eesd --query 'Stacks[].Outputs'
```
* Sample Python with 3rd party dependencies, pipenv and Makefile: ``sam init --location https://github.com/onrylmz/serverless-datapipeline-aws-sam``
