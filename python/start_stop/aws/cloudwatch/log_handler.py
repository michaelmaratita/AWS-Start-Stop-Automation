class Logger:
    @staticmethod
    def log_action(instances, list, action):
        ref = {
            'stop': 'Stopping',
            'start': 'Starting'
        }
        for i, meta in instances.items():
            if meta['InstanceId'] in list:
                print(f'{ref[action]}: {i} ({instances[i]['InstanceId']})')

    @staticmethod
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
        abort += f'ABORTING {abort_dict[action]['v2']}.\nPlease validate serve'
        abort += f'r states in AWS Console.\n {instance_list}' 
        return abort

    @staticmethod
    def log_validation(instance_list):
        print(f'Validating servers state: {instance_list}')

    @staticmethod
    def log_intance_state(meta, i):
        return f'Server: {i} ({meta[i]['InstanceId']}) is {meta[i]['State']}'
    
    @staticmethod
    def log_max_validations(dictionary):
        cw_log = f'Please check the Instance Status and Systems Status for the'
        cw_log += f' following servers:\n\n{dictionary}'
        print(cw_log)

    @staticmethod
    def intro(action, state):
        intro = {
            'start': {
                'success': '\nAll servers have been successfully started.\n',
                'fail': '\nFailed to start all servers.\n'
            },
            'stop': {
                'success': '\nAll servers have been successfully shut down.\n',
                'fail': '\nFailed to stop all servers.\n'
            }
        }
        return intro[action][state]

    @staticmethod
    def log_status(dictionary, action):
        if action == 'start':
            return Logger.format_log_status_start(dictionary)
        else:
            status = ''
            for i in dictionary:
                log1 = Logger.format_state_log(dictionary, i)
                status += f'{log1}.\n'
            return status
    
    @staticmethod
    def format_log_status_start(dictionary):
        status = ''
        for i in dictionary:
            log1 = Logger.format_state_log(dictionary, i) 
            log2 = Logger.format_start_log(dictionary, i)
            status += f'{log1}.\n{log2[0]}'
            status += f' | {log2[1]}\n'
        return status

    @staticmethod
    def format_start_log(dictionary, i):
        log = {
                'i_status': f'{i} ({dictionary[i]['InstanceId']}): Instan' + \
                f'ce Status: {dictionary[i]['InstanceStatus']}',
                's_status': f'System Status: ' + \
                f'{dictionary[i]['SystemStatus']}\n'
            }
        return log['i_status'],log['s_status']
    
    @staticmethod
    def format_state_log(dictionary, i):
        return f'{i} is in a {dictionary[i]['State']} state'
