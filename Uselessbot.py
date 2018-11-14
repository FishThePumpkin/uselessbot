import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import youtube_dl


client = commands.Bot(command_prefix = "!")
client.remove_command('help')
status = ['Viv\'s', 'voice', 'is', 'so', 'nice', 'owo']

players = {}

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)
    
    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(2)


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Online!'))
    print("Bot is ready")

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Exhibitionist')
    await client.add_roles(member, role)

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has added {} to the message: ``{}``'.format(user.name, reaction.emoji, reaction.message.content))

@client.event
async def on_reaction_remove(reaction,user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has removed {} to the message: ``{}``'.format(user.name, reaction.emoji, reaction.message.content))
    

@client.command(pass_context=True)
async def addgame(ctx, *game):
    gamestr = ''
    for word in game:
        gamestr += word
        gamestr += ' '
    status.append(gamestr)
    await client.say('Game changed to **'+gamestr+'**')
                                         

@client.command()
async def ping():
    await client.say('Pong!')


@client.command()
async def say(*args):
    output = ' '
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.command(pass_context=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount)+' Messages deleted')

@client.command(pass_context=True)
async def game(ctx, *game):
    gamestr = ''
    for word in game:
        gamestr += word
        gamestr += ' '
    await client.change_presence(game=discord.Game(name=gamestr))
    await client.say('Game changed to **'+gamestr+'**')

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command()
async def displayembed():
    embed = discord.Embed(
        title = 'Title',
        description = 'This is a description',
        color = discord.Color.blue()
    )

    embed.set_footer(text='This is a footer')
    embed.set_image(url='https://p1.ssl.qhimg.com/t0156bfabfdcaa3b0bc.jpg')
    embed.set_thumbnail(url='https://p0.ssl.qhimg.com/t010d05eabcb0b64372.jpg')
    embed.set_author(name='Author name',
    icon_url='https://p0.ssl.qhimg.com/t0129f3a42fc16517ef.jpg')
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)


    await client.say(embed=embed)
    
@client.command(pass_context=True)
async def help(ctx):

    embed = discord.Embed(
        color = discord.Color.orange()
    )

    embed.set_author(name='**Help**')
    embed.add_field(name='**!addgame <string>**', value='Adds a game to the bot\'s rotation.', inline=False)
    embed.add_field(name='**!clear <value>**', value='Clears chat messages', inline=False)
    embed.add_field(name='**!ping**', value='Returns Pong!', inline=False)
    
    embed.add_field(name='**!say <string>**', value='Tells the bot to say something.', inline=False)
    
    embed.add_field(name='**placeholder**', value='placeholder', inline=False)
    embed.add_field(name='**placeholder**', value='placeholder', inline=False)

    await client.say(embed=embed) #send_message(author, embed=embed)

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


@client.command()
async def logout():
    await client.logout()

client.loop.create_task(change_status())


client.run(os.environ['BOT_TOKEN'])
