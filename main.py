#from keep_alive import keep_alive
import os
import discord
from discord.ext import commands

import db.server_data as server_data
import dscrd.prw as prw
from dscrd.embds import hi_guild
from dscrd.embds import embd_next_contest

from contests.sendupdates import main_updates, get_next_contest

discord_token = os.environ['discord_senpai_bot_secret_key']

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = 'senpai ',intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print('bot is running..')
    await main_updates(client)

@client.event
async def on_guild_remove(guild):
    server_data.remove_serv(guild.id)

@client.event
async def on_guild_join(guild):
    channel_values = ['announcement','announcements','general']
    chnl =None
    for c in guild.text_channels:
        if (c.permissions_for(guild.me).send_messages==True):
            if c.name in channel_values:
                chnl = c
                break
            else:
                chnl = c
    server_data.insert_serv(guild.id, c.id)
    embd = discord.Embed(description= "Hie there :D, \nI will be sending updates on channel `{cx}` for your server `{s}`. \nTo change these settings type `senpai help` on the respective server!\nThanks <3!".format(cx=chnl.name,s=guild.name),color=discord.Color.orange())
    embd.set_thumbnail(url=client.user.avatar_url)
    await guild.owner.send(embed=embd)
    await c.send(embed=hi_guild(guild))

################################COMMANDSS########################
@client.command(name = "alterchannel", aliases = ["announcement="])
@commands.has_permissions(administrator = True)
async def alterchannel(ctx, given_name):
    notdone = True
    for channel in ctx.guild.channels:
        if (channel.name == given_name and channel.permissions_for(ctx.guild.me).send_messages ==True):
            await ctx.channel.send("Great!\nUpdates will now be sent on `{n}`. :)".format(n=given_name))
            server_data.update_serv(ctx.guild.id,channel.id)
            notdone = False
            break
    if(notdone):
        await ctx.channel.send("Oops!\nEither I don't have permission to send message to this channel or you have entered an incorrect name..\nPlease try again! :)")

@client.command(name='checkchannel',aliases=["announcement?"])
@commands.has_permissions(administrator=True)
async def check_channel(ctx):
    chnl = client.get_channel(server_data.get_chnl_by_serv(ctx.guild.id))
    if (chnl == None):
        await ctx.channel.send('Oops!\nNo channel has set.\nSet up channel using `senpai announcement= <channel name>` command.')
    else:
        await ctx.channel.send('Hola!\nUpdates will be sent on `{c}`.\nTo change this, use `senpai announcement= <channel name>` command.'.format(c=chnl.name))

@client.command(name='meme', aliases=["bleh","agh"])
async def meme(ctx):
    msg = await prw.send_meme()
    await ctx.channel.send(msg)

@client.command(name='update', aliases=["nextcontest"])
async def update(ctx):
    em =  embd_next_contest( get_next_contest(),ctx.guild.me.avatar_url )
    await ctx.send(embed=em)

#@---------------------------------------------------------------------------------------------

@client.group(invoke_without_command = True)
async def help(ctx):
    em= discord.Embed(title="Help!",description="Hi there, my prefix is `'senpai '`.\nFollowing are all the commands.\nUse `senpai help <command>` for extended information on a command.", color=ctx.author.color)
    em.add_field(name="Admin commands: ", value="checkchannel, alterchannel")
    em.add_field(name="General commands: ",value = "meme update")

    await ctx.send(embed=em)

@help.command()
async def checkchannel(ctx):
    em=discord.Embed(title="checkchannel (only admins)", description="Returns the channel on which updates would be sent.", color=ctx.author.color)
    em.add_field(name="Syntax", value="`senpai checkchannel`")
    em.add_field(name = "aliases", value="announcement? \n*Syntax* `senpai announcement?`")
    await ctx.send(embed=em)

@help.command()
async def alterchannel(ctx):
    em=discord.Embed(title="alterchannel (only admins)", description="Changes the channel on which updates are being sent!", color=ctx.author.color)
    em.add_field(name="Syntax", value="`senpai altchannel <new channel name>`")
    em.add_field(name = "aliases", value="announcement? \n*Syntax* `senpai announcement= <new channel name>`")
    await ctx.send(embed=em)

@help.command()
async def meme(ctx):
    em=discord.Embed(title="meme", description="Returns a meme on programming/coding", color=ctx.author.color)
    em.add_field(name="Syntax", value="`senpai meme`")
    em.add_field(name = "aliases", value="bleh, agh \n*Syntax* `senpai bleh` `senpai agh`")
    await ctx.send(embed=em)

@help.command()
async def update(ctx):
    em=discord.Embed(title="update", description="Returns the next recent Contest.", color=ctx.author.color)
    em.add_field(name="Syntax", value="`senpai update`")
    em.add_field(name = "aliases", value="nextcontest \n*Syntax* `senpai next contest`")
    await ctx.send(embed=em)

@client.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        em = discord.Embed(title="Error!!!", description="Command not found.", color=ctx.author.color) 
        await ctx.send(embed=em)


#keep_alive()

client.run(discord_token)
