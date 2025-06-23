import start_stop as ss

def lambda_handler(event, context):
    if event['send_mail']:
        ss.sns.send_mail(ss.sns(event))
        return {
            'statusCode': 200
        }
    elif event['next_phase']:
        next_phase, initial_state = ss.pre_check(event)
        return {
            'statusCode': 200,
            'next_phase': next_phase,
            'initial_state': initial_state
        }
    return {
        'statusCode': 200,
        'next_phase': event['next_phase']
    }
