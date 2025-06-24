from start_stop.main import pre_check
from start_stop.aws.sns_handler import SNSHandler


def lambda_handler(event, context):
    if event['send_mail']:
        sns = SNSHandler(event)
        sns.send_mail()
        return {
            'statusCode': 200
        }
    elif event['next_phase']:
        next_phase, initial_state = pre_check(event)
        return {
            'statusCode': 200,
            'next_phase': next_phase,
            'initial_state': initial_state
        }
    return {
        'statusCode': 200,
        'next_phase': event['next_phase']
    }
