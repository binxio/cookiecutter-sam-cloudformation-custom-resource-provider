.PHONY: help install test bucket build package deploy invoke-local invoke-deployed

PROJECT_NAME = {{cookiecutter.project_name}}
SAM_PROJECT_BUCKET = sam-$(shell aws sts get-caller-identity --query Account --output text)-$(shell aws configure get region)

_TEMPLATE = .aws-sam/build/template.yaml


help:           ## shows description of all available make targets
	@fgrep -h "##" $(MAKEFILE_LIST) | sed -e 's/\([^:]*\):[^#]*\(##.*\)/\1			\2/' | grep -v fgrep

build: $(_TEMPLATE)	## the lambda deployment zip in .aws-sam/

test: Pipfile.lock		## runs the unit tests in ./tests
	pipenv run pytest

deploy: packaged.yaml	## uploads the lambda deployment zip file and deploys ./template.yml to aws
	sam deploy \
		--template-file packaged.yaml \
		--capabilities CAPABILITY_IAM \
		--stack-name $(PROJECT_NAME)

packaged.yaml: $(_TEMPLATE)
	sam package \
		--s3-bucket $(SAM_PROJECT_BUCKET) \
		--s3-prefix $(PROJECT_NAME) \
		--output-template-file packaged.yaml


bucket:		## creates s3 bucket for uploading the lambda zip 
	@pipenv run aws s3 ls s3://$(SAM_PROJECT_BUCKET) > /dev/null 2>&1 || pipenv run aws s3 mb s3://$(SAM_PROJECT_BUCKET) ; echo $(SAM_PROJECT_BUCKET) created


invoke-local: $(_TEMPLATE)	## runs integration test of events in ./events
	sam local invoke -e ./events/create.json
	sam local invoke -e ./events/update.json
	sam local invoke -e ./events/delete.json

invoke-deployed: FUNCTION_ARN=$(shell aws cloudformation describe-stacks \
				  --stack-name $(PROJECT_NAME) \
				  --query 'Stacks[0].Outputs[?OutputKey==`ServiceToken`].OutputValue' \
				  --output text)
invoke-deployed:	## runs system test of events in ./events
	aws lambda invoke \
		--function-name $(FUNCTION_ARN) \
		--payload '$(shell cat ./events/create.json)' \
		/dev/stdout
	aws lambda invoke \
		--function-name $(FUNCTION_ARN) \
		--payload '$(shell cat ./events/update.json)' \
		/dev/stdout
	aws lambda invoke \
		--function-name $(FUNCTION_ARN) \
		--payload '$(shell cat ./events/delete.json)' \
		/dev/stdout

show-logs:		## shows logs of the deployed custom provider
	sam logs --name $(PROJECT_NAME)

deploy-demo: 		## deploys ./cloudformation/demo-stack.yaml to AWS
	aws cloudformation deploy \
		--stack-name $(PROJECT_NAME)-demo \
		--template-file cloudformation/demo-stack.yaml

delete-demo: 		## deletes ./cloudformation/demo-stack.yaml from AWS
	aws cloudformation delete-stack \
		--stack-name $(PROJECT_NAME)-demo
	aws cloudformation wait stack-delete-complete \
		--stack-name $(PROJECT_NAME)-demo

$(_TEMPLATE): template.yaml custom_provider/requirements.txt  custom_provider/*
	sam build --use-container
	find .aws-sam -type d -print0 | xargs -0 chmod go+rx
	find .aws-sam -type f -print0 | xargs -0 chmod go+r

Pipfile.lock: Pipfile */requirements.txt 
	pipenv install -d
	pipenv install -r */requirements.txt

