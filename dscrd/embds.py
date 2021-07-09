import random
from discord import Embed, Colour
import json

obj = json.loads((open('data.json','r',encoding='utf-8')).read())

salutation = (obj["salutation"])
ended = (obj["ended"])
logo = (obj["logo"])
greetings = (obj["greetings"])
cheer = (obj["cheer"])


def random_salutation():
    return random.choice(salutation)

def random_cheer():
    return random.choice(cheer)

def random_greeting():
    return random.choice(greetings)

def embed_1drem(cont,ctx):
    desc = random_salutation() + '\n{name} will start tomorrow @{st}! \n[Click here]({link}) to know more! \n{cheer}'.format(name=cont.name, link= cont.link, st = str(cont.start_time.strftime("%I %p")).lower(),cheer= random_greeting())
    embd = Embed(title = "Contest update!", description=desc,colour=Colour.dark_blue())
    embd.set_thumbnail (url = logo[cont.link[16]])
    embd.set_footer(text = str(random_cheer()), icon_url = ctx.guild.me.avatar_url)
   
    return embd

def embed_1hrem(cont,ctx):
    desc = random_salutation() + '\n{name} will start {tod_hr} @{st}! \n[Click here]({link}) to join the contest! \n{cheer}'.format(name=cont.name,tod_hr=random.choice(['today','in an hour']), link=cont.link,st=str(cont.start_time.strftime("%I %p")).lower(),cheer= random_greeting())
    embd = Embed(title = "Contest update!", description = desc,colour= Colour.green())
    embd.set_thumbnail(url=logo[cont.link[16]] )
    embd.set_footer(text = str(random_cheer()), icon_url = ctx.guild.me.avatar_url)

    return embd

def embed_contest_ended(cont):
    desc = random_salutation()+'\n{name} has ended.\n'.format(name=cont.name) + random.choice(ended)
    embd = Embed(title = "Contest update!", description = desc,colour= Colour.red())
    embd.set_thumbnail (url = logo[cont.link[16]])

    return embd

def hi_guild(gld):
    embd = Embed(description = "_Thank you for adding me. I'm glab to be here!_\nYou can see a list of commands by typing `senpai help`",
    colour=Colour.teal())

    embd.add_field(name="About me!", value="__Senpai__ in Japanese stands for " + "_'Elder'_" + ", someone who watches over you. And that's exactly what I'll do.")
    embd.set_thumbnail(url = gld.me.avatar_url)
    embd.set_author(name = 'Senpai',icon_url=gld.me.avatar_url)
    embd.add_field(name="My Job!", value="I'll be sending regular updates on Codechef and Codeforces Contest on the channel specified by admin.\nType `senpai help` to know more.")

    return embd

def altchnl_done():
    pass

def altchnl_notdone():
    pass

def no_chnl_set():
    pass

def chnl_set():
    pass