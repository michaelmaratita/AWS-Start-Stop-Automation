import boto3
from start_stop.aws.cloudwatch.log_handler import Logger
from start_stop.aws.ec2_handler import EC2Instance
from SERVER_LIST import server_lists, environments


client = boto3.client('sns')


class SNSHandler:
    def __init__(self, data):
        self.data = data
        self.sns_topic = 'mailme'
        self.subject = data['subject']
        self.initial = [
            data[k] 
            for k in list(data.keys())[2:]
            if len(data[k]) > 1
            ]
        self.phases = environments()

    def get_topic(self):
        topic_arns = client.list_topics()['Topics']
        return next(arn['TopicArn'] for arn in topic_arns
                    if self.sns_topic in arn['TopicArn'])

    def send_mail(self):
        body = self.format_body()
        client.publish(
            TopicArn = self.get_topic(),
            Message = body,
            Subject = self.subject.upper()
            )
    
    def format_body(self):
        intro = f"ALCON,\n\nPlease see each server's status below.\n\n"
        intro += f"{self.subject}\n-----------------------------------"
        if 'abort' in self.subject:
            if 'start' in self.subject:
                intro += f'\n{Logger.log_abort(server_lists(),'start')}'
            else:
                intro += f'\n{Logger.log_abort(server_lists(),'stop')}'
        i_body = self.format_initial_state()
        e_state_body = self.format_end_state()
        return intro + i_body + e_state_body
    
    def format_initial_state(self):
        body = '\nINITIAL STATE:\n'
        index = 0
        for dict in self.initial:
            body += f"\n{self.phases[index].upper()}\n--------------------------\n"
            index += 1
            for i in dict:
                body += f'{Logger.log_ec2_state(dict, i)}\n'
        return body
    
    def format_end_state(self): 
        action, state = self.get_verb()
        end_intro = '\n-------------------------------------------------------'
        end_intro += f'{Logger.intro(action, state)}'
        state_keys = EC2Instance.get_end_state(self.subject)
        index = 0
        for i in state_keys:
            end_intro += f"\n{self.phases[index].upper()}\n-----------------------\n"
            end_intro += f'{Logger.log_status(i, action)}' 
            index += 1
        return end_intro
    
    def get_verb(self):
        if 'start' in self.subject.lower():
                action = 'start'
        else:
            action = 'stop'
        if 'success' in self.subject.lower():
            state = 'success'
        else:
            state = 'fail'
        return action, state
