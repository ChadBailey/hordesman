import os, dotenv, discord
import sys, nltk

dotenv.load_dotenv()

client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

pc = Processor()

@client.event
async def on_message(message):
    print(message)
    if message.author == client.user:
        return
    raw = message.content
    tokens = nltk.word_tokenize(raw)
    state = pc.state
    md = {
        'raw': raw,
        'tokens': tokens,
        'username': 'admin',
        'campaign': 1,
        'conversion_rate':10,
        'chatroom': '',
        'triggered': False,
        'triggers': ['/','.'],
        'session_id': 0,
        'registered': False,
        'authenticated': False
    }
    response = pc.processor(state,md)
    if response: await message.channel.send(response)


client.run(os.getenv('DISCORD_TOKEN'))