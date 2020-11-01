from discord.ext import commands 
import discord 
from discord.ext.commands import CommandNotFound
from dotenv  import load_dotenv
import os 
import sys 
import aiohttp
import asyncio
import pandas as pd

load_dotenv()

client = commands.Bot(command_prefix='+')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="+"))

@client.command(name ='hello', help = 'says hello')
async def greet(ctx):
    await ctx.send("Hello, I'm FPL AI (v1.0) here to assist you!")

@client.command(name = 'captain', help = 'Enter Actual Name with accurate Accent')
async def captain(ctx, player, playern1='', playern2='',playern3='',playern4='',playern5=''):
    from new_data import new_data

    data, player_name, team_name, opponent = new_data(player, playern1, playern2, playern3, playern4, playern5)

    import joblib
    model = joblib.load('model')
    
    y_pred = model.predict(data)
    result = round(y_pred[0])

    embedVar = discord.Embed(title="Prediction for "+player_name, description="Club:"+str(team_name)+"\nNext match :"+str(opponent), color=0x00ff00)
    embedVar.add_field(name="Selected", value=str(result) +" pts.", inline=False)
    embedVar.add_field(name="Captain", value=str(2*result) +" pts.", inline=False)
    embedVar.add_field(name="Triple Captain", value=str(3*result) +" pts. ", inline=False)
    await ctx.channel.send(embed=embedVar)

@client.command(name = 'week', help = 'gameweek')
async def week1(ctx, w):
    import numpy as np

    url = 'https://raw.githubusercontent.com/footballcsv/england/master/2020s/2020-21/eng.1.csv'

    dataset = pd.read_csv(url)
    week = int(w)
    data = dataset.loc[dataset['Round']==week]
    embedVar = discord.Embed(title="Gameweek "+str(week), color=0x124cb8)
    Home = data['Team 1']   
    s = data['FT']
    Score = s.replace(np.nan,'vs', regex=True)
    Away = data['Team 2']
    date = data['Date']

    for i in range(len(data)):
        embedVar.add_field(name="Match "+str(i+1)+ " : " +str(date.values[i]), value=str(Home.values[i])+" "+str(Score.values[i])+" "+str(Away.values[i]) , inline=False)
    await ctx.channel.send(embed=embedVar)

@client.command(name = 'update', help = "update players if it doesn't appear in prediction")
async def update(ctx):
    dataset = pd.read_csv('https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2020-21/gws/merged_gw.csv')

    player_name_arr = dataset['name'].unique()
    f_pl = []
    s_pl = []
    f_pl_lower = []
    f_pl_upper = []
    s_pl_lower = []
    s_pl_upper = []

    for i in player_name_arr:
        name = i.split()[1]
        if(len(name)<3):
            name = i.split()[2]
        s_pl.append(name)
        s_pl_lower.append(name.lower())
        s_pl_upper.append(name.upper())
        

    for j in player_name_arr:
        name = j.split()[0]    
        f_pl.append(name)
        f_pl_lower.append(name.lower())
        f_pl_upper.append(name.upper())

    df = pd.DataFrame(player_name_arr,columns=['player_name'])

    df['firstname'] = f_pl
    df['surname'] = s_pl
    df['firstname_lower'] = f_pl_lower
    df['surname_lower'] = s_pl_lower
    df['firstname_upper'] = f_pl_upper
    df['surname_upper'] = s_pl_upper

    df.to_csv('player.csv')

    await ctx.send("SUCCESSFULLY UPDATED...")


client.run(os.getenv('discord_token'))

