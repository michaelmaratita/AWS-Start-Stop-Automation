# JSON Code for Step Function State Machine
## Start State Machine
```
{
  "Comment": "State Machine to Start Lower Environments",
  "StartAt": "Start Lower Environments",
  "States": {
    "Start Lower Environments": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "Start Development DB Servers",
          "States": {
            "Start Development DB Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": "{% $states.result.Payload %}",
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 3,
                  "next_phase": true,
                  "action": "start",
                  "cw_log_phase": "starting development db servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "Next": "Did Dev DBs Start?"
            },
            "Did Dev DBs Start?": {
              "Type": "Choice",
              "Choices": [
                {
                  "Next": "Wait for Dev DB process",
                  "Condition": "{% ($states.input.next_phase) = (true) %}",
                  "Comment": "Sucessful Start"
                }
              ],
              "Default": "Dev DB Start Failure"
            },
            "Wait for Dev DB process": {
              "Type": "Wait",
              "Seconds": 60,
              "Next": "Start Development App Servers"
            },
            "Start Development App Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": {
                "start_dev": "{% $states.result.Payload.next_phase %}",
                "dev_server_type": "application",
                "dev_db_initial_state": "{% $states.input.initial_state %}",
                "dev_app_initial_state": "{% $states.result.Payload.initial_state %}"
              },
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 0,
                  "next_phase": "next_phase.$",
                  "action": "start",
                  "cw_log_phase": "starting development app servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            },
            "Dev DB Start Failure": {
              "Type": "Pass",
              "End": true,
              "Output": {
                "dev_db_initial_state": "{% $states.input.initial_state %}",
                "dev_app_initial_state": {
                  "empty": true
                }
              }
            }
          }
        },
        {
          "StartAt": "Start Test DB",
          "States": {
            "Start Test DB": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": "{% $states.result.Payload %}",
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 4,
                  "next_phase": true,
                  "action": "start",
                  "cw_log_phase": "starting test db servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "Next": "Did Test DBs Starts?"
            },
            "Did Test DBs Starts?": {
              "Type": "Choice",
              "Choices": [
                {
                  "Next": "Wait for Test DB process",
                  "Condition": "{% ($states.input.next_phase) = (true) %}",
                  "Comment": "Successful Start"
                }
              ],
              "Default": "Test DB Start Failure"
            },
            "Wait for Test DB process": {
              "Type": "Wait",
              "Seconds": 60,
              "Next": "Start Test App Servers"
            },
            "Start Test App Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": {
                "start_test": "{% $states.result.Payload.next_phase %}",
                "test_server_type": "application",
                "test_db_initial_state": "{% $states.input.initial_state %}",
                "test_app_initial_state": "{% $states.result.Payload.initial_state %}"
              },
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 1,
                  "next_phase": "next_phase.$",
                  "action": "start",
                  "cw_log_phase": "starting test app servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            },
            "Test DB Start Failure": {
              "Type": "Pass",
              "End": true,
              "Output": {
                "test_db_initial_state": "{% $states.input.initial_state %}",
                "test_app_initial_state": {
                  "empty": true
                }
              }
            }
          }
        },
        {
          "StartAt": "Start PreProd DB Servers",
          "States": {
            "Start PreProd DB Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": "{% $states.result.Payload %}",
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 5,
                  "next_phase": true,
                  "action": "start",
                  "cw_log_phase": "starting preproduction db servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "Next": "Did PreProd DBs Start?"
            },
            "Did PreProd DBs Start?": {
              "Type": "Choice",
              "Choices": [
                {
                  "Next": "Wait for PreProd DB process",
                  "Condition": "{% ($states.input.next_phase) = (true) %}",
                  "Comment": "Successful Start"
                }
              ],
              "Default": "PreProd DB Start Failure"
            },
            "Wait for PreProd DB process": {
              "Type": "Wait",
              "Seconds": 60,
              "Next": "Start PreProd App Servers"
            },
            "Start PreProd App Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": {
                "start_preprod": "{% $states.result.Payload.next_phase %}",
                "preprod_server_type": "application",
                "preprod_db_initial_state": "{% $states.input.initial_state %}",
                "preprod_app_initial_state": "{% $states.result.Payload.initial_state %}"
              },
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 2,
                  "next_phase": "next_phase.$",
                  "action": "start",
                  "cw_log_phase": "starting preproduction app servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            },
            "PreProd DB Start Failure": {
              "Type": "Pass",
              "End": true,
              "Output": {
                "preprod_db_initial_state": "{% $states.input.initial_state %}",
                "preprod_app_initial_state": {
                  "empty": true
                }
              }
            }
          }
        }
      ],
      "Next": "Did All Servers Start?"
    },
    "Did All Servers Start?": {
      "Type": "Choice",
      "Choices": [
        {
          "Next": "Send Success Email",
          "Condition": "{% (($states.input.start_dev) = (true) and
                          ($states.input.dev_server_type) = (\"application\") and
                          ($states.input.start_test) = (true) and
                          ($states.input.test_server_type) = (\"application\") and
                          ($states.input.start_preprod) = (true) and
                          ($states.input.preprod_server_type) = (\"application\")) %}",
          "Comment": "All Servers Started"
        }
      ],
      "Default": "Send Failure Email"
    },
    "Send Success Email": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
        "Payload": {
          "send_mail": true,
          "subject": "START STATUS: SUCCESS",
          "dap_state": "{% $states.input.dev_app_initial_state %}",
          "tap_state": "{% $states.input.test_app_initial_state %}",
          "pap_state": "{% $states.input.preprod_app_initial_state %}",
          "ddb_state": "{% $states.input.dev_db_initial_state %}",
          "tdb_state": "{% $states.input.test_db_initial_state %}",
          "pdb_state": "{% $states.input.preprod_db_initial_state %}"
        }
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Success"
    },
    "Success": {
      "Type": "Succeed"
    },
    "Send Failure Email": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
        "Payload": {
          "send_mail": true,
          "subject": "START STATUS: ABORTED",
          "dap_state": "{% $states.input.dev_app_initial_state %}",
          "tap_state": "{% $states.input.test_app_initial_state %}",
          "pap_state": "{% $states.input.preprod_app_initial_state %}",
          "ddb_state": "{% $states.input.dev_db_initial_state %}",
          "tdb_state": "{% $states.input.test_db_initial_state %}",
          "pdb_state": "{% $states.input.preprod_db_initial_state %}"
        }
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Fail"
    },
    "Fail": {
      "Type": "Fail"
    }
  },
  "QueryLanguage": "JSONata"
}
```

