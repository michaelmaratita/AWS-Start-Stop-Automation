# Example CloudWatch Logs
### Start Success
```
STARTING PREPRODUCTION SERVERS
Server: test10 (i-00cf4d5173285122e) is running
Server: test3 (i-078fda61cd88fbd07) is running
Server: test9 (i-01c3da4ea7644f7ed) is running
Validating servers state: ['test3', 'test9', 'test10']
Rechecking instances status to ensure completion.
Rechecking instances status to ensure completion.
test10's Instance Status is initializing
test10's Instance Status is initializing
All servers have been successfully started.
test10 is in a running state
test10: Instance Status: passed
test10: System Status: passed
test3 is in a running state
test3: Instance Status: passed
test3: System Status: passed
test9 is in a running state
test9: Instance Status: passed
test9: System Status: passed

```

### Start Failure
```
STARTING PREPRODUCTION SERVERS
Server: test10 (i-00cf4d5173285122e) is stopped
Server: test3 (i-078fda61cd88fbd07) is stopped
Server: test9 (i-01c3da4ea7644f7ed) is stopped
Starting: test10 (i-00cf4d5173285122e)
Starting: test3 (i-078fda61cd88fbd07)
Starting: test9 (i-01c3da4ea7644f7ed)
Enabling Alarm: test3 - test
Validating servers state: ['test3', 'test9', 'test10']
Rechecking instances status to ensure completion.
Rechecking instances status to ensure completion.
Rechecking instances status to ensure completion.
Rechecking instances status to ensure completion.
Not all servers from (['test3', 'test9', 'test10']) have been started.
ABORTING STARTUPS.
Please validate server states in AWS Console.
Failed to start all servers.
test10 is in a running state
test10: Instance Status: initializing
test10: System Status: initializing
test3 is in a running state
test3: Instance Status: initializing
test3: System Status: initializing
test9 is in a running state
test9: Instance Status: initializing
test9: System Status: initializing
```

### Stop

```
STOPPING DEVELOPMENT SERVERS
Server: test1 (i-05c868d5d09413ae5) is running
Server: test11 (i-058be27b70e2fec7b) is running
Server: test12 (i-0d8bd90bf516333dc) is running
Server: test13 (i-0a8c5abaf9c06cb09) is running
Server: test14 (i-08de400479cf27353) is running
Server: test4 (i-066f1921dfac78c7b) is running
Server: test5 (i-01fc40e3662fe433b) is running
Server: test6 (i-09eb2725b6b641290) is running
Disabling Alarm: test1 - Lambda_Function
Disabling Alarm: test1 - testing
Disabling Alarm: test4 - testing
Stopping: test1 (i-05c868d5d09413ae5)
Stopping: test11 (i-058be27b70e2fec7b)
Stopping: test12 (i-0d8bd90bf516333dc)
Stopping: test13 (i-0a8c5abaf9c06cb09)
Stopping: test14 (i-08de400479cf27353)
Stopping: test4 (i-066f1921dfac78c7b)
Stopping: test5 (i-01fc40e3662fe433b)
Stopping: test6 (i-09eb2725b6b641290)
Validating servers state: ['test1', 'test4', 'test5', 'test6', 'test11', 'test12', 'test13', 'test14']
Rechecking instances status to ensure completion.
Rechecking instances status to ensure completion.
All servers have been successfully shut down.
test1 is in a stopped state
test11 is in a stopped state
test12 is in a stopped state
test13 is in a stopped state
test14 is in a stopped state
test4 is in a stopped state
test5 is in a stopped state
test6 is in a stopped state
```
