import boto3
import time

ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')


def main():
    original_list = describe_lists()
    copy_list = original_list[:]
    phase_num = 0
    phase_len = len(original_list)
    
    while phase_num < phase_len:
        working_list = copy_list[phase_num]
        is_pass, appended_list = start_ec2(working_list, phase_num)
        copy_list[phase_num] = appended_list
        phase_num += 1
        
        if not is_pass:
            break
    
    arch_notify(is_pass, original_list, copy_list)


def servers_lists():
    db1_servers = [
        'test_linux_1', 
        'test_linux_2', 
        'test_linux_3', 
        'test_linux_4', 
        'test_linux_5'
        ]
    db2_servers = [
        'test_linux_6', 
        'test_linux_7', 
        'test_linux_8', 
        'test_linux_9', 
        'test_linux_10'
        ]
    servers_lists = [
        db1_servers, db2_servers
        ]
    return servers_lists


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
            is_stopped = False
            describe_status = ec2_client.describe_instance_status(
                InstanceIds = [
                    instance_id
                ])['InstanceStatuses'][0]
            instance_status = describe_status['InstanceStatus']
            instance_status_status = instance_status['Status']
            instance_status_detail = instance_status['Details'][0]['Status']
            system_status = describe_status['SystemStatus']
            sys_status_status = system_status['Status']
            sys_status_detail = system_status['Details'][0]['Status']
            
            if (
                instance_status_detail == 'passed' and 
                sys_status_detail == 'passed'
                ):
                    is_initializing = False
            else:
                is_initializing = True
        else:
            is_stopped = True
            instance_status_status = 'Null'
            instance_status_detail = 'Null'
            sys_status_status = 'Null'
            sys_status_detail = 'Null'
            is_initializing = False
            
        server_dictionary[instance_name] = {
            'InstanceId' : instance_id,
            'State' : instance_state,
            'InstanceStatus' : {
                'Details' : instance_status_detail,
                'Status' : instance_status_status
            },
            'SystemStatus' : {
                'Details' : sys_status_detail,
                'Status' : sys_status_status
            },
            'is_stopped' : is_stopped,
            'is_initializing' : is_initializing
        }
    return server_dictionary
    

def start_ec2(list, phase_num):
    server_dictionary = list[0]
    instance_id_list = []
    initializing_list = []
    server_list = []
    cloudwatch_logs(list, phase_num)
    
    for server in server_dictionary.keys():
        server_list.append(server)
        server_key = server_dictionary[server]
        is_stopped = server_key['is_stopped']
        is_initializing = server_key['is_initializing']
        instance_id = server_key['InstanceId']
        if is_stopped:
            instance_id_list.append(instance_id)
        if is_initializing:
            initializing_list.append(server)
            
    if instance_id_list:
        print(f"Starting servers with InstanceId(s): {instance_id_list}")
        ec2_client.start_instances(
            InstanceIds = instance_id_list
            )
        time.sleep(150)
        
        while True:
            passed_servers = []
            new_server_dictionary = describe_ec2(server_list)
        
            for server in new_server_dictionary.keys():
                server_key = new_server_dictionary[server]
                is_initializing = server_key['is_initializing']
                is_stopped = server_key['is_stopped']
                
                if is_stopped:
                    is_pass = False
                    print(f"Phase {phase_num + 1} FAILED!")
                    cloudwatch_logs([new_server_dictionary], phase_num)
                    return is_pass, [new_server_dictionary]
                    
                elif not is_initializing:
                    passed_servers.append(server)
            
            if len(passed_servers) == len(new_server_dictionary.keys()):
                is_pass = True
                print(f"Phase {phase_num + 1} SUCCESSFUL!")
                cloudwatch_logs([new_server_dictionary], phase_num)
                return is_pass, [new_server_dictionary]
                
    elif not instance_id_list:
        if not is_initializing:
            print(f"Phase {phase_num + 1}: No Servers were stopped")
            is_pass = True
        else:
            is_pass = False
    return is_pass, list


def cloudwatch_logs(list, phase_num):
    server_dictionary = list[0]
    print(f"Phase {phase_num + 1} server state(s):")
    for server in server_dictionary.keys():
        server_key = server_dictionary[server]
        instance_id = server_key['InstanceId']
        state = server_key['State']
        i_details = server_key['InstanceStatus']['Details']
        i_status = server_key['InstanceStatus']['Status']
        s_details = server_key['SystemStatus']['Details']
        s_status = server_key['SystemStatus']['Status']
        print(f"{server}    State: {state}    InstanceStatus: " + \
            f"{i_details}({i_status})\\SystemStatus: {s_details}" + \
            f"({s_status})")


def arch_notify(is_pass, list1, list2):
    # Use SNS Topic ARN with correct IAM Permissions
    topic_arn = 'arn:aws:sns:us-west-2:*AWS ACCOUNT HERE*:Lambda_Shutdown_West2'
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
            server_key = server_dictionary1[server]
            instance_id = server_key['InstanceId']
            state = server_key['State']
            i_details = server_key['InstanceStatus']['Details']
            i_status = server_key['InstanceStatus']['Status']
            s_details = server_key['SystemStatus']['Details']
            s_status = server_key['SystemStatus']['Status']
            body += f"\t{server}    State: {state}    InstanceStatus: " + \
            f"{i_details}({i_status})\\SystemStatus: {s_details}" + \
            f"({s_status})\n"
        phase_num += 1
    body += """
Server State After Start Up Execution:
------------------------------------------------------------\n
"""
    phase_num = 0
    phase_len = len(list2)
    while phase_num < phase_len:
        working_list = list2[phase_num]
        body += f"Phase {phase_num + 1}:\n"
        server_dictionary2 = working_list[0]
        for server in server_dictionary2.keys():
            server_key = server_dictionary2[server]
            instance_id = server_key['InstanceId']
            state = server_key['State']
            i_details = server_key['InstanceStatus']['Details']
            i_status = server_key['InstanceStatus']['Status']
            s_details = server_key['SystemStatus']['Details']
            s_status = server_key['SystemStatus']['Status']
            instance_id = server_dictionary2[server]['InstanceId']
            state = server_dictionary2[server]['State']
            body += f"\t{server}    State: {state}    InstanceStatus: " + \
            f"{i_details}({i_status})\\SystemStatus: {s_details}" + \
            f"({s_status})\n"
        phase_num += 1
    
    if is_pass:
        subject = "START UPS COMPLETED SUCCESSFULLY"
    elif not is_pass:
        subject = "START UPS FAILED!"
        
    print(subject)
    sns_client.publish(
        TopicArn = topic_arn,
        Message = body,
        Subject = subject
        )
    # Change print to where email was sent, e.g. test@gmail.com
    print("email notification sent to test@gmail.com")
