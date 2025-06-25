# 📌 Step Function States: Start & Stop EC2 Workflows

This is an overview of the **start** and **stop** lifecycle of EC2 instances across multiple environments (Development, Test, and Pre-Production).

📁 Related Documenation:
- [JSON Payload Reference](./JSON_payload.md) - Input/Output structures for Lambda state transitions
- [Lambda Function Details](./start_stop.md) - Implementation details of the main.py script
- [Email Notification Details](./sns.md) - Example formats of SNS-based email alerts
- [Jump to 🛑 Stop Steps](#-stop-workflow)

---
## ▶️ Start Workflow
![start arch](./img/parallel_start_arch.png)

### 1️⃣ Initial Parallel States
The workflow begins with a parallel state that simultaneously starts **Database EC2 instances** for:
- Development
- Test
- Pre-Production

Each Lambda state receives a payload like:
#### 📥 Input
```
json

{
  "phase_number": 3,
  "next_phase": true,
  "action": "start",
  "cw_log_phase": "starting development db servers",
  "send_mail": false
}
```

#### Payload Field Descriptions
| Field          | Type    | Description                                 |
| -------------- |---------|---------------------------------------------|
| `phase_number` | List    | Index of server group from `SERVER_LIST.py` |
| `next_phase`   | Boolean | Whether to start the DB servers             |
| `action`       | String  | `'start'`                                   |
| `cw_log_phase` | String  | CloudWatch log description                  |
| `send_mail`    | Boolean | Whether to notify SysAdmins                 |

#### 📤 Output
```
json

{
  "next_phase": true,
  "initial_state": {
    "test10": { "InstanceId": "i-0bad14933fffa49b9", "State": "stopped", "is_running": false },
    "test3":  { "InstanceId": "i-079d3e78afa290053", "State": "stopped", "is_running": false },
    "test9":  { "InstanceId": "i-082e1ef64192e11ad", "State": "stopped", "is_running": false }
  }
}
```

#### Output Field Descriptions
| Field          | Description     |
|----------------|--------------------------------------------------------|
| `next_phase`   | Indicates whether the application servers should start |
| `initial_state | The current status of EC2 instances fetched via `describe_instances` |

---
### 2️⃣ Choice State Logic
After the DB servers are started:

**IF** `next_phase` value:
- `true` → Proceed to start application servers (after a 10-minute wait)
- `false` (Default) → Skip application server start
   - A placeholder `initial_state` is generated to maintain workflow compatibility downstream. 

#### ⚠️Example When Skipping
```
json

{
  "dev_db_initial_state": "{% $states.input.initial_state %}",
  "dev_app_initial_state": { "empty": true }
}
```
---
### 3️⃣ Start Application Servers
Once the wait period completes:
- The workflow triggers a second Lambda function to start Application EC2 instances for each environment.
- It uses the previous Lambda output to determine success and capture instance state.

The results are aggregated to prepare the final email payload and provide context for validation.

#### Aggregation Example for Dev parallel
```
json
{
  "start_dev": "{% $states.result.Payload.next_phase %}",
  "dev_server_type": "application",
  "dev_db_initial_state": "{% $states.input.initial_state %}",
  "dev_app_initial_state": "{% $states.result.Payload.initial_state %}"
}

```

---
### 4️⃣ Final Choice Evaluation
The workflow evaluates success conditions:
- `start_*` **must all be** `true`
- `*_server_type` **must all be** `"application"`

---
### 📬 Notification
An email is sent via SNS with the status of the start operation:
- ✅ **START STATUS: SUCCESS** - if all evalutions are `true`
- ❌ **START STATUS: ABORTED (Default)** - if any conditions do not meet requirements

---
## 🛑 Stop Workflow
![start arch](./img/parallel_stop_arch.png)
### 1️⃣ Initial Parallel States
Similar to the start process, a parallel state is used to simultaneously stop **Application EC2 instances** for:
- Development
- Test
- Pre-Production

Each Lambda state receives a payload like:
#### 📥 Input
```
json

{
  "phase_number": 0,
  "next_phase": true,
  "action": "stop",
  "cw_log_phase": "stopping development app servers",
  "send_mail": false
}
```

#### Payload Field Descriptions
| Field          | Type    | Description                                 |
| -------------- |---------|---------------------------------------------|
| `phase_number` | List    | Index of server group from `SERVER_LIST.py` |
| `next_phase`   | Boolean | Whether to start the DB servers             |
| `action`       | String  | `'stop'`                                    |
| `cw_log_phase` | String  | CloudWatch log description                  |
| `send_mail`    | Boolean | Whether to notify SysAdmins                 |

#### 📤 Output
```
json

{
  "next_phase": true,
  "initial_state": {
    "test1": { "InstanceId": "i-0bad14933fffa49b9", "State": "running", "is_running": true },
    "test4":  { "InstanceId": "i-079d3e78afa290053", "State": "running", "is_running": true },
    "test19":  { "InstanceId": "i-082e1ef64192e11ad", "State": "running", "is_running": true }
  }
}
```
#### Output Field Descriptions
| Field          | Description     |
|----------------|--------------------------------------------------------|
| `next_phase`   | Indicates whether the database servers should stop |
| `initial_state | The current status of EC2 instances fetched via `describe_instances` |

---
### 2️⃣ Choice State Logic
After the App servers are stopped:

**IF** `next_phase` value:
- `true` → Proceed to stop database servers
- `false` (Default) → Skip database server stop
   - A placeholder `initial_state` is generated to maintain workflow compatibility downstream. 

---
### 3️⃣ Stop Database Servers
- The workflow triggers a second Lambda function to stop Database EC2 instances for each environment.
- It uses the previous Lambda output to determine success and capture instance state.

The results are aggregated to prepare the final email payload and provide context for validation.

#### Aggregation Example for Dev parallel
```
json
{
  "stop_dev": "{% $states.result.Payload.next_phase %}",
  "dev_server_type": "database",
  "dev_app_initial_state": "{% $states.input.initial_state %}",
  "dev_db_initial_state": "{% $states.result.Payload.initial_state %}"
}

```

---
### 4️⃣ Final Choice Evaluation
The workflow evaluates success conditions:
- `stop_*` **must all be** `true`
- `*_server_type` **must all be** `"database"`

---
### 📬 Notification
An email is sent via SNS with the status of the start operation:
- ✅ **SHUTDOWN STATUS: SUCCESS** - if all evalutions are `true`
- ❌ **SHUTDOWN STATUS: ABORTED (Default)** - if any conditions do not meet requirements

---
✅ Summary
This Step Function workflow provides a scalable, modular, and observable way to:

- Manage EC2 lifecycle operations across multiple environments

- Ensure dependency control (DBs before apps)

- Enable failure-safe workflows using Choice, Wait, and fallback logic

- Notify SysAdmins in real time via email
- 
[⬆️ Back to top](#%EF%B8%8F-start-workflow)
