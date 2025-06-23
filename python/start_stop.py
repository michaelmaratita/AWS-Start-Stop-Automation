import boto3
from time import sleep

ec2 = boto3.client('ec2')
cloudwatch_client = boto3.client('cloudwatch')
sns_client = boto3.client('sns')

#################################################################################################
#### Note: ONLY comment out the SERVER NAMES!!! (not brackets)
#### If an entire environment needs to be commented out, e.g. DEV APP;
#### You'll also need to make modification to lines 381-386 that corresponds to that environment
#### This will cause an indexing error if the modification is not done.
#### Lines 381-386 are associated with the EMAIL formatting
#### See Example for DEV APP. DEV APP Servers below are commented out, as well as line 381
##################################################################################################

def server_lists():
    lists = [

####### DEV APP #########
        [
        # 'test1',
        # 'test4', 
        # 'test5',
        # 'test19'
        ],

####### TEST APP #########
        [
        'test6',
        'test11',
        'test17',
        'test18'
        ],

####### PREPROD APP #########
        [
        'test12',
        'test13',
        'test14'
        ],

####### DEV DB #########
        [
        'test2',
        'test7',
        'test8'
        ],

####### TEST DB #########
        [
        'test3',
        'test9',
        'test10'
        ], 

####### PREPROD DB #########
        [
        'test15',
        'test16',
        'test20'
        ] 
    ]
    return lists

def get_validation_state(instances, action):
        if action == 'start':
            return instances.validate_status(0, action)
        else:
            return instances.validation(0, action)

def pre_check(event):
    instances = instance(server_lists()[event['phase_number']])
    if len(instances.data) > 1:
        return main(event, instances)
    return True, {"empty": True}
    
def main(event, instances):
    initial_state = instances.describe()
    print(event['cw_log_phase'].upper())
    instances.start_or_stop(initial_state, event['action'])
    passed = get_validation_state(instances, event['action'])
    cloudwatch.log_start_stop_status(instances, passed, event['action'])
    return passed, initial_state

class instance:
    def __init__(self, data):
        self.data = data

    def describe(self):
        reservations = ec2.describe_instances(Filters = [
            {
                'Name': 'tag:Name',
                'Values': self.data
            }
        ])['Reservations']
        return instance.server_dict(reservations[0]['Instances'])

    def server_dict(reservations):
        dictionary = {
            i['Tags'][0]['Value']: {
            'InstanceId': i['InstanceId'],
            'State': i['State']['Name'],
            'is_running':True
            if i['State']['Name'] == 'running'
            else False
            }
            for i in reservations
        }
        return dictionary
    
    def start_or_stop(self, instances, action):
        if action == 'stop':
            instance.stop(self, instances, action)
        else:
            instance.start(self, instances, action)

    def start(self, instances, action):
        start_list = [
            instances[i]['InstanceId']
            for i in instances
            if not instances[i]['is_running']
        ]
        for i in instances:
            print(cloudwatch.log_ec2_state(instances, i))
        if len(start_list) > 0:
            cloudwatch.log_action(instances, start_list, action)            
            ec2.start_instances(
                InstanceIds = start_list
            )
            cloudwatch.enable_alarms(self)
        else:
            print('No servers to start...')

    def stop(self, instances, action):
        stop_list = [
            instances[i]['InstanceId']
            for i in instances
            if instances[i]['is_running']
        ]
        for i in instances:
            print(cloudwatch.log_ec2_state(instances, i))
        if len(stop_list) > 0:
            cloudwatch.disable_alarms(self)
            cloudwatch.log_action(instances, stop_list, action)       
            ec2.stop_instances(
                InstanceIds = stop_list
            )
        else:
            print('No servers to stop...')

    def validation(self, num, action, sleep_val=15):
        num += 1
        passed = True
        instances = instance.describe(self)
        if sleep_val == 0:
            return passed
        if num == 1:
            cloudwatch.log_validation(self.data)
        if num == 5:
            cloudwatch.log_abort(self.data, action)
            return False
        state = instance.get_state(action)
        for i in instances:
            if instances[i]['State'] != state:
                passed = False
                sleep(sleep_val)
                break
        if not passed and num <= 4:
            print('Rechecking instances status to ensure completion.')
            passed = instance.validation(self, num, action)
        return passed

    def get_state(action):
        if action == 'stop':
            return 'stopped'
        else:
            return 'running'

    def validate_status(self, num, action, sleep_val=15):
        passed = instance.validation(self, 0, action, sleep_val)
        if not passed:
            return False
        num += 1
        sleep(45)
        updated_dict = instance.validation_dict(self)
        if num == 6:
            cloudwatch.log_max_validations(updated_dict)
            return False
        for i in updated_dict:
            instance_status = updated_dict[i]['InstanceStatus']
            system_status = updated_dict[i]['SystemStatus']
            if instance_status != 'passed':
                cw_log = f'{i}\'s Instance Status is'
                cw_log += f' {instance_status}'
                print(cw_log)
                passed = False
                break
            elif system_status != 'passed':
                cw_log = f'{i}\'s System Status is'
                cw_log += f' {system_status}'
                print(cw_log)
                passed = False
                break
        if not passed and num < 6:
                passed = instance.validate_status(self, num, action, 0)
        return passed
        
    def validation_dict(self):
        instances = instance.describe(self)
        id_list = [instance['InstanceId'] for instance in instances.values()]
        describe_status = ec2.describe_instance_status(
            InstanceIds = id_list
        )['InstanceStatuses']
        new_dict = {
            i : {
                'InstanceId': instances[i]['InstanceId'],
                'State': instances[i]['State'],
                'is_running': instances[i]['is_running'],
                'InstanceStatus': ii['InstanceStatus']['Details'][0]['Status'],
                'SystemStatus': ii['SystemStatus']['Details'][0]['Status']
            }
            for i in instances
            for ii in describe_status
            if instances[i]['InstanceId'] == ii['InstanceId']
        }
        return new_dict
    
    def get_end_state(subject):
        if "shutdown" in subject.lower():
            list = [
                instance.describe(instance(i))
                for i in server_lists()
                if len(i) != 0
                ]
        else:
            list = [
                instance.validation_dict(instance(i))
                for i in server_lists()
                if len(i) != 0
                ]
        return list


