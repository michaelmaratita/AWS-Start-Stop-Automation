# JSON Payload Information For Step Function Input/Output

## Development App Servers:
### JSON Payload Format
```JSON
{
  "phase_number": 0,
  "next_phase": SEE INPUT,
  "action": SEE INPUT,
  "cw_log_phase": SEE INPUT,
  "send_mail": false
}
```
### Input:
```JSON
START Inputs:
"next_phase": "next_phase.$",
"action": "start",
"cw_log_phase": "starting development app servers"

STOP Inputs:
"next_phase": true,
"action": "stop",
"cw_log_phase": "stopping development app servers"
```

### Output:
```JSON
START Outputs:
{
  "start_dev": "{% $states.result.Payload.next_phase %}",
  "dev_server_type": "application",
  "dev_db_initial_state": "{% $states.input.initial_state %}",
  "dev_app_initial_state": "{% $states.result.Payload.initial_state %}"
}
```

## Test App Servers:
### JSON Payload Format
```JSON
{
  "phase_number": 1,
  "next_phase": SEE INPUT,
  "action": SEE INPUT,
  "cw_log_phase": SEE INPUT,
  "send_mail": false
}
```
### Input:
```JSON
START Inputs:
"next_phase": "next_phase.$",
"action": "start",
"cw_log_phase": "starting test app servers"

STOP Inputs:
"next_phase": true,
"action": "stop",
"cw_log_phase": "stopping test app servers"
```

### Output:
```JSON
START Outputs:
{
  "start_test": "{% $states.result.Payload.next_phase %}",
  "test_server_type": "application",
  "test_db_initial_state": "{% $states.input.initial_state %}",
  "test_app_initial_state": "{% $states.result.Payload.initial_state %}"
}
```

## Pre-Production App Servers:
### JSON Payload Format
```JSON
{
  "phase_number": 2,
  "next_phase": SEE INPUT,
  "action": SEE INPUT,
  "cw_log_phase": SEE INPUT,
  "send_mail": false
}
```
### Input:
```JSON
START Inputs:
"next_phase": "next_phase.$",
"action": "start",
"cw_log_phase": "starting preprod app servers"

STOP Inputs:
"next_phase": true,
"action": "stop",
"cw_log_phase": "stopping preprod app servers"
```

### Output:
```JSON
START Outputs:
{
  "start_preprod": "{% $states.result.Payload.next_phase %}",
  "preprod_server_type": "application",
  "preprod_db_initial_state": "{% $states.input.initial_state %}",
  "preprod_app_initial_state": "{% $states.result.Payload.initial_state %}"
}
```

## Development DB Servers:
### JSON Payload Format
```JSON
{
  "phase_number": 3,
  "next_phase": SEE INPUT,
  "action": SEE INPUT,
  "cw_log_phase": SEE INPUT,
  "send_mail": false
}
```
### Input:
```JSON
START Inputs:
"next_phase": true,
"action": "start",
"cw_log_phase": "starting development db servers"

STOP Inputs:
"next_phase": "next_phase.$",
"action": "stop",
"cw_log_phase": "stopping development db servers"
```

### Output:
```JSON
STOP Outputs:
{
  "stop_dev": "{% $states.result.Payload.next_phase %}",
  "dev_server_type": "database",
  "dev_db_initial_state": "{% $states.result.Payload.initial_state %}",
  "dev_app_initial_state": "{% $states.input.initial_state %}"
}
```

## Test DB Servers:
### JSON Payload Format
```JSON
{
  "phase_number": 4,
  "next_phase": SEE INPUT,
  "action": SEE INPUT,
  "cw_log_phase": SEE INPUT,
  "send_mail": false
}
```
### Input:
```JSON
START Inputs:
"next_phase": true,
"action": "start",
"cw_log_phase": "starting test db servers"

STOP Inputs:
"next_phase": "next_phase.$"
"action": "stop",
"cw_log_phase": "stopping test db servers"
```

