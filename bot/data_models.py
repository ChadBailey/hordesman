about = {
    'name': 'Hordesman Bot',
    'author': 'Chad Bailey (https://github.com/ChadBailey)',
    'url': 'https://github.com/ChadBailey/hordesman'
}
game_data = [
    {
        'campaign_id': 1,
        'campaign_name': 'Decent Avernus',
        'players': [1],
        'roll20_url':'https://app.roll20.net/campaigns/details/5397144/decent-avernus',
        'dnd_beyond_url': 'https://www.dndbeyond.com/campaigns/716014',
        'rules_id': 1,
        'conversion_rate':10,
        'banks': [
            {
                'description':'Party Bank',
                'creator':'admin',
                'owner':'admin',
                'can_deposit': [1],
                'can_withdrawl':[1],
                'slots': 16,
                'currency': 0,
                'items': [
                    {
                        'item_id':1,
                        'qty':2
                    }
                ]
            }
        ]
    }
]
items = [
    {
        'id':1,
        'name': 'Gold Necklace',
        'stack_size': 5,
        'value': 2500,
        'level': 1,
        'soulbound': [],
        'bind_on_pickup': False,
        'bind_on_equip': False
    },
    {
        'id':2,
        'name': 'Blackened Pearl Ring',
        'stack_size': 5,
        'value':12500,
        'level':1,
        'soulbound': [],
        'bind_on_pickup': False,
        'bind_on_equip': False
    }
]
user_db = {
    '': {
        'groups': ['anonymous','unregistered'],
        'whitelisted_commands':['help']
    },
    'admin': {
        'groups': ['admins'],
        'blacklisted_commands':[]
    }
}
user_mapper = [
    {
        'user':'',
        'aliases':'anonymous',
        'groups':[]
    },
    {
        'user': 'admin',
        'aliases': ['Kamel','Chad','Rapha'],
        'groups': ['admins','players']
    }
]
state = {
    'confirm': None,
    'confirm_callback': None, #Function to call on confirmation
    'deny_callback': None #Function to call on denial
}
md = {
    'raw': '',
    'tokens': [],
    'campaign': 1,
    'conversion_rate':10,
    'cmd': '',
    'params': [],
    'username': '',
    'chatroom': '',
    'triggered': False,
    'trigger_used':'',
    'session_id':0,
    'registered': False,
    'authenticated': False,
}
