import sys, nltk
from bot.bot import Processor

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
            'conversion_rate':100,
            'chatroom': '',
            'triggered': False,
            'triggers': ['!','.'],
            'session_id': 0,
            'registered': False,
            'authenticated': False
        }
        print(pc.processor(state,md))

if __name__ == '__main__':
    main()

