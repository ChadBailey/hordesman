import sys

def deposit(g,s,c):
    assert type(g) == 'int', 'Gold must be an integer'
    assert type(s) == 'int', 'Silver must be an integer'
    assert type(c) == 'int', 'Copper must be an integer'
        

def confirm(cmd):
    resp = input(f'{cmd}, Are you sure? [Y/n]\n').lower()
    if resp in ['','yes','y']:
        return True
    else:
        return False

def main(cmd):
    if cmd == 'quit':
        if confirm(cmd):
            sys.exit(0)
    elif cmd == 'deposit':
        pass
    else:
        return "Sorry, I don't understand. For a list of available commands please type 'help'"

if __name__ == '__main__':
    while True:
        cmd = input('What would you like to do?\n').lower()
        print(main(cmd))
