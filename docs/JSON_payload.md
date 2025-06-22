# JSON Payload Information For Step Function Input/Output

## Development App Servers:
### JSON Payload Format
```json
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
```json
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
```json
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
```json
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
```json
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
```json
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
