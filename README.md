# 🥅 AWS EC2 Start & Stop Automation

This project was developed to meet customer requirements for automating the start and stop processes of servers. It implements parallel execution to start or stop multiple environments simultaneously. If one environment fails during the process, built-in logic ensures that the corresponding parallel state halts without impacting the remaining environments. This design guarantees fault isolation—allowing failures in individual environments to be handled gracefully without affecting the overall operation.

This process uses the following AWS Services:
- 🕐 [Amazon EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html) - to schedule when startups and shutdowns will occur
- 🧠[AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) - to orchestrate Lambda functions to execute start/stop functions
- 💻[AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) - the main function that will start/stop EC2 instances, disable associated CloudWatch alarms, and send SNS emails about the end state of the Step Function execution
- 📬[Amazon CloudWatch Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) - the service to send notification emails 
- 📖[AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - the SDK utilized to script the lambda_function.py and start_stop.py
- ☁️[A]

## Table of Contents:
- 🧠[Step Function States](./docs/step_function_steps.md)
- 📃[State Machine JSON code](./docs/state_machine.md)
- 💻[Lambda Start_Stop Logic](./docs/start_stop.md)
- 💻[Lambda Start_Stop Code Breakdown](./docs/start_stop_code.md)
- 📃[JSON Payload for Step Functions](./docs/JSON_payload.md)
- ✔️[Example State Machine Execution](./docs/state_machine_execution.md)
- ☁️[Example CloudWatch Logs](./docs/cloudwatch.md)
- 📧[Example Email from SNS](./docs/sns.md)

## Step Function Diagram
![Stop State Machine](./docs/img/parallel_stop_arch.png)
![Start State Machine](./docs/img/parallel_start_arch.png)
