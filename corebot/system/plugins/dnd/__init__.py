# {
#     'cmd': 'deposit',
#     'aliases': [],
#     'description': f"Deposit money into the currently active bank",
#     'usage':f"{self.md['trigger_used']}deposit [amount]",
#     'function': self.cmd_deposit
# },
# def cmd_deposit(self):
#     return "Coming soon..."


# {
#     'cmd': 'exchange',
#     'aliases': [],
#     'description': f"Exchange your money for higher denominations",
#     'usage':f"{self.md['trigger_used']}exchange 10g30s99c",
#     'function': self.cmd_exchange
# }
class exchange:
    '''Exchange your money for higher denominations'''
    usage = 'exchange [#g][#s][#c]'
    @staticmethod
    def func(context):
        return exchange.get_gsc(context,context.get_value(context.md['params']))

    @staticmethod
    def get_gsc(context,value):
        cr = context.md['conversion_rate']
        g,s,c = 0,0,0
        c += value % cr
        value = value - c
        s += int(value /cr) % cr
        value = value - (s * cr)
        g += int(value / (cr**2))

        return f'{g}g{s}s{c}c'

    @staticmethod
    def get_value(context,tokens):
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
            gold * (context.md['conversion_rate'] ** 2)
        ) + (
            silver * context.md['conversion_rate']
        ) + (
            copper
        )
        return value
