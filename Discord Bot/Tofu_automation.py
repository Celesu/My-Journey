# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:13:37 2022

@author: Reza A R
"""

# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import asyncio
# IMPORT THE OS MODULE.
import os

# ======= Things I don't underestand =========
# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
# from dotenv import load_dotenv

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
# load_dotenv()
# GRAB THE API TOKEN FROM THE .ENV FILE.
# ============================================

import requests
import json
# import time

#
#
# ============ BACA =================
DISCORD_TOKEN="isi token sendiri"
# ============ OK!  =================
#
#

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client()

# ============================= Just Paste(d) This from Web =======================================
# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
# ==================================================================================================

async def retrieve_msg(channel_id):
    headers = {
        "authorization": "your discord acc token" #ini untuk akses akun discord
    }
    r = requests.get('https://discord.com/api/v9/channels/'+str(channel_id)+'/messages?limit=10', headers=headers) # Pembeda hanya
    #/channel/cahnnel_id/....
    
    jsonn = json.loads(r.text)
    for value in jsonn:
        try:
            react = value['reactions'][-1]['emoji'].get('name')
        except:
            None 
        else:
            if react == '🎲':    # Plan mau set input 'react'
                return value, value['id']

async def retrieve_the_msg(channel_id, val_id):
    headers = {
        "authorization": "your discord acc token" #ini untuk akses akun discord
    }
    r = requests.get('https://discord.com/api/v9/channels/'+channel_id+'/messages?limit=100', headers=headers) # Pembeda hanya
    #/channel/cahnnel_id/....
    
    jsonn = json.loads(r.text)
    for value in jsonn:
        if value['id'] == val_id:
            return value
            
async def total_pages(the_footer):
    for _, word in enumerate(the_footer):
        if word == 'o' and the_footer[_+1] =='f':
            leng = len(the_footer[_+3:])
            nganu = 10**(leng-1)
            pages = the_footer[_+3:]
            
            if nganu == 1:
                return 1
            elif int(pages)%nganu == 0:
                return int(pages[:leng-1])
            else:
                return int(pages[:leng-1])+1
        
# 1 ==============================================================
# Get the hexes!
async def the_hexes(message, val):
    hexes = []
    for i in val['embeds']:
        for ii in i['description'].split('·'):
            if ii[2] == '-':
                hexes.append(ii[2:-2])

    return hexes

async def get_hexes(message, channel_id, page=1):
    the_val, val_id = await retrieve_msg(channel_id)
    pages = await total_pages(the_val['embeds'][0]['footer']['text'])
    my_hexes = []
#    page=1
#    print('\n~~~Start~~~')
    for i in range(pages):
#        print('Page:', page)
        the_value = await retrieve_the_msg(channel_id, val_id)
        my_hexes =  my_hexes + await the_hexes(message, the_value)
        page += 1
        if page <= pages:
            hal = 'Gas ke hal. '+ str(page) + ' senpai~'
            await message.edit(content=hal)
            await asyncio.sleep(3)
#     print('\n~~~Done~~~\n')
    return '\n'.join(my_hexes), my_hexes

# 2 ==============================================================
# Get the spells!

async def the_spells(message, val):
    spells = []
    for i in val['embeds']:
        for ii in i['description'].split('·'):
            if ii[2] == '%':
                spells.append(ii[2:-2])

    return spells

async def get_spells(message, channel_id, page=1):
    the_val, val_id = await retrieve_msg(channel_id)
    pages = await total_pages(the_val['embeds'][0]['footer']['text'])
    my_spells = []
#    page=1
#    print('\n~~~Start~~~')
    for i in range(pages):
        print('Page:', i)
        the_value = await retrieve_the_msg(channel_id, val_id)
        my_spells = my_spells + await the_spells(message, the_value)
        page += 1
        if page <= pages:
            hal = 'Gas ke hal. '+ str(page) + ' senpai~'
            await message.edit(content=hal)
            await asyncio.sleep(3)
        
#     print('\n~~~Done~~~\n')
    return ', '.join(my_spells), my_spells

# ==============================================================
# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
    # Get the id of the channel!
    channel = str(message.channel.id)
    if message.content == "hex" or message.content == "Hex":
        message = await message.channel.send('Ok')
        hex_ , the_hexes = await get_hexes(message, channel)
        # SENDS BACK A MESSAGE TO THE CHANNEL.
        await message.edit(hex_)
    elif message.content == 'on?' or message.content == 'On?':
        await message.channel.send('on bang!')
    elif message.content == 'spell' or message.content == 'Spell':
        message = await message.channel.send('Ok')
        spell_ , the_spells = await get_spells(message, channel)
        await message.edit(content=spell_)
        
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)