## Stop State Machine
```
{
  "Comment": "State Machine to Stop Lower Environments",
  "StartAt": "Stop Lower Environments",
  "States": {
    "Stop Lower Environments": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "Stop Dev App Servers",
          "States": {
            "Stop Dev App Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": "{% $states.result.Payload %}",
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 0,
                  "next_phase": true,
                  "action": "stop",
                  "cw_log_phase": "stopping development app servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "Next": "Did Dev App Servers Stop?"
            },
            "Did Dev App Servers Stop?": {
              "Type": "Choice",
              "Choices": [
                {
                  "Next": "Stop Dev DB",
                  "Condition": "{% ($states.input.next_phase) = (true) %}",
                  "Comment": "Sucessful Stop"
                }
              ],
              "Default": "Dev App Stop Failure"
            },
            "Dev App Stop Failure": {
              "Type": "Pass",
              "End": true,
              "Output": {
                "dev_app_initial_state": "{% $states.input.initial_state %}",
                "dev_db_initial_state": {
                  "empty": true
                }
              }
            },
            "Stop Dev DB": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": {
                "stop_dev": "{% $states.result.Payload.next_phase %}",
                "dev_server_type": "database",
                "dev_db_initial_state": "{% $states.result.Payload.initial_state %}",
                "dev_app_initial_state": "{% $states.input.initial_state %}"
              },
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 3,
                  "next_phase": "next_phase.$",
                  "action": "stop",
                  "cw_log_phase": "stopping development db servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "Stop Test App Servers",
          "States": {
            "Stop Test App Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": "{% $states.result.Payload %}",
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 1,
                  "next_phase": true,
                  "action": "stop",
                  "cw_log_phase": "stopping test app servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "Next": "Did Test App Servers Stop?"
            },
            "Did Test App Servers Stop?": {
              "Type": "Choice",
              "Choices": [
                {
                  "Next": "Stop Test DB",
                  "Condition": "{% ($states.input.next_phase) = (true) %}",
                  "Comment": "Sucessful Stop"
                }
              ],
              "Default": "Test App Stop Failure"
            },
            "Test App Stop Failure": {
              "Type": "Pass",
              "End": true,
              "Output": {
                "test_app_initial_state": "{% $states.input.initial_state %}",
                "test_db_initial_state": {
                  "empty": true
                }
              }
            },
            "Stop Test DB": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": {
                "stop_test": "{% $states.result.Payload.next_phase %}",
                "test_server_type": "database",
                "test_db_initial_state": "{% $states.result.Payload.initial_state %}",
                "test_app_initial_state": "{% $states.input.initial_state %}"
              },
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 4,
                  "next_phase": "next_phase.$",
                  "action": "stop",
                  "cw_log_phase": "stopping test db servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "Stop PreProd App Servers",
          "States": {
            "Stop PreProd App Servers": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": "{% $states.result.Payload %}",
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 2,
                  "next_phase": true,
                  "action": "stop",
                  "cw_log_phase": "stopping preproduction app servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "Next": "Did PreProd App Servers Stop?"
            },
            "Did PreProd App Servers Stop?": {
              "Type": "Choice",
              "Choices": [
                {
                  "Next": "Stop PreProd DB",
                  "Condition": "{% ($states.input.next_phase) = (true) %}",
                  "Comment": "Sucessful Stop"
                }
              ],
              "Default": "PreProd App Stop Failure"
            },
            "PreProd App Stop Failure": {
              "Type": "Pass",
              "End": true,
              "Output": {
                "preprod_app_initial_state": "{% $states.input.initial_state %}",
                "preprod_db_initial_state": {
                  "empty": true
                }
              }
            },
            "Stop PreProd DB": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Output": {
                "stop_preprod": "{% $states.result.Payload.next_phase %}",
                "preprod_server_type": "database",
                "preprod_db_initial_state": "{% $states.result.Payload.initial_state %}",
                "preprod_app_initial_state": "{% $states.input.initial_state %}"
              },
              "Arguments": {
                "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
                "Payload": {
                  "phase_number": 5,
                  "next_phase": "next_phase.$",
                  "action": "stop",
                  "cw_log_phase": "stopping preproduction db servers",
                  "send_mail": false
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            }
          }
        }
      ],
      "Next": "Did ALL Servers Stop?"
    },
    "Did ALL Servers Stop?": {
      "Type": "Choice",
      "Choices": [
        {
          "Next": "Send Success Email",
          "Condition": "{% (($states.input.stop_dev) = (true) and
                        ($states.input.stop_test) = (true) and
                        ($states.input.stop_preprod) = (true) and
                        ($states.input.dev_server_type) = (\"database\") and
                        ($states.input.test_server_type) = (\"database\") and
                        ($states.input.preprod_server_type) = (\"database\")) %}",
          "Comment": "All Servers Stopped"
        }
      ],
      "Default": "Send Failure Email"
    },
    "Send Success Email": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
        "Payload": {
          "send_mail": true,
          "subject": "SHUTDOWN STATUS: SUCCESS",
          "dap_state": "{% $states.input.dev_app_initial_state %}",
          "tap_state": "{% $states.input.test_app_initial_state %}",
          "pap_state": "{% $states.input.preprod_app_initial_state %}",
          "ddb_state": "{% $states.input.dev_db_initial_state %}",
          "tdb_state": "{% $states.input.test_db_initial_state %}",
          "pdb_state": "{% $states.input.preprod_db_initial_state %}"
        }
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Success"
    },
    "Success": {
      "Type": "Succeed"
    },
    "Send Failure Email": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:region:aws_account_number:function:Start_Stop:$LATEST",
        "Payload": {
          "send_mail": true,
          "subject": "SHUTDOWN STATUS: ABORTED",
          "dap_state": "{% $states.input.dev_app_initial_state %}",
          "tap_state": "{% $states.input.test_app_initial_state %}",
          "pap_state": "{% $states.input.preprod_app_initial_state %}",
          "ddb_state": "{% $states.input.dev_db_initial_state %}",
          "tdb_state": "{% $states.input.test_db_initial_state %}",
          "pdb_state": "{% $states.input.preprod_db_initial_state %}"
        }
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Fail"
    },
    "Fail": {
      "Type": "Fail"
    }
  },
  "QueryLanguage": "JSONata"
}
```
