import boto3


client = boto3.client('cloudwatch')


class AlarmManager:
    def __init__(self, names):
        self.alarm_names = names

    def get_alarm_names(self):
        alarms = client.describe_alarms()['MetricAlarms']
        return [
            a['AlarmName'] for a in alarms
            if any(name in a['AlarmName'] for name in self.alarm_names)
        ]
    
    def disable_alarms(self):
        alarms_list = self.get_alarm_names()
        for alarm in alarms_list:
            print(f'Disabling Alarm: {alarm}')
        client.disable_alarm_actions(
            AlarmNames = alarms_list
        )

    def enable_alarms(self):
        alarms_list = self.get_alarm_names()
        for alarm in alarms_list:
            print(f'Enabling Alarm: {alarm}')
        client.enable_alarm_actions(
            AlarmNames = alarms_list
        )
