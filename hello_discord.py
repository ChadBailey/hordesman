import os, dotenv, discord

dotenv.load_dotenv()

client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')


client.run(os.getenv('DISCORD_TOKEN'))