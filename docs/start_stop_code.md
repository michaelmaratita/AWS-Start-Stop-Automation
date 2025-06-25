# Start/Stop Code Breakdown

## Table of Contents:
- [🚦 `lambda_function.py` and `main.py`](./start_stop.md)
- [📬 `sns_handler.py`](#sns_handlerpy)
- [🔔 `alarm_handler.py`](#alarm_handlerpy)
- [📝 `log_handler.py`](#log_handlerpy)

## `ec2_handler.py`
## 💻`class EC2Instance` - EC2 Lifecycle Management via AWS SDK (Boto3)

[link to code](../python/start_stop/aws/ec2_handler.py)

This module provides a reusable interface for starting, stopping, and validating the state of EC2 instances using AWS Step Functions and Lambda. It also integrates with CloudWatch logging and alarm management.

### 📦 Module Dependencies
- `boto3.client('ec2')`: AWS SDK client to interact with EC2 Instances.
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

### 📌 Design Considerations
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
## Table of Contents:
- [🚦 `lambda_function.py` and `main.py`](./start_stop.md)
- [💻 `ec2_handler.py`](#ec2_handlerpy)
- [🔔 `alarm_handler.py`](#alarm_handlerpy)
- [📝 `log_handler.py`](#log_handlerpy)
## 📬 `class SNSHandler` - Automated EC2 State Email Notifications via SNS

[link to code](../python/start_stop/aws/sns_handler.py)

This module handles email notifications via AWS SNS as part of an EC2 instance orchestration workflow. It builds dynamic email content based on the instance lifecycle status (start/stop) and sends alerts to administrators.

### 📦 Dependencies
- `boto3.client('sns')`: AWS SDK client for SNS operations.
- `Logger`: Used to format email notifications.
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

### 📌 Design Considerations
- ✅ **Flexible Topic Matching**: Finds SNS topic dynamically via name match
- 📋 **Readable Logs**: Uses Logger to ensure log format consistency
- 📣 **Environment-Aware**: Includes environment names (Dev/Test/PreProd) for easier identification
- ♻️ **Reusable Output**: Pairs with Step Functions to automate entire lifecycle and reporting

### 📁 Related Files
- `start_stop/aws/cloudwatch/log_handler.py` – Formats instance output
- `start_stop/aws/ec2_handler.py` – Used to get end state information
- `SERVER_LIST.py` – Defines instance groups by environment

---
## `alarm_handler.py`
## Table of Contents:
- [🚦 `lambda_function.py` and `main.py`](./start_stop.md)
- [💻 `ec2_handler.py`](#ec2_handlerpy) 
- [📬 `sns_handler.py`](#sns_handlerpy)
- [📝 `log_handler.py`](#log_handlerpy)
## 🔔 `class AlarmManager` - CloudWatch Alarm Controller

[link to code](../python/start_stop/aws/cloudwatch/alarm_handler.py)

This class manages CloudWatch alarm states for EC2 instances during start/stop workflows. It dynamically enables or disables alarms based on instance names passed in via the Lambda/Step Function execution.

### 📦 Dependencies
- `boto3.client('cloudwatch')` - AWS SDK client to interact with CloudWatch alarms.

### 🔧 `__init__(self, names)`

Initializes the manager with a list of instance name strings that will be matched against CloudWatch alarm names.

#### Parameters:
- `names`: List[str] — from SERVER_LIST[event['phase_number']]

### 🔍 `get_alarm_names(self)`

Fetches all CloudWatch alarms, filters them to include only those whose names partially match the instance names provided.

#### Returns:
- `List[str]`: Filtered list of alarm names to be updated.

#### Logic:
```python
python

a['AlarmName'] for a in alarms
if any(name in a['AlarmName'] for name in self.alarm_names)
```
This allows for flexible partial matches, e.g., `"web-dev"` in `"web-dev-cpu-util"`

### 🚫 `disable_alarms(self)`

Disables all alarm actions (e.g., InstanceStatus failure, High CPU Utilization, etc.) for matching CloudWatch alarms.

#### Steps:
1. Call `get_alarm_names()` to get relevant alarms.
2. Log each one being disabled.
3. Use `client.disable_alarm_actions()` to update AWS.

Use Case:
Called **before stopping** EC2 instances to prevent false positive alerts (e.g., CPU alarm triggering during shutdown).

### ✅ enable_alarms(self)

Re-enables previously disabled alarm actions for matching alarms.

#### Steps:
1. Call get_alarm_names().
2. Log each one being enabled.
3. Use client.enable_alarm_actions() to re-activate them.

Use Case:
Called **after starting** EC2 instances to resume normal monitoring.

### 📌 Design Considerations
- ✅ **Partial Matching** - No hardcoded alarm names
- ➖ **Logic Separation** - Alarm control isolated from EC2 logic
- 📋 **Logging** - Provides easy traceability for audit/debugging
- ♻️ **Reusable** - Works with any resource-alarm convention where names align

### 📂 Related Modules
- `EC2Instance (ec2_handler.py)` — calls `AlarmManager` within `_start()` and `_stop()`.
- `SERVER_LIST.py` — source of EC2 tag names passed into this manager.

---
## `log_handler.py`
## Table of Contents:
- [🚦 `lambda_function.py` and `main.py`](./start_stop.md)
- [💻 `ec2_handler.py`](#ec2_handlerpy) 
- [📬 `sns_handler.py`](#sns_handlerpy)
- [🔔 `alarm_handler.py`](#alarm_handlerpy)
## 📝 `class Logger` - EC2 Lifecyle Logging and SNS Formatting Utility

[link to code](../python/start_stop/aws/cloudwatch/log_handler.py)

The `Logger` class is a stateless utility providing consistent logging for EC2 start/stop workflows. It enhances visibility into what's happening at each step and is especially helpful for debugging state transitions in Step Functions or Lambda executions.

This is a static-only utility class — no instantiation required. Every method is decorated with @staticmethod, meaning you call it like Logger.log_action(...) instead of creating a Logger() object.

### `log_action(instances, list, action)`
Logs (prints) which EC2 instances are being started or stopped.
- `instances`: Dictionary with instance metadata.
- `list`: List of instance IDs being operated on.
- `action`: `"start"` or `"stop"`

```
Starting: test1 (i-xxxxx)
...
...
Stopping: test1 (i-xxxxx)
```

### `log_abort(instance_list, action)`
Logs a failure to complete a full start/stop operation.
- `instance_list`: List of EC2 instance names or objects.
- `action`: `"start"` or `"stop"`.
**Returns**: A string message (not printed).

```
Not all servers have been started...ABORTING STARTUPS.
Please validate server states in AWS Console.
['test1', 'test2']
```

### `log_validation(instance_list)`
Logs (prints) a message when validation checks begin.
```
Validating servers state: ['test1', 'test2']
```

### `log_intance_state(meta, i)`
Logs the current state of a specific instance.
- `meta`: Dictionary of instance metadata.
- `i`: Name key (e.g., 'test1').
**Returns**: A string message (not printed).

```
Server: test1 (i-xxxxxx) is running
...
...
Server: test1 (i-xxxxxx) is stopped
```

### `log_max_validations(dictionary)`
Called when the validation retry limit has been reached.
- `dictionary`: Final state/status dict.
```
Please check the Instance Status and Systems Status for the following servers:

{ ...detailed instance dict... }
```

### `intro(action, state)`
Prints the summary result of an action:
- `action`: `"start"` or `"stop"`
- state: `"success"` or `"fail"`
```
All servers have been successfully started.
```
or
```
Failed to stop all servers
```

### `log_status(dictionary, action)`
Top-level formatter for EC2 state summaries.
- If `action == 'start'`: Calls `format_log_status_start()`.
- If `action == 'stop'`: Calls `format_state_log()`.

### `format_log_status_start(dictionary)`
Formats full start logs including instance and system health checks.
```
test1 is in a running state.
test1 (i-xxxxxx): Instance Status: passed | System Status: passed
```

### `format_start_log(dictionary, i)`
Called by `format_log_status_start`. Generates formatted instance + system status strings.
**Returns**
Tuple of:
- Instance status log (string) `Instance Status: passed`
- System status log (string)   `System Status: passed`

### `format_state_log(dictionary, i)`
Returns a one-liner state summary for an instance.
```
test1 is in a stopped state
```

### 🧠 Design Rationale
- **@staticmethod**	- enables global access
- **Return vs. Print** - Returns strings that can be used for both CloudWatch and SNS/email usage, prints for CloudWatch only

### 📁 Related Components
- `EC2Instance`: Calls most `Logger` methods during start/stop.
- `SNSHandler`: Uses `Logger.log_abort()` and `Logger.log_status()` for email body.

[back to ⬆️](#startstop-code-breakdown)
