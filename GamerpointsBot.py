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


#Commands


#Events
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(Message):
    await bot.process_commands(Message)






bot.run(os.getenv('GAMERPOINTS_BOT_TOKEN'))