from SERVER_LIST import server_lists
from start_stop.aws.sns_handler import EC2Instance


def pre_check(event):
    instances = EC2Instance(server_lists()[event['phase_number']])
    if len(instances.names) > 0:
        return main(event, instances)
    return True, {"empty": True}
    
def main(event, instances):
    initial_state = instances.describe()
    print(event['cw_log_phase'].upper())
    instances.start_or_stop(event['action'])
    passed = get_validation_state(instances, event['action'])
    instances.instance_log_status(passed, event['action'])
    return passed, initial_state

def get_validation_state(instances, action):
        if action == 'start':
            return instances.validate_status(0, action)
        else:
            return instances.validation(0, action)
