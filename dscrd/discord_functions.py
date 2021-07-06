import os
import discord
from bs4 import BeautifulSoup
import asyncio

##token
discord_token = os.environ['token']

##enable intents
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
##

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

client.run(discord_token)