#from keep_alive import keep_alive
import os
import discord
from discord.ext import commands

from contests.getupdates import get_updates
import db.server_data as server_data
import dscrd.prw as prw
from dscrd.embds import hi_guild

discord_token = os.environ['discord_senpai_bot_secret_key']

intents = discord.Intents.all()
intents.members = True
DEFAULT_PREFIX = "senpai "

def get_prefix(bot_obj, message) -> str:
    # a custom prefix can be retrieved with the guild's ID
    try:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

    except AttributeError:  # triggered when command is invoked in dms
        return DEFAULT_PREFIX

    except KeyError:  # triggered when the server prefix has never been changed
        return DEFAULT_PREFIX
    
client = commands.Bot(command_prefix=get_prefix, intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print('bot is running..')
    await get_updates(client)

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
    
@client.event
async def on_guild_remove(guild):
    try:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=2)
    except KeyError:  # the server never changed the default prefix
        pass

################################COMMANDS########################

@client.command(aliases=["PREFIX", "Prefix", "pREFIX"])
@has_permissions(administrator=True)
async def prefix(ctx, new_prefix: str):

    if ctx.guild is None:
        await ctx.reply("**You cannot change the prefix outside of a server!**")
        return

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = new_prefix

    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=2)

    await ctx.send(f"**Prefix changed to {new_prefix}**")

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("**Incorrect usage!\n"
                        f"Example: {get_prefix(client, ctx)}prefix .**")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("**You do not have the permission to change the server prefix!**")

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
############################################################################

@client.group(invoke_without_command = True)
async def help(ctx):
    em= discord.Embed(title="Help!",description="Hi there, my prefix is `'senpai '`.\nFollowing are all the commands, use `senpai help <command>` for extended information on a command.", color=ctx.author.color)
    em.add_field(name="Admin commands: ", value="checkchannel, alterchannel")
    em.add_field(name="General commands: ",value = "meme")

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

@client.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        em = discord.Embed(title="Error!!!", description="Command not found.", color=ctx.author.color) 
        await ctx.send(embed=em)


#keep_alive()

client.run(discord_token)