class cloudwatch:
    def log_action(instances, list, action):
        ref = {
            'stop': 'Stopping',
            'start': 'Starting'
        }
        for i in instances:
            if instances[i]['InstanceId'] in list:
                print(f'{ref[action]}: {i} ({instances[i]['InstanceId']})')

    def log_abort(instance_list, action):
        abort_dict = {
            'start': {
                'v1': 'started',
                'v2': 'STARTUPS'
            },
            'stop': {
                'v1': 'stopped',
                'v2': 'SHUTDOWNS'
            }
        }
        abort = f'Not all servers have been {abort_dict[action]['v1']}...'
        abort += f'ABORTING {abort_dict[action]['v1']}.\nPlease validate serve'
        abort += f'r states in AWS Console.\n {instance_list}' 
        print(abort)
        return abort

    def log_validation(instance_list):
        print(f'Validating servers state: {instance_list}')

    def log_ec2_state(instances, i):
        cw_log = f'Server: {i} ({instances[i]['InstanceId']})'
        cw_log += f' is {instances[i]['State']}'
        return cw_log
    
    def log_max_validations(dictionary):
        cw_log = f'Please check the Instance Status and Systems Status for the'
        cw_log += f' following servers:\n\n{dictionary}'
        print(cw_log)

    def log_start_stop_status(self, passed, action):
        if action == 'start':
            dictionary = instance.validation_dict(self)
        else:
            dictionary = instance.describe(self)
        if passed:
            print(cloudwatch.intro(action, 'success'))
        else:
            print(cloudwatch.intro(action, 'fail'))
            
        print(cloudwatch.log_status(dictionary, action))

    def intro(action, state):
        intro_dict = {
            'start': {
                'success': '\nAll servers have been successfully started.\n',
                'fail': '\nFailed to start all servers.\n'
            },
            'stop': {
                'success': '\nAll servers have been successfully shut down.\n',
                'fail': '\nFailed to stop all servers.\n'
            }
        }
        return intro_dict[action][state]

    def log_status(dictionary, action):
        if action == 'start':
            return cloudwatch.format_log_status_start(dictionary)
        else:
            status = ''
            for i in dictionary:
                log1 = cloudwatch.format_state_log(dictionary, i)
                status += f'{log1}.\n'
            return status
    
    def format_log_status_start(dictionary):
        status = ''
        for i in dictionary:
            log1 = cloudwatch.format_state_log(dictionary, i) 
            log2 = cloudwatch.format_start_log(dictionary, i)
            status += f'{log1}.\n{log2[0]}'
            status += f' | {log2[1]}\n'
        return status

    def format_start_log(dictionary, i):
        log = {
                'i_status': f'{i} ({dictionary[i]['InstanceId']}): Instan' + \
                f'ce Status: {dictionary[i]['InstanceStatus']}',
                's_status': f'System Status: ' + \
                f'{dictionary[i]['SystemStatus']}\n'
            }
        return log['i_status'],log['s_status']
    
    def format_state_log(dictionary, i):
        return f'{i} is in a {dictionary[i]['State']} state'
        
    def get_alarm_names(self):
        all_alarms = cloudwatch_client.describe_alarms()['MetricAlarms']
        alarm_list = [
            alarm['AlarmName']
            for alarm in all_alarms
            ]
        alarm_names = [
            alarm 
            for alarm in alarm_list
            for instance in self.data 
            if instance in alarm
            ]
        return alarm_names
    
    def disable_alarms(self):
        alarms_list = cloudwatch.get_alarm_names(self)
        for alarm in alarms_list:
            print(f'Disabling Alarm: {alarm}')
        cloudwatch_client.disable_alarm_actions(
            AlarmNames = alarms_list
        )

    def enable_alarms(self):
        alarms_list = cloudwatch.get_alarm_names(self)
        for alarm in alarms_list:
            print(f'Enabling Alarm: {alarm}')
        cloudwatch_client.enable_alarm_actions(
            AlarmNames = alarms_list
        )
            
