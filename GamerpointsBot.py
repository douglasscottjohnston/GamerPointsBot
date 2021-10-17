import os
import random

import discord
import discord.ext
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
scoreboard = {} # member : score

notInMsg = " is not in the scoreboard, add them with the addUser command"
inMsg = " is already in the scoreboard"

#Commands
@bot.command(name="add_user", description="Adds a member to the scoreboard")
@commands.has_permissions(administrator=True)
async def add_user(ctx, *members: commands.Greedy[discord.Member]):
  for member in members:
    if member.name in scoreboard:
      await ctx.send(member.name + inMsg)
    else:
      scoreboard[member.name] = 0
      await ctx.send(member.name + " added with a score of 0")

@bot.command(name="remove_user", description="Removes a member from the scoreboard")
@commands.has_permissions(administrator=True)
async def remove_user(ctx, *members: commands.Greedy[discord.Member]):
  for member in members:
    if member.name in scoreboard:
      del scoreboard[member.name]
      await ctx.send(member.name + " removed from the scoreboard")
    else:
      await ctx.send(member.name + notInMsg)

@bot.command(name="won_game", description="Adds 10 points to all members that won a game")
async def won_game(ctx, *members: commands.Greedy[discord.Member]):
  for member in members:
    if member.name in scoreboard:
      scoreboard[member.name] = scoreboard.get(member.name) + 10
      await ctx.send(member.name + " gained 10 gamerpoints!")
    else:
      await ctx.send(member.name + notInMsg)

@bot.command(name="lost_game", description="Removes 10 points from all members that lost a game")
async def lost_game(ctx, *members: commands.Greedy[discord.Member]):
  for member in members:
    if member.name in scoreboard:
      scoreboard[member.name] = scoreboard.get(member.name) - 10
      await ctx.send(member.name + " lost 10 gamerpoints!")
    else:
      await ctx.send(member.name  + notInMsg)

@bot.command(name="add_points", description="Adds points to the member")
@commands.has_permissions(administrator=True)
async def add_points(ctx, *, member, points):
  if member.name in scoreboard:
    scoreboard[member.name] = scoreboard.get(member.name) + points
    await ctx.send(member.name + (" gained %d gamerpoints!" % points))
  else:
    await ctx.send(member + notInMsg)

@bot.command(name="remove_points", description="Removes points from tmember")
@commands.has_permissions(administrator=True)
async def remove_points(ctx, *, member, points):
  if member.name in scoreboard:
    scoreboard[member.name] = scoreboard.get(member.name) - points
    await ctx.send(member + " lost %d gamerpoints" % points)
  else:
    await ctx.send(member + notInMsg)

@bot.command(name="scores", description="Displays the scoreboard")
async def scores(ctx):
  bWidth = 32 #board width
  uWidth = 14 #width of the user section
  sWidth = 15 #width of the score section
  row = ('-' * bWidth)
  row += "\n| # |-----user-----|-----score-----|\n"#14 lines in user, 15 lines in score, 32 total
  place = 1
  for member, points in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True):
  #generates the place of each user
    row += "|"
    row += ((" %s |") % place)
  #generates the user portion of the scoreboard
    #in case the username is bigger than the bWidth
    if len(member) > uWidth:
      temp = member
      while len(temp) > uWidth:
        temp = temp[:-1]
      row += temp
    #in case the username takes up the entire bWidth
    elif len(member) == uWidth - 2:
      row += member
    else:
      #puts in the optimal ammount of spaces
      spaces = ('-' * int((uWidth - len(member)) / 2))
      row += spaces
      row += member
      row += spaces
    row += "|"
  #generates the score part of the scoreboard
    spoints = str(points)
    #maxes out the score at 999999999999999 if the score is bigger than the sWidth
    if len(spoints) > sWidth:
      row += ('9' * sWidth)
    #inserts no spaces if the score has as many digets as the width
    elif len(spoints) == sWidth:
      row += spoints
    #puts the optimal ammount of spaces for any score bigger with multiple digets
    elif len(spoints) > 9:
      spaces = ('-' * int((sWidth - len(spoints)) / 2))
      row += spaces
      row += spoints
      row += spaces
    else:
      row += ('-' * 7)
      row += spoints
      row += ('-' * 7)
    row += "|\n"
    place += 1
  #sends the scoreboard as an embed in the channel
  row += ('-' * bWidth)
  print(row)
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
