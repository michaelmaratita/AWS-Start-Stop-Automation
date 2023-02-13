# <p align="center"><img align="center" src="/source/images/logos/lambda_logo.PNG" width=5% height=5%> **Create Start DB EC2 Function**</p>

1. Select the **Lambda** Service
2. Under AWS Lambda > Select **Functions**
3. Select **Create function**
4. Under the Create function Pane, leave the default **Author from scratch**
   - 4.1. Enter the Function Name, e.g. Phase_Start_DB 
   - 4.2. Under Runtime, Select **Python 3.9** from the drop-down options
   - 4.3. Under Architecture, leave the default **x86_64** radio button
   - 4.4. Expand Permission > Select the **Use an existing role** radio button
     - 4.4.1. Under Existing Role, Select the role created in [Create IAM Role](/AWS-Start-Stop-Automation/how_to/iam/create_iam_role.md) step
   - 4.5. Select the **Create function** button

5. Under Code source > from the lambda_function.py, **remove** the following code:
```python
  # TODO implement
  return {
  'statusCode': 200,
  'body': json.dumps('Hello from Lambda!')
  }
```
    
6. On line 2, insert the following code:
    ```python
    from start_servers import main
    ```
   6.1. Press Enter
   
7. On line 5 **Press Enter**, insert the following code on line 6:
> NOTE: The code should follow the same format as below.
```python
    result = main()

    if result:
        output = "pass"
    else:
        output = "fail"

    return {
        'status' : output
    }
```

### FULL EXAMPLE
```python
1   import json
2   from start_servers import main
3
4
5   def lambda_handler(event, context):
6       result = main()
7
8       if result:
9           output = "pass"
10      else:
11          output = "fail"
12
13      return {
14          'status' : output
15      }
```

8. Select File > Open New File
   - 8.1. Copy [Python Code for Lambda Function](/python/lambda_start_db.py) and paste into the Untitled1 fiile
9. Select File Save As...
   - 9.1. Enter Filename, e.g. start_db_servers.py
   - 9.2. Select Save
10. Select the **Deploy Button** at the top
