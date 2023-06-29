import discord
from discord.ext import commands
import numpy as np
import pandas as pd
import random
import re


NO_PREFERENCE = 2
TOKEN = open("token.txt", "r").readline()

# parse numeric string for arguments
def get_args(arg, categories, slang_choice):
  cats = []
  slang = NO_PREFERENCE
  for i in range(len(arg)):
    num = int(arg[i])
    if i < NO_PREFERENCE and num <= NO_PREFERENCE:
      if categories[num] not in cats:
        cats.append(categories[num])
    elif i >= NO_PREFERENCE and int(arg[i]) < NO_PREFERENCE:
      slang = int(slang_choice[num])
  return (cats, slang)

# filters the given dataframe based on contents of categories and slang
def get_valentine(df, cats = [], slang = NO_PREFERENCE):
  cond1 = (df['Category_1'].isin(cats)) | (df['Category_2'].isin(cats))
  if (cats and 'No preference' not in cats):
    df = df[cond1]
  if (slang < NO_PREFERENCE):
    cond2 = (df['Is_slang'] == slang)
    df = df[cond2]
  return random.choice(list(df['Name']))


# returns the unique values in a dataframe column
def get_values(df, col):
  l = list(df[col].value_counts().index)
  l.append('No preference')
  return l

## global variables ##
valentines = pd.read_csv("valentines.txt", sep = ',', on_bad_lines = 'skip')
valentines['Is_slang'] = np.where(valentines['Is_slang'] == 0, False, True)
categories = get_values(valentines, 'Category_1')
slang_choice = get_values(valentines, 'Is_slang')


#### bot stuff ###

client = discord.Client(intents = discord.Intents.all())
def options(l):
  s = ""
  for i in range(len(l)):
    s += "\t" + str(i)  + ": " + str(l[i]) + "\n"
  return s

def error_message(msg, categories, slang_choice):
  s = ""
  s += "To generate a valentine, must have this format:"
  s += "```./valentine```For filtering, must have this format:"
  s += "```./valentine [filter option 1][filter option 2][abbreviation preference option]```"
  s += "Filter options:\n"
  s += options(categories)
  s += "Abbreviation options:\n"
  s += options(slang_choice)
  return s

@client.event
async def on_message(ctx):
  if x := re.findall("^./valentine [0-3]{2}[0-2]$", ctx.content):
    (cats, slang) = get_args(x[0][-3:], categories, slang_choice)
    await ctx.channel.send(get_valentine(valentines, cats, slang), reference = ctx, mention_author = False)
  elif x := re.findall("^./valentine$", ctx.content):
    await ctx.channel.send(get_valentine(valentines), reference = ctx, mention_author = False)
  elif re.findall("^./valentine help", ctx.content):
    await ctx.channel.send(error_message(ctx.content, categories, slang_choice))

client.run(TOKEN)
