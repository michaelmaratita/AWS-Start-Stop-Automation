# Start/Stop Code Breakdown

## Table of Contents:
- [Lambda Handler and Main](./start_stop.md)
- [📬 `sns_handler.py](#-sns_handlerpy)

## `ec2_handler.py`
## ☁️`class EC2Instance` - EC2 Lifecycle Management via AWS SDK (Boto3)

This module provides a reusable interface for starting, stopping, and validating the state of EC2 instances using AWS Step Functions and Lambda. It also integrates with CloudWatch logging and alarm management.

### 📦 Module Dependencies
- `boto3`: AWS SDK for Python
- `Logger`: Custom CloudWatch log handler
- `AlarmManager`: Manages CloudWatch alarms
- server_lists: Returns server name groups by phase/environment
- time.sleep: Used during re-check instance states

### 🔧 `__init__(self, names)`

Initializes an `EC2Instance` object with a list of EC2 instance **Name tags**.
```python
python

instance = EC2Instance(['web-server-dev', 'db-server-dev'])
```

### 🔍 `describe(self)`
Fetches instance metadata using the describe_instances API. It filters by the Name tag and returns a dictionary keyed by instance name.

#### Output Structure
```python
python

{
  "web-server-dev": {
    "InstanceId": "i-xxxx",
    "State": "running",
    "is_running": True
  }
}
```

### 🔁 `start_or_stop(self, action)`
Dispatches to either `_start()` or `_stop()` based on the `action` string (`'start'` or `'stop'`).

### ▶️ `_start(self, action)`
- Filters out already running instances.
- Starts stopped instances using `start_instances()`.
- Enables CloudWatch alarms via `AlarmManager`.
Also logs:
- Current instance state
- Action taken

### ⏹️ `_stop(self, action)`
- Filters out already stopped instances.
- Disables CloudWatch alarms.
- Stops running instances using `stop_instances()`.
Also logs:
- Current instance state
- Action taken

### ✅ `validation(self, num, action, sleep_val=15)`
Recursive method that:
- Waits up to 5 cycles for all instances to reach expected state (running or stopped)
- Pauses sleep_val seconds between checks
- Aborts if instances don't reach the expected state in time
- Logs validation progress and failures.

### ✅ `validate_status(self, num, action, sleep_val=15)`
Builds on validation() and:
- Waits an additional 45 seconds
- Uses `describe_instance_status()` to validate instance health checks
  - `InstanceStatus`
  - `SystemStatus`
- Retry validations up to 6 times

### 🧪 `validation_dict(self)`
Returns a merged dictionary combining:
- `describe_instances` data
- `describe_instance_status` data
Used for detailed post-action validation.

#### ⚠️Example 
```python
python

{
  "web-server-dev": {
    "InstanceId": "i-xxxx",
    "State": "running",
    "is_running": True,
    "InstanceStatus": "passed",
    "SystemStatus": "passed"
  }
}
```

### 📜 `instance_log_status(self, passed, action)`
Logs:
- A summary message (success or fail)
- Detailed instance status report using Logger
Used at the end of main() Lambda logic to summarize outcome.

### 📦 `get_end_state(subject: str)`
Static method that:
- Iterates over all server groups
- Returns:
  - `describe()` results for shutdown workflows
  - `validation_dict()` results for startup workflows
Useful for Step Function final payloads (e.g., email or output states).

### 🧠 Design Considerations
- 💪 **Resilient Validation**: Includes retry loops and recursive checks for reliable automation.
- 📝 **Logging Integration**: Uses Logger throughout for visibility via CloudWatch.
- 📢 **Alarm Handling**: Enables/disables CloudWatch alarms to avoid false positives.
- 🔀 **Extensible**: Supports multi-environment (Dev/Test/PreProd) orchestration.

### 📁 Related Files
- `start_stop/aws/cloudwatch/log_handler.py`: Handles log formatting/output
- `start_stop/aws/cloudwatch/alarm_handler.py`: Enables/disables CloudWatch alarms
- `SERVER_LIST.py`: Defines instance groups by environment
- `main.py`: Entry point Lambda logic for Step Functions

---
## `sns_handler.py`
## 📬 `class SNSHandler` - Automated EC2 State Email Notifications via SNS

This module handles email notifications via AWS SNS as part of an EC2 instance orchestration workflow. It builds dynamic email content based on the instance lifecycle status (start/stop) and sends alerts to administrators.

### 📦 Dependencies
- `boto3`: AWS SDK for SNS operations.
- `Logger`: Custom CloudWatch logging formatter.
- `EC2Instance`: EC2 state retriever (used for end-state snapshots).
- `server_lists`, `environments`: Define grouped instance lists and their phase (e.g., Dev, Test, PreProd).

### 🔧 `__init__(self, data)`
Initializes the handler using output from the Step Function.

#### Parameters:
- `data`: Dict payload passed from Step Functions, includes:
- `subject`: The email subject line (e.g., `START STATUS: SUCCESS`)
- `dev_db_initial_state`, `dev_app_initial_state`, etc.

#### Logic:
- Stores instance data in `self.initial`
- Extracts phases from `environments()`

### 🔑 `get_topic(self)`
Dynamically finds the SNS topic ARN that includes `"mailme"` in its name.

> 🔍 This avoids hardcoding ARNs, which makes the code environment-agnostic.

### 📤 `send_mail(self)`
Publishes a message to the SNS topic with:
- The generated message body (`format_body()`)
- A capitalized subject line
Used at the final step of a Step Function state machine.

### 🧱 `format_body(self)`
Builds the full email message body, combining:
1. A greeting and subject line
2. Initial state output (format_initial_state)
3. End state output (format_end_state)
4. Optional abort message via Logger.log_abort()

### 🟡 `format_initial_state(self)`
Loops through the initial EC2 state data (`self.initial`) grouped by phase, and uses `Logger.log_ec2_state()` to format each instance’s state (running/stopped).

```
text

SHUTDOWN STATUS: SUCCESS
------------------------
INITIAL STATE:

DEV APP SERVERS
--------------------------
test1 is in a running state
....
```

### 🔴 `format_end_state(self)`
Shows post-action instance health using:
- `EC2Instance.get_end_state()`: Fetches current EC2 state after action
- `Logger.log_status()`: Formats output for each instance

Also includes a summary header from Logger.intro().

```
text

------------------------
All Server have successfully stopped

DEV APP SERVERS
------------------------
test1 is in a stopped state
...
```

### ⚙️ `get_verb(self)`
Parses the email subject to determine:
- **Action**: `start` or `stop`
- **State**: `success` or `fail`
Used to customize log summaries and alert content.

### 🧠 Design Considerations
- ✅ **Flexible Topic Matching**: Finds SNS topic dynamically via name match
- 📋 **Readable Logs**: Uses Logger to ensure log format consistency
- 📣 **Environment-Aware**: Includes environment names (Dev/Test/PreProd) for easier identification
- 🔁 **Reusable Output**: Pairs with Step Functions to automate entire lifecycle and reporting

### 📁 Related Files
- `start_stop/aws/cloudwatch/log_handler.py` – Formats instance output
- `start_stop/aws/ec2_handler.py` – Manages EC2 start/stop logic
- `SERVER_LIST.py` – Lists instance groups by environment/phase


