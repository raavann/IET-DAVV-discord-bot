import os
import discord
from bs4 import BeautifulSoup

discord_token = os.environ['token']

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_member_join(member):
    await member.send("Welcome!")

@client.event
async def on_ready():
  print('bot running..')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    

client.run(discord_token)