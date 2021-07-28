import random
from discord import Embed, Colour
import json


obj = json.loads((open('./dscrd/data.json','r',encoding='utf-8')).read())

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

def embed_1drem(cont):
    desc = random_salutation() + '\n{name} will start tomorrow @{st}! \n[Click here]({link}) to know more! \n{cheer}'.format(name=cont.name, link= cont.link, st = str(cont.start_time.strftime("%I:%M %p")).lower(),cheer= random_greeting())
    embd = Embed(title = "Contest starts tomorrow!", description=desc,colour=Colour.dark_blue())
    embd.set_thumbnail (url = logo[cont.link[12:20]])
   
    return embd

def embed_1hrem(cont,avtr):
    desc = random_salutation() + '\n{name} will start soon @{st}! \n[Click here]({link}) to join the contest! \n{cheer}'.format(name=cont.name, link=cont.link,st=str(cont.start_time.strftime("%I:%M %p")).lower(),cheer= random_greeting())
    embd = Embed(title = "Contest about to start!", description = desc,colour= Colour.green())
    embd.set_thumbnail(url=logo[cont.link[12:20]] )
    embd.set_footer(text = str(random_cheer()), icon_url = avtr)

    return embd

def embed_contest_ended(cont):
    desc = random_salutation()+'\n{name} has ended.\n'.format(name=cont.name) + random.choice(ended)
    embd = Embed(title = "Contest has ended!", description = desc,colour= Colour.red())
    embd.set_thumbnail (url = logo[cont.link[12:20]])

    return embd

def hi_guild(gld):
    embd = Embed(description = "_Thank you for adding me. I'm glab to be here!_\nYou can see a list of commands by typing `senpai help`",
    colour=Colour.teal())

    embd.add_field(name="About me!", value="__Senpai__ in Japanese stands for " + "_'Elder'_" + ", someone who watches over you. And that's exactly what I'll do.")
    embd.set_thumbnail(url = gld.me.avatar_url)
    embd.set_author(name = 'Senpai',icon_url=gld.me.avatar_url)
    embd.add_field(name="My Job!", value="I'll be sending regular updates on Codechef and Codeforces Contest on the channel specified by admin.\nType `senpai help` to know more.")

    return embd

def embd_next_contest(cont,avtr):
    desc='{salut}\nThe next contest, i.e. {cn}, will start on {dt}.\n[Click here]({link}) to know more!'.format(salut=random_salutation(),cn = cont.name, dt = cont.start_time.strftime("%d %b @%I:%M %p"),link=cont.link)
    embd = Embed(title="Upcoming contest!", description=desc,colour= Colour.purple())
    embd.set_thumbnail (url = logo[cont.link[12:20]])

    embd.set_footer(text = str(random_greeting()), icon_url = avtr)
    return embd