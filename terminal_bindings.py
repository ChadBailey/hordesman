import sys, nltk
from bot.bot import Processor

binding = {
    'name':'Hordesman',
    'binding':'terminal',
    'triggers': [''],
    'cmd_match_percent': 0.7,
    'offer_suggestions_percent': 0,
    'default_trigger': True
}
pc = Processor(binding)

def main():
    print('Well met, mortal! Enter a command (type help for command list)')
    while True:
        raw = input('')
        tokens = nltk.word_tokenize(raw)
        state = pc.state
        md = {
            'raw': raw,
            'tokens': tokens,
            'username': 'admin',
            'campaign': 1,
            'conversion_rate':100,
            'chatroom': '',
            'session_id': 0,
            'registered': False,
            'authenticated': False
        }
        print(pc.processor(state,md))

if __name__ == '__main__':
    main()