class sns:
    def __init__(self, data):
        self.data = data
        self.subject = data['subject']
        self.initial = [
            data[k] 
            for k in list(data.keys())[2:]
            if len(data[k]) > 1
            ]
        self.phases = [
            # "dev app servers",
            "test app servers",
            "preprod app servers",
            "dev db servers",
            "test db servers",
            "preprod db servers"
            ]

    def get_topic():
        topic_arns = sns_client.list_topics()['Topics']
        for arn in topic_arns:
            if 'mailme' in arn['TopicArn']:
                return arn['TopicArn']

    def send_mail(event):
        body = sns.format_body(event)
        sns_client.publish(
            TopicArn = sns.get_topic(),
            Message = body,
            Subject = event.subject.upper()
            )
    
    def format_body(event):
        phases = event.phases
        intro = f"ALCON,\n\nPlease see each server's status below.\n\n"
        intro += f"{event.subject}\n-----------------------------------"
        if 'abort' in event.subject:
            if 'start' in event.subject:
                intro += f'\n{cloudwatch.log_abort(server_lists(),'start')}'
            else:
                intro += f'\n{cloudwatch.log_abort(server_lists(),'stop')}'
        i_body = sns.format_initial_state(event.initial, phases)
        e_state_body = sns.format_end_state(event)
        return intro + i_body + e_state_body
    
    def format_initial_state(state, phases):
        body = '\nINITIAL STATE:\n'
        index = 0
        for dict in state:
            body += f"\n{phases[index].upper()}\n--------------------------\n"
            index += 1
            for i in dict:
                body += f'{cloudwatch.log_ec2_state(dict, i)}\n'
        return body
    
    def format_end_state(event): 
        phases = event.phases
        action, state = sns.get_verb(event.subject)
        end_intro = '\n-------------------------------------------------------'
        end_intro += f'{cloudwatch.intro(action, state)}'
        state_keys = instance.get_end_state(event.subject)
        index = 0
        for i in state_keys:
            end_intro += f"\n{phases[index].upper()}\n-----------------------\n"
            end_intro += f'{cloudwatch.log_status(i, action)}' 
            index += 1
        return end_intro
    
    def get_verb(subject):
        if 'start' in subject.lower():
                action = 'start'
        else:
            action = 'stop'
        if 'success' in subject.lower():
            state = 'success'
        else:
            state = 'fail'
        return action, state
