# Step Function States
## Start
![start](./img/parallel_start_arch.png)
---
### Initial Parallel States
- Development DB Servers
- Test DB Servers
- Pre-Production DB Servers
---
- To start the process, each Lambda function state within the parallel state is given input information that the Lambda Handler expects as event data.
   As seen below:
   - **phase_number** - The index of the server list within start_stop.py
   - **next_phase** - The boolean value (true/false) whether to execute the main function
   - **action** - Either "start" or "stop". Corresponds to the Lambda function logic to either execute the Boto3 method ***start_instances*** or ***stop_instances*** for EC2 instances
   - **cw_log_phase** - Used for posting to CloudWatch to show what execution step is being accomplished
   - **send_mail** - The boolean value whether to send the email notification to Sys Admins 
  
```
Example JSON Payload Input:

{
"phase_number": 3,
"next_phase": true,
"action": "start",
"cw_log_phase": "starting development db servers",
"send_mail": false
}
```
    
  - Upon completion of the Lambda functions, they return JSON data back to the Step Function to assist with next step logic
    
 ```
 Example Output From Lambda:
 
  {
    "next_phase": true,
    "initial_state": {
      "test10": {
      "InstanceId": "i-0bad14933fffa49b9",
      "State": "stopped",
      "is_running": false
      },
      "test3": {
      "InstanceId": "i-079d3e78afa290053",
      "State": "stopped",
      "is_running": false
      },
      "test9": {
      "InstanceId": "i-082e1ef64192e11ad",
      "State": "stopped",
      "is_running": false
      }
    }
  }
  ```
   - **next_phase** - The boolean value (true/false) whether to proceed starting the corresponding Application servers
   - **initial_state** - The initial state is the processed description of each EC2 within a given server list. This uses the Boto3 method ***describe_instances*** for EC2 instances
---
### Choice
3. The next step in the process is to determine whether or not to proceed starting Application servers within its parallel state
   - Utilizing the **next_phase** output from the previous Lambda Function, the ***Choice*** state will use the following logic:
     - IF **$states.input.next_phase == true**, proceed to start the Application servers
     - DEFAULT is to pass the output data if **$states.input.next_phase != true**, and do not start the next phase
---    
### **$states.input.next_phase == true**
4. If **$states.input.next_phase == true**, the state machine will proceed to the next Lambda function for execution
   - This will follow the same process as the DB start with the initial JSON payload as event data
   - Upon completion of the Lambda 
---
### DEFAULT ($states.input.next_phase != true)

```
Example of the DEV DB function passing "next_phase" == false

{
"dev_db_initial_state": "{% $states.input.initial_state %}",
"dev_app_initial_state": { "empty": true }
}

```
