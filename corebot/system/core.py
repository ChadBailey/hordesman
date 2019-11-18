import sys, json, nltk, inspect
from difflib import SequenceMatcher

from corebot.system import cmd
from corebot.system.plugins import dnd

from corebot.system.data_models import \
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
        self.game_data = game_data
        self.items = items
        self.user_db = user_db
        self.user_mapper = user_mapper
        self.state = state
        self.md = md
        self.cmds = [ f for f in inspect.getmembers(cmd) if '__' not in f[0] ]
        self.cmds += [ f for f in inspect.getmembers(dnd) if '__' not in f[0] ]
        # plugins = [cmd,dnd]
        # for plugin in plugins:
        #     for cmd in inspect.getmembers(plugin):
        #         if '__' not in cmd[0]:
        #             self.cmds += cmd


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
        all_cmds = []
        highest_match = {
            'pcnt': 0,
            'cmd': ''
        }
        for cmd_obj in self.cmds:
            all_cmds += [cmd_obj[0]]
            try:
                all_cmds += cmd_obj[1].aliases
            except AttributeError:
                pass
        for cmd_txt in all_cmds:
            match = SequenceMatcher(None, cmd_txt, cmd).ratio()
            if match > highest_match['pcnt']:
                highest_match['pcnt'] = match
                highest_match['cmd'] = cmd_txt
        return highest_match

    def fire_cmd(self):
        # Get command requested
        cmd = self.md['cmd']

        # Find suggested commands (in case this was a slight-typo)
        suggested = self.find_cmd()
        self.suggested = suggested

        # If suggested percent match is greater than the match percent, replace
        # it as if the user had typed the correct command
        if suggested['pcnt'] > self.binding['cmd_match_percent']:
            cmd = suggested['cmd']

        # check cmds for matches (new way)
        # inspect.getmembers(cmd) returns a tuple containing
        # 0: string of class name
        # 1: class
        for cmd_obj in self.cmds:
            if cmd == cmd_obj[0] or cmd in getattr(cmd_obj[1],'aliases',[]):
                # Must check against the command name, not the alias
                if self.check_privilege(cmd_obj[0]):
                    return cmd_obj[1].func(self) # Call discovered function with self
                else:
                    return 'Access Denied. Go cry to mommy'

        # If not found, fire default command
        cmd = 'default'
        for cmd_obj in self.cmds:
            if cmd == cmd_obj[0] or cmd in cmd_obj[1].aliases:
                # Must check against the command name, not the alias
                if self.check_privilege(cmd_obj[0]):
                    return cmd_obj[1].func(self) # Call discovered function with self
                else:
                    return 'Access Denied. Go cry to mommy'

    def quit(self):
        sys.exit(0)
