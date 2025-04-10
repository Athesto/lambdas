# Lambdas
This is a monorepo of differents lambdas


## Getting Started
To get started with the project, follow these steps:

### Prerequisites
Before you start, make sure you have the following:
- **Git** installed on your machine
- **GitHub** account
- **AWS account** to view your deployed code
- **SAM** installed on your machine for local development

### Setup a new Lambda Function
1. Copy the folder `lambdas/Templates/SimpleLambda`
    - Rename it to `lambdas/<your-lambda>` ex `lambdas/HelloWorld`
2. Modify `app.py` to your needs and `requirements.txt` to your needs
3. Modify template `template.yaml` to your needs
    - Duplicate Resources `TemplatesSimpleLambda` inside the `Resources` ex `HelloWorld`
    - Modify `CodeUri` to your needs

### Execute a Lambda Function with SAM locally
it needs `docker` installed on your machine
```
sam validate --lint
sam build
sam local invoke <Your-Resource-Name> [--watch]
```

### Execute a workflow locally
it needs `docker` installed on your machine
```
brew install act
act -j testing --container-architecture linux/amd64
```

### Display CloudFormation Outputs
```
export AWS_PROFILE=<your-profile> && aws cloudformation describe-stacks --stack-name Multilambdas
```

### Branch Structure
To maintain a structured and organized repository, follow the naming conventions for branches:

- **Feature branches:** Use the prefix `feat/`
- **Bug fix branches:** Use the prefix `fix/`
- **Ticket codes:** Use the format `LAM01` to `LAM99`
- **Short name:** Should be descriptive yet concise, with a maximum of 20 characters

### Useful Urls
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli.html)
- [AWS::CertificateManager::Certificate](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html)
- [AWS::Serverless::Api](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html)
- [AWS::Serverless::Function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html)
- [AWS::ApiGateway::DomainName](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html)

#### Example Branch Names:
- `feat/LAM01-add-user-auth`
- `feat/LAM25-update-logs`
- `fix/LAM10-bug-fix-login`
- `fix/LAM99-correct-error-msg`

## Licence
MIT
