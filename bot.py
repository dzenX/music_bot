import discord

TOKEN = ''

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}, wanna some music?'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!yes'):
        msg = 'Omae wa mou shindeiru'.format(message)
        await client.send_message(message.channel, msg)
        msg = 'NO NI'.format(message)
        await client.send_message(message.channel, msg)
        msg = 'sry, no music yet'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)