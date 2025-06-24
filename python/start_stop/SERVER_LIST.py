def server_lists():
    return [

####### DEV APP #########
        [
        'test1',
        'test4', 
        'test5',
        'test19'
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

def environments():
    return [
            "dev app servers",
            "test app servers",
            "preprod app servers",
            "dev db servers",
            "test db servers",
            "preprod db servers"
            ]
