
import sys, json

class Processor:
    def __init__(self):
        self.me = {
            'name':'hordesman',
            'author': 'Chad Bailey (https://github.com/ChadBailey)',
            'url': 'https://github.com/ChadBailey/hordesman'
        }
        self.game_data = [
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
        self.items = [
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
        self.user_db = {
            '': {
                'groups': ['anonymous','unregistered'],
                'whitelisted_commands':['help']
            },
            'admin': {
                'groups': ['admins'],
                'blacklisted_commands':[]
            }
        }
        self.user_mapper = [
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
        self.state = {
            'confirm': None,
            'confirm_callback': None, #Function to call on confirmation
            'deny_callback': None #Function to call on denial
        }
        self.md = {
            'raw': '',
            'tokens': [],
            'campaign': 1,
            'conversion_rate':10,
            'cmd': '',
            'params': [],
            'username': '',
            'chatroom': '',
            'triggers':[],
            'trigger_used':'',
            'session_id':0,
            'registered': False,
            'authenticated': False,
        }
        self.cmd_mapper = [
            {
                'cmd': '',
                'aliases': [],
                'usage':'N/A',
                'description': 'Default command (ran if no other commands match)',
                'function': self.cmd_default
            },
            {
                'cmd': 'yes',
                'aliases': ['y'],
                'usage':f"{self.md['trigger_used']}yes",
                'description':f"Response to question asked by {self.me['name']}",
                'function': self.cmd_y
            },
            {
                'cmd': 'no',
                'aliases': ['n'],
                'description':f"Response to question asked by {self.me['name']}",
                'usage':f"{self.md['trigger_used']}no",
                'function': self.cmd_n
            },
            {
                'cmd': 'help',
                'aliases': ['h'],
                'description': "Shows all commands if no command specified, otherwise provides help on [command]",
                'usage':f"{self.md['trigger_used']}help [command]",
                'function': self.cmd_help
            },
            {
                'cmd': 'quit',
                'aliases': ['q','k','kill','die','exit','sleep','dismiss'],
                'description': "All good things must come to an end...",
                'usage':f"{self.md['trigger_used']}quit",
                'function': self.cmd_quit
            },
            {
                'cmd': 'about',
                'aliases': ['info'],
                'description': f"Shows information about {self.me['name']}",
                'usage':f"{self.md['trigger_used']}about",
                'function': self.cmd_about
            },
            {
                'cmd': 'deposit',
                'aliases': [],
                'description': f"Deposit money into the currently active bank",
                'usage':f"{self.md['trigger_used']}deposit [amount]",
                'function': self.cmd_deposit
            },
        ]

    def processor(self,state,metadata):
        lc = lambda token: [ x.lower() for x in token ]
        self.md.update(metadata)
        self.state = state
        if len(self.md['tokens']) > 0:
            self.md['cmd'] = self.md['tokens'][0].lower()
        else:
            self.md['cmd'] = ''

        self.md['params'] = lc(self.md['tokens'][1:])
        return self.fire_cmd()

    def check_privilege(self,cmd):
        user = self.user_db[self.md['username']]
        if 'whitelisted_commands' in user.keys():
            if cmd in user['whitelisted_commands']:
                return True
            else:
                return False
        if 'blacklisted_commands' in user.keys():
            if cmd not in user['blacklisted_commands']:
                return True
            else:
                return False

    def fire_cmd(self):
        cmd = self.md['cmd']
        for cmd_obj in self.cmd_mapper:
            if cmd == cmd_obj['cmd'] or cmd in cmd_obj['aliases']:
                self.cmd_obj = cmd_obj
                if self.check_privilege(cmd_obj['cmd']):
                    return cmd_obj['function']()
                else:
                    return 'Access Denied. Go cry to mommy'

        # If not found, fire default command
        cmd = ''
        for cmd_obj in self.cmd_mapper:
            if cmd == cmd_obj['cmd'] or cmd in cmd_obj['aliases']:
                self.cmd_obj = cmd_obj
                if self.check_privilege(cmd_obj['cmd']):
                    return cmd_obj['function']()
                else:
                    return 'Access Denied. Go cry to mommy'

    def cmd_default(self):
        return "Sorry, I don't understand. For a list of available commands please type 'help'"

    def cmd_help(self):
        if len(self.md['params']) == 0:
            result = "Here is a list of available commands:"
            for cmd_obj in self.cmd_mapper:
                result += f'''
Command: {cmd_obj['cmd']}
Aliases: {','.join(cmd_obj['aliases'])}
Usage: {cmd_obj['usage']}
Description: {cmd_obj['description']}
'''
            return result
        else:
            cmd = self.md['params'][0]
            for cmd_obj in self.cmd_mapper:
                if cmd == cmd_obj['cmd'] or cmd in cmd_obj['aliases']:
                    return f'''\
Command: {cmd_obj['cmd']}
Aliases: {','.join(cmd_obj['aliases'])}
Usage: {cmd_obj['usage']}
Description: {cmd_obj['description']}
'''

    def cmd_about(self):
        result = ''
        for k,v in self.me.items():
            result += f"{k}: {v}\n"
        return result

    def cmd_y(self):
        if self.state['confirm'] is None:
            return "I didn't ask you anything"
        self.state['confirm'] = None
        if self.state['confirm_callback']:
            func = self.state['confirm_callback']
            self.state['confirm_callback'] = None
            self.state['deny_callback'] = None
            if func: return func()
        return ''

    def cmd_n(self):
        if self.state['confirm'] is None:
            return "I didn't ask you anything"
        self.state['confirm'] = None
        if self.state['deny_callback']:
            func = self.state['deny_callback']
            self.state['confirm_callback'] = None
            self.state['deny_callback'] = None
            if func: return func()
        return ''

    def cmd_quit(self):
        self.state['confirm'] = True
        self.state['confirm_callback'] = self.quit
        self.state['deny_callback'] = lambda: "whew, you had me worried there for a moment *nervous laughter*"
        return "Quit? Are you sure?"

    def quit(self):
        sys.exit(0)

    def cmd_deposit(self):
        return self.get_value(self.md['params'])

    def get_value(self,tokens):
        gold = 0
        silver = 0
        copper = 0
        head = 0
        value = 0
        for token in tokens:
            for char in token:
                char = char.lower()
                if char == '': pass
                elif char in ['g','gold']:
                    gold = head * self.md['conversion_rate'] * self.md['conversion_rate']
                    head = 0
                elif char in ['s','silver']:
                    silver = head * self.md['conversion_rate']
                    head = 0
                elif char in ['c','copper']:
                    copper = head
                    head = 0
                else:
                    try:
                        head += int(char)
                    except ValueError:
                        return f"Unable to convert {''.join(tokens)} into currency!"
        value = (
            gold * self.md['conversion_rate'] * self.md['conversion_rate']
        ) + (
            silver * self.md['conversion_rate']
        ) + (
            copper
        )
        return value


#############################################################
# TODO: Move to commandline.py / make structure more better #
#############################################################

import sys, nltk

def main():
    print('Well met, mortal! Enter a command (type help for command list)')
    pc = Processor()
    while True:
        raw = input('')
        tokens = nltk.word_tokenize(raw)
        state = pc.state
        md = {
            'raw': raw,
            'tokens': tokens,
            'username': 'admin',
            'campaign': 1,
            'conversion_rate':10,
            'chatroom': '',
            'triggers': [],
            'trigger_used': '',
            'session_id': 0,
            'registered': False,
            'authenticated': False
        }
        print(pc.processor(state,md))

if __name__ == '__main__':
    main()