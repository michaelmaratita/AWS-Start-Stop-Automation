# Code Breakdown

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

### 📁 Related Files
- `start_stop/aws/cloudwatch/log_handler.py`: Handles log formatting/output
- `start_stop/aws/cloudwatch/alarm_handler.py`: Enables/disables CloudWatch alarms
- `SERVER_LIST.py`: Defines instance groups by environment
- `main.py`: Entry point Lambda logic for Step Functions
