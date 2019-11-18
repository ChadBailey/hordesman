# from . import dnd

# {
#     'cmd': 'about',
#     'aliases': ['info'],
#     'description': f"Shows information about {self.binding['name']}",
#     'usage':f"{self.md['trigger_used']}about",
#     'function': self.cmd_about
# },

class about:
    '''Shows information about corebot.'''
    aliases = ['info']
    usage = 'about'
    @staticmethod
    def func(context):
        return f'''\
Name: CoreBot
Author: Chad Bailey (https://github.com/ChadBailey)
URL: https://github.com/ChadBailey/hordesman
'''

# {
#     'cmd': '',
#     'aliases': [],
#     'usage':'N/A',
#     'description': 'Default command (ran if no other commands match). Requires `default_trigger` to be set to `True`',
#     'function': self.cmd_default
# },

class default:
    '''Default command (ran if no other commands match). Requires `default_trigger` to be set to `True`'''
    aliases = ['']
    @staticmethod
    def func(context):
        c = context
        if c.binding['offer_suggestions_percent'] is not None:
            if c.suggested['pcnt'] > c.binding['offer_suggestions_percent'] and c.md['cmd'] != '':
                return f'''"{c.md['trigger_used']}{c.md['cmd']}" not understood. Did you mean "{c.md['trigger_used']}{c.suggested['cmd']}"?'''

        if c.binding['default_trigger']:
            return "Sorry, I don't understand. For a list of available commands please type 'help'"

# {
#     'cmd': 'help',
#     'aliases': ['h'],
#     'description': "Shows all commands if no command specified, otherwise provides help on [command]",
#     'usage':f"{self.md['trigger_used']}help [command]",
#     'function': self.cmd_help
# },
class help:
    '''Shows all commands if no command specified, otherwise provides help on [command]'''
    usage = 'help [command]'
    aliases = ['h','?']
    @staticmethod
    def func(context):
        if len(context.md['params']) == 0:
            result = "Here is a list of available commands:"
            for cmd_obj in context.cmds:
                result += f'''
Command: {cmd_obj[0]}
Aliases: {','.join(getattr(cmd_obj[1],'aliases',['None']))}
Usage: {getattr(cmd_obj[1],'usage','N/A')}
Description: {cmd_obj[1].__doc__}
'''
            return result
        else:
            cmd = context.md['params'][0]
            for cmd_obj in context.cmds:
                if cmd == cmd_obj[0] or cmd in cmd_obj[1].aliases:
                    return f'''\
Command: {cmd_obj[0]}
Aliases: {','.join(getattr(cmd_obj[1],'aliases',['None']))}
Usage: {getattr(cmd_obj[1],'usage','N/A')}
Description: {cmd_obj[1].__doc__}
'''

# {
#     'cmd': 'yes',
#     'aliases': ['y'],
#     'usage':f"{self.md['trigger_used']}yes",
#     'description':f"Response to question asked by {self.binding['name']}",
#     'function': self.cmd_y
# },
class yes:
    f'''Response to question asked by corebot'''
    usage = 'yes'
    aliases = ['y']
    @staticmethod
    def func(context):
        if context.state['confirm'] is None:
            return "I didn't ask you anything"
        context.state['confirm'] = None
        if context.state['confirm_callback']:
            func = context.state['confirm_callback']
            context.state['confirm_callback'] = None
            context.state['deny_callback'] = None
            if func: return func()
        return ''

# {
#     'cmd': 'no',
#     'aliases': ['n'],
#     'description':f"Response to question asked by {self.binding['name']}",
#     'usage':f"{self.md['trigger_used']}no",
#     'function': self.cmd_n
# },
class no:
    f'''Response to question asked by corebot'''
    aliases = ['n']
    usage = 'no'
    @staticmethod
    def func(context):
        if context.state['confirm'] is None:
            return "I didn't ask you anything"
        context.state['confirm'] = None
        if context.state['deny_callback']:
            func = context.state['deny_callback']
            context.state['confirm_callback'] = None
            context.state['deny_callback'] = None
            if func: return func()
        return ''


# {
#     'cmd': 'quit',
#     'aliases': ['q','k','kill','die','exit','sleep','dismiss'],
#     'description': "All good things must come to an end...",
#     'usage':f"{self.md['trigger_used']}quit",
#     'function': self.cmd_quit
# },
class quit:
    '''All good things must come to an end...'''
    aliases = ['q','k','kill','die','exit','sleep','dismiss']
    usage = 'quit'
    @staticmethod
    def func(context):
        context.state['confirm'] = True
        context.state['confirm_callback'] = context.quit
        context.state['deny_callback'] = lambda: "whew, you had me worried there for a moment *nervous laughter*"
        return "Quit? Are you sure?"


# {
#     'cmd': 'trigger',
#     'aliases': ['t'],
#     'description': f"View or set the trigger for the current binding",
#     'usage':f"{self.md['trigger_used']}trigger [add/remove] [trigger value]",
#     'function': self.cmd_trigger
# },
class trigger:
    '''View or set the trigger for the current binding'''
    aliases = ['t']
    usage = 'trigger [add/remove] [trigger value]'
    @staticmethod
    def func(context):
        if len(context.md['params']) == 0:
            return f"Current trigger(s): `{'`,`'.join(context.binding['triggers'])}`"
        else:
            raise NotImplementedError("Support for changing triggers is not yet implemented")
