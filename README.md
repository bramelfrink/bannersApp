# Banners Assignment

## Updating the project
Push your changes to GitHub. CodePipeline will make sure that the changes are deployed.

## Deploying the stack
To deploy the Banners-CodePipeline stack, run the following:
```
aws cloudformation create-stack\
 --stack-name Banners-CodePipeline\
 --template-body file://cloudformation_templates/code_pipeline.yml
 --capabilities CAPABILITY_IAM\
 --parameters\
 ParameterKey=OAuthToken,ParameterValue=<A GitHub personal access token> \
 ParameterKey=GitBranch,ParameterValue=<The Git Branch>
```

## Updating the stack
```
aws cloudformation update-stack\
 --stack-name Banners-CodePipeline\
 --template-body file://cloudformation_templates/code_pipeline.yml
 --capabilities CAPABILITY_IAM\
 --parameters\
 ParameterKey=OAuthToken,ParameterValue=<A GitHub personal access token> \
 ParameterKey=GitBranch,ParameterValue=<The Git Branch>
```