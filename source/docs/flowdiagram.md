# <p align="center">**Automation Diagram**</p>

## **Start Up**

> 1. Scheduled **EventBridge** rule is triggered, e.g. every Monday at 0600 HRS
> 2. [AWS Step Function](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) kicks off a series of steps: 
>  - 2.1. **Lambda Function: Start Database EC2**
>    - 2.1.1. Get Instance State, Instance/System Status of **Master Server list**
>       - Valid EC2 State:
>          - **pending | running | shutting-down | terminated | stopping | stopped**
>       - Valid Instance/System Status:
>          - **ok | impaired | initializing | insufficient-data | not-applicable**
>    - 2.1.2. Write Instance State of each EC2 to CloudWatch Logs
>    - 2.1.3. Write Instances to be started to CloudWatch Logs
>    - 2.1.4. Start All Database Servers from *list* that are ***stopped***
>    - 2.1.5. Get Instance State of *list* to validate ***running*** state
>        - Continue 2.1.5 until Instance State is **NOT initializaing**
>        - If all instances are in a **running** state  and  Instace/System status **ok**: **pass** variable is returned
>        - If any instances are in a **stopped** state or Instace/System status not **ok**: **fail** variable is returned
>    - 2.1.6. Write Instance State and Instance/System Status of each EC2 to CloudWatch Logs
>    - 2.1.7. Trigger [AWS Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
>        - Send email notification to Org box
>        - Success or Failure will be indicated in the Subject line
>        - Message body contains Instance Name, Instance Id, Instace State, Instance Status, and System Status
- if **pass**: 
> - 2.2. Wait 10 mins (DB instances start up completion time)
> - 2.3. **Lambda Function: Start Application EC2**
>    - 2.3.1. Get Instance State, Instance/System Status of **Master Server list**
>       - Valid EC2 State:
>          - **pending | running | shutting-down | terminated | stopping | stopped**
>       - Valid Instance/System Status:
>          - **ok | impaired | initializing | insufficient-data | not-applicable**
>    - 2.3.2. Write Instance State of each EC2 within *Phase list* to CloudWatch Logs
>    - 2.3.3. Write Instances within *Phase list* to be started to CloudWatch Logs
>    - 2.3.4. Start Application Servers within *Phase list* that are ***stopped***
>    - 2.3.5. Get Instance State of *Phase list* to validate ***running*** state
>         - Continue 2.3.5. until Instance State is **NOT initializaing**
>         - If all instances are in a **running** state  and  Instace/System status **ok**: **pass** variable is returned
>         - If any instances are in a **stopped** state or Instace/System status not **ok**: **fail** variable is returned and process **ENDS START UP EXECUTION**
>     - 2.3.6. Write Instance State and Instance/System Status of each EC2 within *Phase list* to CloudWatch Logs
>     -  **Repeat** 2.3.2. - 2.3.6. until *Phase lists* are complete or **fail** variable from 2.3.5.
>     - 2.3.7. Trigger [AWS Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
>         - Send email notification to Org box
>         - Success or Failure will be indicated in the subject line on the email
>             - Failues will indicate the Phase that failed
>         - Message body contains Instance Name, Instance Id, Instace State, Instance Status, and System Status
> - 2.4 **Lambda Function: Enable CloudWatch Alarms**
>    - 2.4.1. Get CloudWatch Alarms: ActionsEnabled status
>       - Valid ActionsEnabled Status:
>         - **True | False**
>    - 2.4.2. Write CloudWatch Alarms: Name, ActionsEnabled Status to CloudWatch Logs
>    - 2.4.3. Enable CloudWatch Alarms where ***ActionsEnabled == False***
- if **fail**:
> NOTE: If 2.1.5 or 2.3.5 return **fail** variable, Lambda function stops any additional Phase Start ups and completes steps 2.1.7 or 2.3.7; depending on where the failure occurred. Step Functions will not continue to the next Step in the process.

| Phase | Environment | Server Type |
|-------|-------------|-------------|
| Phase 1 | Development, Test, Pre-Production | Database |
| Phase 2 | Development | Application |
| Phase 3 | Test | Application |
| Phase 4 | Pre-Production | Application |

[**Start EC2 Flow Diagram**](/source/images/lambda_startup_diagram.PNG)
<img src="/source/images/lambda_startup_diagram.PNG">

## **Shutdown**
| Phase | Environment | Server Type|
|-------|-------------|------------|
| Phase 1 | Development | Application |
| Phase 2 | Test | Application |
| Phase 3 | Pre-Production | Application |
| Phase 4 | Development | Database |
| Phase 5 | Test | Database |
| Phase 6 | Pre-Production | Database |

[**Stop EC2 Flow Diagram**](/source/images/lambda_startup_diagram1.PNG)
<img src="/source/images/lambda_shutdown_diagram1.png">