### Output:
```JSON
STOP Outputs:
{
  "stop_test": "{% $states.result.Payload.next_phase %}",
  "test_server_type": "database",
  "test_db_initial_state": "{% $states.result.Payload.initial_state %}",
  "test_app_initial_state": "{% $states.input.initial_state %}"
}
```

## Pre-Production DB Servers:
### JSON Payload Format
```JSON
{
  "phase_number": 5,
  "next_phase": SEE INPUT,
  "action": SEE INPUT,
  "cw_log_phase": SEE INPUT,
  "send_mail": false
}
```
### Input:
```JSON
START Inputs:
"next_phase": true,
"action": "start",
"cw_log_phase": "starting preprod db servers"

STOP Inputs:
"next_phase": "next_phase.$",
"action": "stop",
"cw_log_phase": "stopping preprod db servers"
```

### Output:
```JSON
STOP Outputs:
{
  "stop_preprod": "{% $states.result.Payload.next_phase %}",
  "preprod_server_type": "database",
  "preprod_db_initial_state": "{% $states.result.Payload.initial_state %}",
  "preprod_app_initial_state": "{% $states.input.initial_state %}"
}
```

## Send EMAIL State:
### Format:
```JSON

{
  "send_mail": true,
  "subject": SEE INPUT --->,
  "dap_state": "{% $states.input.dev_app_initial_state %}",
  "tap_state": "{% $states.input.test_app_initial_state %}",
  "pap_state": "{% $states.input.preprod_app_initial_state %}",
  "ddb_state": "{% $states.input.dev_db_initial_state %}",
  "tdb_state": "{% $states.input.test_db_initial_state %}",
  "pdb_state": "{% $states.input.preprod_db_initial_state %}"
}
```

### Start:
```JSON
START SUCCESS:
"subject": "START STATUS: SUCCESS"

SUCCESS IF THESE CONDITIONS ARE TRUE:
"(($states.input.start_dev) = (true)" and
"($states.input.dev_server_type) = ('application')" and
"($states.input.start_test) = (true)" and
"($states.input.test_server_type) = ('application')" and
"($states.input.start_preprod) = (true)" and
"($states.input.preprod_server_type) = ('application'))"

START FAIL (DEFAULT RULE):
"subject": "START STATUS: ABORTED"

```
### Stop:
```JSON
STOP SUCCESS:
"subject": "SHUTDOWN STATUS: SUCCESS"

SUCCESS IF THESE CONDITIONS ARE TRUE:
"(($states.input.start_dev) = (true)" and
"($states.input.dev_server_type) = ('database')" and
"($states.input.start_test) = (true)" and
"($states.input.test_server_type) = ('database')" and
"($states.input.start_preprod) = (true)" and
"($states.input.preprod_server_type) = ('database'))"

STOP FAIL (DEFAULT RULE):
"subject": "SHUTDOWN STATUS: ABORTED"

```

## DEFAULT Choice Rules:
### Dev App Stop
```JSON
{
  "dev_app_initial_state": "{% $states.input.initial_state %}",
  "dev_db_initial_state": {
    "empty": true
  }
}
```

### Test App Stop
```JSON
{
  "test_app_initial_state": "{% $states.input.initial_state %}",
  "test_db_initial_state": {
    "empty": true
  }
}
```

### Pre-Production App Stop
```JSON
{
  "preprod_app_initial_state": "{% $states.input.initial_state %}",
  "preprod_db_initial_state": {
    "empty": true
  }
}
```

### Dev DB Start
```JSON
{
  "dev_db_initial_state": "{% $states.input.initial_state %}",
  "dev_app_initial_state": {
    "empty": true
  }
}
```

### Test DB Start
```JSON
{
  "test_db_initial_state": "{% $states.input.initial_state %}",
  "test_app_initial_state": {
    "empty": true
  }
}
```

### Pre-Production DB Start
```JSON
{
  "preprod_db_initial_state": "{% $states.input.initial_state %}",
  "preprod_app_initial_state": {
    "empty": true
  }
}
```

