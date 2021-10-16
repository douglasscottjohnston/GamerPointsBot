import discord
import discord.ext
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

#Credentials
load_dotenv('.env')

#Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-',intents=intents)

#Global variables
scoreboard = {}

#Commands
@bot.command
async def addUser(ctx, *, user):
  scoreboard[user] = 0

@bot.command
async def removeUser(ctx, *, user):
  del scoreboard[user]

@bot.command
async def wonGame(ctx, *, message):


@bot.command
async def addPoints(ctx, *, points):
  

@bot.command
async def removePoints(ctx, *, points):

#Events
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(Message):
    await bot.process_commands(Message)






bot.run(os.getenv('GAMERPOINTS_BOT_TOKEN'))