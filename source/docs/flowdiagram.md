# <p align="center">**Automation Diagram**</p>
## **Start Up**

1. Scheduled **EventBridge** rule is triggered
   - EventBridge rule executes according to designated CRON job.

   > NOTE: Event schedules are listed in Universal Time Coordinated(UTC). This can be changed to Local time zone, via drop down option, for easier readability.

2. [AWS Step Function](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) kicks off a series of steps: 
   - 2.1. **Lambda Function: Start Database EC2**
     - 2.1.1. Get Instance State, Instance/System Status of **Master Server list**
       - Valid EC2 State:
         - **pending | running | shutting-down | terminated | stopping | stopped**
       - Valid Instance/System Status:
        - **ok | impaired | initializing | insufficient-data | not-applicable**
     - 2.1.2. Write Instance State of each EC2 to CloudWatch Logs
     - 2.1.3. Write Instances to be started to CloudWatch Logs
     - 2.1.4. Start All Database Servers from *list* that are ***stopped***
     - 2.1.5. Get Instance State of *list* to validate ***running*** state
       - 2.1.5 continues until all Instance States are **NOT initializaing**
       - If all instances are in a **running** state  and  Instace/System status **ok**: **pass** variable is returned
       - If any instances are in a **stopped** state or Instace/System status not **ok**: **fail** variable is returned
     - 2.1.6. Write Instance State and Instance/System Status of each EC2 to CloudWatch Logs
     - 2.1.7. Trigger [AWS Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
       - Send email notification to Org box
       - Success or Failure will be indicated in the Subject line
       - Message body contains Instance Name, Instance Id, Instace State, Instance Status, and System Status
      
     > NOTE: If 2.1.5 returns **fail** variable, the Lambda function will complete the remaining steps within that function. The additional steps within the Step Function will not be executed. System Administrators will need to intervene to find the root cause.
      
- if **pass**: 
  - 2.2. Wait 10 mins (DB instances start up completion time)
  - 2.3. **Lambda Function: Start Application EC2**
    - 2.3.1. Get Instance State, Instance/System Status of **Master Server list**
      - Valid EC2 State:
        - **pending | running | shutting-down | terminated | stopping | stopped**
      - Valid Instance/System Status:
        - **ok | impaired | initializing | insufficient-data | not-applicable**
    - 2.3.2. Write Instance State of each EC2 within *Phase list* to CloudWatch Logs
    - 2.3.3. Write Instances within *Phase list* to be started to CloudWatch Logs
    - 2.3.4. Start Application Servers within *Phase list* that are ***stopped***
    - 2.3.5. Get Instance State of *Phase list* to validate ***running*** state
      - 2.3.5. continues until all Instance States are **NOT initializaing**
      - If all instances are in a **running** state  and  Instace/System status **ok**: **pass** variable is returned
      - If any instances are in a **stopped** state or Instace/System status not **ok**: **fail** variable is returned and process **ENDS START UP EXECUTION**
    - 2.3.6. Write Instance State and Instance/System Status of each EC2 within *Phase list* to CloudWatch Logs
    - 2.3.7. Trigger [AWS Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
      - Send email notification to Org box
      - Success or Failure will be indicated in the subject line on the email
      - Failues will indicate the Phase that failed
      - Message body contains Instance Name, Instance Id, Instace State, Instance Status, and System Status

    > NOTE: If 2.3.5 returns **fail** variable, the Lambda function will not execute any additional Start up phases. It will continue to steps 2.3.6 and 2.3.7. The additional steps within the Step Function will not be executed. System Administrators will need to intervene to find the root cause.

  - 2.4 **Lambda Function: Enable CloudWatch Alarms**
    - 2.4.1. Get CloudWatch Alarms: ActionsEnabled status
      - Valid ActionsEnabled Status:
        - **True | False**
    - 2.4.2. Write CloudWatch Alarms: Name, ActionsEnabled Status to CloudWatch Logs
    - 2.4.3. Enable CloudWatch Alarms where ***ActionsEnabled == False***

| Phase | Environment | Server Type |
|-------|-------------|-------------|
| Phase 1 | Development, Test, Pre-Production | Database |
| Phase 2 | Development | Application |
| Phase 3 | Test | Application |
| Phase 4 | Pre-Production | Application |

[**Start EC2 Flow Diagram**](/source/images/lambda_startup_diagram.PNG)
<img src="/source/images/lambda_startup_diagram.PNG">

> NOTE: The **GREEN** outlines within the diagram. Each service (EventBridge, Step Function, and Lambda) references the IAM role to receive permissions to execute; [sts:AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html). This Role has specific policies to execute each function according to [Amazon Resource Names (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html). This allows fine-grained permissions to only resources that are listed within the attached policy.

## **Shutdown**

1. Scheduled **EventBridge** rule is triggered
   - EventBridge rule executes according to designated CRON job.

   > NOTE: Event schedules are listed in Universal Time Coordinated(UTC). This can be changed to Local time zone, via drop down option, for easier readability.

2. **Lambda Function: Phase Shutdown EC2**:
   - 2.1. Disable All CloudWatch Alarms for EC2 Instances
     - 2.1.1. All AlarmNames are contained in a Python list
   - 2.2. Get Instance State of **Master Server list**
     - Valid EC2 State:
       - **pending | running | shutting-down | terminated | stopping | stopped**
   - 2.3. Write Instance State of each EC2 within *Phase list* to CloudWatch Logs
   - 2.4. Write Instances within *Phase list* to be stopped to CloudWatch Logs
   - 2.5. Stop Application Servers within *Phase list* that are ***running***

   > NOTE: Phases are listed in the Table below.

   - 2.6. Get Instance State of *Phase list* to validate ***stopped*** state
     - 2.6. continues until all Instance States are **NOT initializaing**
     - If all instances are in a **stopped** state: **pass** variable is returned
     - If any instances are in a **running** state: **fail** variable is returned and process **ENDS SHUTDOWN EXECUTION**
   - 2.7. Write Instance State of each EC2 within *Phase list* to CloudWatch Logs
   - 2.8. Trigger [AWS Simple Notification Service (SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
     - Send email notification to Org box
     - Success or Failure will be indicated in the subject line on the email
     - Failues will indicate the Phase that failed
     - Message body contains Instance Name, Instance Id, and Instace State

   > NOTE: If any of the Phases fail to stop **ALL** servers within that Phase, the remaining phases **WILL NOT EXECUTE**. System Administrators will need to intervene to find the root cause. 

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

> NOTE: The **GREEN** outlines within the diagram. Each service (EventBridge and Lambda) references the IAM role to receive permissions to execute; [sts:AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html). This Role has specific policies to execute each function according to [Amazon Resource Names (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html). This allows fine-grained permissions to only resources that are listed within the attached policy.
