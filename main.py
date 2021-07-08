import os

import discord
from discord.utils import find
from discord.ext import commands,tasks
import asyncio
from datetime import datetime,timedelta

import contests.getupdates

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = 'senpai ',intents=intents)


