import discord
import discord.ext
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

#Credentials
load_dotenv('.env')
GAMERPOINTS_BOT_TOKEN = os.getenv("GAMERPOINTS_BOT_TOKEN")

#Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-',intents=intents)

#Global variables
scoreboard = {}

notInMsg = " is not in the scoreboard, add them with the addUser command"

#Commands
@bot.command()
async def addUser(ctx, *members: commands.Greedy[discord.Member]):
  for member in members:
    if scoreboard.has_key(member):
      await ctx.send(member.id)

@bot.command()
async def removeUser(ctx, *members: commands.Greedy[discord.Member]):
  del scoreboard[user]

@bot.command()
async def wonGame(ctx, *members: commands.Greedy[discord.Member]):
  if scoreboard.has_key(user):
    scoreboard[user] += 10
    await ctx.channel.send(user + " gained 10 gamerpoints!")
  else:
    await ctx.channel.send(user + notInMsg)

@bot.command()
async def addPoints(ctx, *, user, points):
  if scoreboard.has_key(user):
    scoreboard[user] += points
    await ctx.channel.send(user + " gained %points gamerpoints!" % points)
  else:
    await ctx.channel.send(user + notInMsg)

@bot.command()
async def removePoints(ctx, *, user, points):
  if scoreboard.has_key(user):
    scoreboard[user] += points
    await ctx.channel.send(user + " gained %points gamerpoints" % points)
  else:
    await ctx.channel.send(user + notInMsg)

@bot.command()
async def scores(ctx):
  bWidth = 32 #board width
  uWidth = 14 #width of the user section
  sWidth = 15 #width of the score section
  board = '-'*bWidth
  board += "\n| # |     user     |     score     |\n"#14 lines in user, 15 lines in score, 32 total
  board += '-' * bWidth
  board += "\n"
  row = "|"
  place = 1
  for user in scoreboard:
  #generates the place of each user
    row += ((" %place |") % place)
  #generates the user portion of the scoreboard
    #in case the username is bigger than the bWidth
    if user.length > uWidth:
      temp = user
      while temp > uWidth:
        temp = temp[:-1]
      row += temp
    #in case the username takes up the entire bWidth
    elif user.length == uWidth - 2:
      row += user
    else:
      #puts in the optimal ammount of spaces
      spaces = ' ' * ((uWidth - user.length) / 2)
      row += spaces
      row += user
      row += spaces
    row += "|"
  #generates the score part of the scoreboard
    score = str(scoreboard[user])
    #maxes out the score at 999999999999999 if the score is bigger than the sWidth
    if score.length > sWidth:
      row += '9'*sWidth
    #inserts no spaces if the score has as many digets as the width
    elif score.length == sWidth:
      row += score
    #puts the optimal ammount of spaces for any score bigger with multiple digets
    elif score.length > 9:
      spaces = ' ' * ((sWidth - score.length) / 2)
      row += spaces
      row += score
      row += spaces
    else:
      row += ' '*7
      row += score
      row += ' '*7
    row += "|\n"
  #sends the scoreboard as an embed in the channel
  msg = discord.Embed(title="Gamerpoints Leaderboard", description=row)
  await ctx.send(embed=msg)
  

#Events
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(Message):
    await bot.process_commands(Message)






bot.run(os.getenv('GAMERPOINTS_BOT_TOKEN'))