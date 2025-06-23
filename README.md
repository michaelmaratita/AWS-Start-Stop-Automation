# 🎯 AWS EC2 Start & Stop Automation

This project was accomplished to meet customer needs to automate starting and stopping servers. 

This process uses the following:
- 🕐 [AWS EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html) - to schedule when startups and shutdowns will occur
- 🧠[AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) - to orchestrate Lambda functions to execute start/stop functions
- 📃[AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) - the main function that will start/stop EC2 instances, disable associated CloudWatch alarms, and send SNS emails about the end state of the Step Function execution
- 📬[AWS Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) - the service to send notification emails 
- 📖[AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - the SDK utilized to script the lambda_function.py and start_stop.py

## Table of Contents:
- [JSON Payload for step functions](./docs/JSON_payload.md)

## Step Function Diagram
![Stop State Machine](./docs/img/parallel_stop_arch.png)
![Start State Machine](./docs/img/parallel_start_arch.png)
