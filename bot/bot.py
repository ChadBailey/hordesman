import sys, json, nltk

from difflib import SequenceMatcher

from .data_models import \
    about, \
    game_data, \
    items, \
    user_db, \
    user_mapper, \
    state, \
    md

class Processor:
    def __init__(self,binding):
        if len(binding['triggers']) == 0:
            raise ValueError("Error: No triggers specified for binding. If you want to trigger off of everything, you must specify a blank trigger via a blank string like: `['']`")
        self.binding = binding
        self.about = about
        self.game_data = game_data
        self.items = items
        self.user_db = user_db
        self.user_mapper = user_mapper
        self.state = state
        self.md = md
        self.cmd_mapper = [
            {
                'cmd': '',
                'aliases': [],
                'usage':'N/A',
                'description': 'Default command (ran if no other commands match). Requires `default_trigger` to be set to `True`',
                'function': self.cmd_default
            },
            {
                'cmd': 'yes',
                'aliases': ['y'],
                'usage':f"{self.md['trigger_used']}yes",
                'description':f"Response to question asked by {self.binding['name']}",
                'function': self.cmd_y
            },
            {
                'cmd': 'no',
                'aliases': ['n'],
                'description':f"Response to question asked by {self.binding['name']}",
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
                'description': f"Shows information about {self.binding['name']}",
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
            {
                'cmd': 'exchange',
                'aliases': [],
                'description': f"Exchange your money for higher denominations",
                'usage':f"{self.md['trigger_used']}exchange 10g30s99c",
                'function': self.cmd_exchange
            },
            {
                'cmd': 'trigger',
                'aliases': ['t'],
                'description': f"View or set the trigger for the current binding",
                'usage':f"{self.md['trigger_used']}trigger [add/remove] [trigger value]",
                'function': self.cmd_trigger
            },
        ]

    def processor(self,state,metadata):
        try:
            # lc = lambda token: [ x.lower() for x in token ]
            self.md.update(metadata)
            self.state = state
            for trigger in self.binding['triggers']:
                trigger_len = len(trigger)
                trigger_check = self.md['raw'][0:trigger_len]
                if trigger_check == trigger:
                    self.md['trigger_used'] = trigger_check
                    self.md['raw_wo_trigger'] = self.md['raw'][trigger_len:]
                    self.md['tokens'] = nltk.word_tokenize(self.md['raw_wo_trigger'])
                    if len(self.md['tokens']) > 0:
                        self.md['cmd'] = self.md['tokens'][0].lower()
                    else:
                        self.md['cmd'] = ''
                    self.md['triggered'] = True
                    break
            if self.md['triggered']:
                # Maybe: lower the tokens? i think we should push that out to individual commands
                self.md['params'] = self.md['tokens'][1:]
                return self.fire_cmd()
        except Exception as e:
            return f"Oh dear, something went wrong:\n\n{e}"

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

    def find_cmd(self):
        cmd = self.md['cmd']
        # all_cmds = [ [cmd_obj['cmd']] + cmd_obj['aliases'] for cmd_obj in self.cmd_mapper ]
        all_cmds = []
        highest_match = {
            'pcnt': 0,
            'cmd': ''
        }
        for cmd_obj in self.cmd_mapper:
            all_cmds += [cmd_obj['cmd']]
            all_cmds += cmd_obj['aliases']
        for cmd_txt in all_cmds:
            match = SequenceMatcher(None, cmd_txt, cmd).ratio()
            if match > highest_match['pcnt']:
                highest_match['pcnt'] = match
                highest_match['cmd'] = cmd_txt
        return highest_match

    def fire_cmd(self):
        cmd = self.md['cmd']
        suggested = self.find_cmd()
        self.suggested = suggested
        if suggested['pcnt'] > self.binding['cmd_match_percent']:
            cmd = suggested['cmd']
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
        if self.binding['offer_suggestions_percent'] is not None:
            if self.suggested['pcnt'] > self.binding['offer_suggestions_percent'] and self.md['cmd'] != '':
                return f'''"{self.md['trigger_used']}{self.md['cmd']}" not understood. Did you mean "{self.md['trigger_used']}{self.suggested['cmd']}"?'''

        if self.binding['default_trigger']:
            return "Sorry, I don't understand. For a list of available commands please type 'help'"

    def cmd_help(self):
        if len(self.md['params']) == 0:
            result = "Here is a list of available commands:"
            for cmd_obj in self.cmd_mapper:
                result += f'''
Command: {cmd_obj['cmd']}
Aliases: {','.join(cmd_obj['aliases'])}
Usage: {self.md['trigger_used']}{cmd_obj['usage']}
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
        for k,v in self.about.items():
            result += f"{k}: {v}\n"
        return result

    def cmd_trigger(self):
        if len(self.md['params']) == 0:
            return f"Current trigger(s): `{'`,`'.join(self.binding['triggers'])}`"
        else:
            raise NotImplementedError("Support for changing triggers is not yet implemented")

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
        return "Coming soon..."

    def cmd_exchange(self):
        return self.get_gsc(self.get_value(self.md['params']))

    def get_gsc(self,value):
        cr = self.md['conversion_rate']
        g,s,c = 0,0,0
        c += value % cr
        value = value - c
        s += int(value /cr) % cr
        value = value - (s * cr)
        g += int(value / (cr**2))

        return f'{g}g{s}s{c}c'

    def get_value(self,tokens):
        gold = 0
        silver = 0
        copper = 0
        head = ''
        value = 0
        for token in tokens:
            for char in token:
                char = char.lower()
                if char == '': pass
                elif char in ['g','gold']:
                    gold += int(head)
                    head = ''
                elif char in ['s','silver']:
                    silver += int(head)
                    head = ''
                elif char in ['c','copper']:
                    copper += int(head)
                    head = ''
                else:
                    try:
                        int(char)
                        head += char
                    except ValueError:
                        return f"Unable to convert {''.join(tokens)} into currency!"
        if head != '':
            return f"Unable to convert {''.join(tokens)} into currency!"
        value = (
            gold * (self.md['conversion_rate'] ** 2)
        ) + (
            silver * self.md['conversion_rate']
        ) + (
            copper
        )
        return value
