import boto3
import time


ec2_client = boto3.client('ec2')
cloudwatch_client = boto3.client('cloudwatch')
sns_client = boto3.client('sns')

def main():
    disable_alarm()
    original_list = describe_lists()
    copy_list = original_list[:]
    phase_num = 0
    phase_len = len(original_list)
    
    while phase_num < phase_len:
        working_list = copy_list[phase_num]
        is_pass, appended_list = stop_ec2(working_list, phase_num)
        copy_list[phase_num] = appended_list
        phase_num += 1
        
        if not is_pass:
            break
    # Send email to SNS Topic Address
    email_notify(is_pass, original_list, copy_list)


def servers_lists():
  # Append lists to reflect AWS {Tag: Name}
    dev_app_servers = [
        'test_linux_1',
        'test_linux_2',
        'test_linux_3',
        'test_linux_4',
        'test_linux_5'
        ]
    test_app_servers = [
        'test_linux_6',
        'test_linux_7',
        'test_linux_8',
        'test_linux_9',
        'test_linux_10'
        ]
    pp_app_servers = [
        'test_linux_11',
        'test_linux_12',
        'test_linux_13',
        'test_linux_14',
        'test_linux_15'
        ]
    dev_db_servers = [
        'test_linux_16',
        'test_linux_17',
        'test_linux_18'
        ]
    test_db_servers = [
        'test_linux_19',
        'test_linux_20'
        ]
    servers_lists = [
        dev_app_servers, test_app_servers, pp_app_servers,
        dev_db_servers, test_db_servers
        ] 
    return servers_lists


def disable_alarm():
    while True:
        alarms_enabled = []
        cloudwatch_log = ''
        alarm_responses = cloudwatch_client.describe_alarms(
          # Append AlarmNames with CloudWatch pertinent Alarm Names  
          AlarmNames = [
                'test_linux_1 - StatusCheckFailed_System',
                'test_linux_2 - StatusCheckFailed_System'
                ])['MetricAlarms']
        
        for alarm in alarm_responses:
            alarm_name = alarm['AlarmName']
            action_enabled = alarm['ActionsEnabled']
            
            cloudwatch_log += f"{alarm_name}\tActionsEnabled:" + \
                            f"{action_enabled}\n"
            if action_enabled:
                alarms_enabled.append(alarm_name)
           
        if alarms_enabled:
            cloudwatch_log = "Disabling Alarms:\n" + cloudwatch_log
            print(cloudwatch_log)
            cloudwatch_client.disable_alarm_actions(
                AlarmNames = alarms_enabled
                )
        else:
            cloudwatch_log = "Alarm States:\n" + cloudwatch_log
            print(cloudwatch_log)
            break


def describe_lists():
    server_lists = servers_lists()
    return_list = []
    for list in server_lists:
        described_dict = describe_ec2(list)
        return_list.append([described_dict])
    return return_list


def describe_ec2(list):
    server_dictionary = {}
    reservations = ec2_client.describe_instances(Filters = [
        {
         'Name' : 'tag:Name',
         'Values' : list
        }])['Reservations']

    for instance in reservations:
        instance = instance['Instances'][0]
        instance_id = instance['InstanceId']
        instance_state = instance['State']['Name']
        instance_tags = instance['Tags']
        
        for instance_key in instance_tags:
            if instance_key['Key'] == 'Name':
                instance_name = instance_key['Value']
        if instance_state == 'running':
            status_boolean = True
        elif instance_state == 'stopped':
            status_boolean = False
            
        server_dictionary[instance_name] = {
            'InstanceId' : instance_id ,
            'State' : instance_state,
            'is_running' : status_boolean}
    return server_dictionary


def stop_ec2(list, phase_num):
    server_dictionary = list[0]
    instance_id_list = []
    server_list = []
    cloudwatch_logs(list, phase_num)
    
    for server in server_dictionary.keys():
        server_list.append(server)
        server_key = server_dictionary[server]
        is_running = server_key['is_running']
        instance_id = server_key['InstanceId']
        if is_running:
            instance_id_list.append(instance_id)
    
    if instance_id_list:
        print(f"Stopping servers with InstanceId(s): {instance_id_list}")
        ec2_client.stop_instances(
            InstanceIds = instance_id_list)
        time.sleep(60)
        new_server_dictionary = describe_ec2(server_list)
        is_pass = pass_result(new_server_dictionary)
        cloudwatch_logs([new_server_dictionary], phase_num)
        return is_pass, [new_server_dictionary]
    
    elif not instance_id_list:
        is_pass = pass_result(server_dictionary)
        return is_pass, list


def pass_result(server_dictionary):
    is_pass = True
    for server in server_dictionary.keys():
        server_key = server_dictionary[server]
        if server_key['is_running']:
            is_pass = False
            return is_pass
    return is_pass
    

def cloudwatch_logs(list, phase_num):
    server_dictionary = list[0]
    print(f"Phase {phase_num + 1} server state(s):")
    for server in server_dictionary.keys():
        instance_id = server_dictionary[server]['InstanceId']
        state = server_dictionary[server]['State']
        print(f"{server}({instance_id}) is {state}")


def email_notify(is_pass, list1, list2):
    # Use SNS Topic ARN with correct IAM Permissions
    topic_arn = 'arn:aws:sns:us-west-2:*AWS_ACCOUNT_HERE*:Lambda_Shutdown_West2'
    body = """Please see below for server. Please check CloudWatch logs for 
any additional information regarding shutdowns.
    
Initial Running/Stop State:
------------------------------------------------------------\n
"""
    phase_num = 0
    phase_len = len(list1)
    while phase_num < phase_len:
        working_list = list1[phase_num]
        body += f"Phase {phase_num + 1}:\n"
        server_dictionary1 = working_list[0]
        for server in server_dictionary1.keys(): 
            instance_id = server_dictionary1[server]['InstanceId']
            state = server_dictionary1[server]['State']
            body += f"\t{server}\tId: {instance_id:<25}\tState: {state}\n"
        phase_num += 1
    body += """
Server State After Shut Down Execution:
------------------------------------------------------------\n
"""
    phase_num = 0
    phase_len = len(list2)
    while phase_num < phase_len:
        working_list = list2[phase_num]
        body += f"Phase {phase_num + 1}:\n"
        server_dictionary2 = working_list[0]
        for server in server_dictionary2.keys(): 
            instance_id = server_dictionary2[server]['InstanceId']
            state = server_dictionary2[server]['State']
            body += f"\t{server}\tId: {instance_id:<25}\tState: {state}\n"
        phase_num += 1
    
    if is_pass:
        subject = "SHUTDOWNS COMPLETED SUCCESSFULLY"
    elif not is_pass:
        subject = "SHUTDOWNS FAILED!"
        
    print(subject)
    sns_client.publish(
        TopicArn = topic_arn,
        Message = body,
        Subject = subject
        )
    # Change print to where email was sent, e.g. test@gmail.com
    print("email notification sent to test@gmail.com")
