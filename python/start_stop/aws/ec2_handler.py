import boto3
from start_stop.aws.cloudwatch.log_handler import Logger
from start_stop.aws.cloudwatch.alarm_handler import AlarmManager
from start_stop.SERVER_LIST import server_lists
from time import sleep


client = boto3.client('ec2')


class EC2Instance:
    def __init__(self, names):
        self.names = names

    def describe(self):
        reservations = client.describe_instances(Filters = [
            {
                'Name': 'tag:Name',
                'Values': self.names
            }
        ])['Reservations']
        return self._to_dict(reservations[0]['Instances'])
    
    def _to_dict(self, reservations):
        return {
            i['Tags'][0]['Value']: {
            'InstanceId': i['InstanceId'],
            'State': i['State']['Name'],
            'is_running': i['State']['Name'] == 'running'
            }
            for i in reservations
        }
        
    def start_or_stop(self, action):
        if action == 'stop':
            self._stop(action)
        else:
            self._start(action)

    def _start(self, action):
        instances = self.describe()
        start_list = [
            v['InstanceId']
            for v in instances.values()
            if not v['is_running']
        ]
        for name in instances:
            print(Logger.log_intance_state(instances, name))
        if start_list:
            Logger.log_action(instances, start_list, action)            
            client.start_instances(
                InstanceIds = start_list
            )
            AlarmManager.enable_alarms(AlarmManager(self.names))
        else:
            print('No servers to start...')

    def _stop(self, action):
        instances = self.describe()
        stop_list = [
            v['InstanceId']
            for v in instances.values()
            if v['is_running']
        ]
        for name in instances:
            print(Logger.log_intance_state(instances, name))
        if stop_list:
            AlarmManager.disable_alarms(AlarmManager(self.names))
            Logger.log_action(instances, stop_list, action)       
            client.stop_instances(
                InstanceIds = stop_list
            )
        else:
            print('No servers to stop...')

    def validation(self, num, action, sleep_val=15):
        num += 1
        passed = True
        instances = self.describe()
        if sleep_val == 0:
            return passed
        if num == 1:
            Logger.log_validation(self.names)
        if num == 5:
            print(Logger.log_abort(self.names, action))
            return False
        expected_state = 'running' if action == 'start' else 'stopped'
        for instance in instances.values():
            if instance['State'] != expected_state:
                passed = False
                sleep(sleep_val)
                break
        if not passed and num <= 4:
            print('Rechecking instances status to ensure completion.')
            passed = self.validation(num, action)
        return passed
    
    def validate_status(self, num, action, sleep_val=15):
        passed = self.validation(0, action, sleep_val)
        if not passed:
            return False
        num += 1
        sleep(45)
        updated_dict = self.validation_dict()
        if num == 6:
            Logger.log_max_validations(updated_dict)
            return False
        for i, status in updated_dict.items():
            if status['InstanceStatus'] != 'passed':
                print(f'{i}\'s Instance Status is {status['InstanceStatus']}')
                passed = False
                break
            elif status['InstanceStatus'] != 'passed':
                print(f'{i}\'s System Status is {status['SystemStatus']}')
                passed = False
                break
        if not passed and num < 6:
                passed = self.validate_status(num, action, 0)
        return passed
    
    def validation_dict(self):
        instances = self.describe()
        instance_ids = [id['InstanceId'] for id in instances.values()]
        statuses = client.describe_instance_status(
            InstanceIds = instance_ids
        )['InstanceStatuses']
        updated_dict =  {
            i : {
                'InstanceId': instances[i]['InstanceId'],
                'State': instances[i]['State'],
                'is_running': instances[i]['is_running'],
                'InstanceStatus': ii['InstanceStatus']['Details'][0]['Status'],
                'SystemStatus': ii['SystemStatus']['Details'][0]['Status']
            }
            for i in instances
            for ii in statuses
            if instances[i]['InstanceId'] == ii['InstanceId']
        }
        return updated_dict
    
    def instance_log_status(self, passed, action):
        if action == 'start':
            dictionary = self.validation_dict()
        else:
            dictionary = self.describe()
        if passed:
            print(Logger.intro(action, 'success'))
        else:
            print(Logger.intro(action, 'fail'))        
        print(Logger.log_status(dictionary, action))
    
    @staticmethod
    def get_end_state(subject):
        state_data = []
        is_shutdown = "shutdown" in subject.lower()
        for group in server_lists():
            if not group:
                continue
            instance_obj = EC2Instance(group)
            if is_shutdown:
                state_data.append(instance_obj.describe())
            else:
                state_data.append(instance_obj.validation_dict())
        return state_data
