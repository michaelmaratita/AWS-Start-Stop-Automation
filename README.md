# AWS EC2 Start & Stop Automation

- This process was established to meet customer demands for a phased approach to start and stop Amazon EC2 instances. The reasoning for the phased approach is to ensure EC2 instances are started or stopped in the correct order. If any of the phases fail, the lambda function will not proceed to the following phases. The purpose is to save costs when EC2 instances are not in use. 

- These processes leverage the use of [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), [AWS EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html) and [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to perform the automated start-ups and shutdowns of the EC2 instances. Within this repository, you will find the Python code for the lambda functions, as well as configuration checklists for utilizing this solution.

## Table of Contents
- [How It Works](/source/docs/flowdiagram.md)
  - [Start Up](/source/docs/flowdiagram.md#start-up)
    - [Start Up Diagram](/source/images/lambda_startup_diagram.PNG)
  - [Shutdown](/source/docs/flowdiagram.md#shutdown)
    - [Shutdown Diagram](/source/images/lambda_shutdown_diagram1.png) 
- [Lambda Function Code Breakdown]()

## Configurations

[<img align="center" src="/source/images/logos/CW_logo.PNG" width=4% height=4%>](how_to/cloudwatch/cw_config.md) 
[**CloudWatch**](how_to/cloudwatch/cw_config.md)

[<img align="center" src="/source/images/logos/eventbridge_logo.PNG" width=4% height=4%>](how_to/eventbridge/eventbridge_config.md) 
[**EventBridge**](how_to/eventbridge/eventbridge_config.md)

[<img align="center" src="/source/images/logos/IAM_logo.PNG" width=4% height=4%>](how_to/iam/iam_config.md)
[**IAM**](how_to/iam/iam_config.md)

[<img align="center" src="/source/images/logos/lambda_logo.PNG" width=4% height=4%>](how_to/lambda/lambda_config.md)
[**Lambda**](how_to/lambda/lambda_config.md)

[<img align="center" src="/source/images/logos/SNS_logo.PNG" width=4% height=4%>](how_to/sns/sns_config.md)
[**SNS**](how_to/sns/sns_config.md)

[<img align="center" src="/source/images/logos/Step_Functions_Logo.PNG" width=4% height=4%>](how_to/step_functions/step_functions_config.md)
[**Step Functions**](how_to/step_functions/step_functions_config.md)

## More Resources
- [Boto3](https://github.com/boto/boto3#readme)
- [License](LICENSE)
