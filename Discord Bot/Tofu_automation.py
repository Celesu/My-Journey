# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 19:30:51 2022


@author: Reza~
"""
from webserver import keep_alive
import os
import discord
import logging
import time
import asyncio


logging.basicConfig(level=logging.INFO)

client = discord.Client()
guild = discord.Guild

# ======== SOME DEFINITIONS ===============

# 1. Get the spell code on the page.
async def get_spells(message, auth_msg, spells_):
    spells = []
    for i in message.embeds[0].description.split('·'):
        if i[2] == '%':
            spells.append(i[2:-2])
    if spells != spells_: # To avoid giving the same code (when the user haven't change the page)
        await auth_msg.reply(content=', '.join(spells))
    return spells

# 2. Get the hex code on the page.
async def get_hexes(message, auth_msg, hexes_):
    hexes = []
    for i in message.embeds[0].description.split('·'):
        if i[2] == '-':
            hexes.append(i[2:-2])
    if hexes != hexes_: # To avoid giving the same code (when the user haven't change the page)
        await auth_msg.reply(', '.join(hexes))
    return hexes

# 3. Get the aura code on the page.
async def get_auras(message, auth_msg, auras_):
    auras = []
    for i in message.embeds[0].description.split('·'):
        if i[2] == '&':
            auras.append(i[2:-2])
    if auras != auras_: # To avoid giving the same code (when the user haven't change the page)
        await auth_msg.reply(', '.join(auras))
    return auras
    
# 4. Get the card code on the page.
async def get_cards(message, auth_msg, cards_):
    cards = []
    collection = message.embeds[0].description.split('·')
    for i in range(2, len(collection),7):
            cards.append(collection[i][2:-2])
    if cards != cards_: # To avoid giving the same code (when the user haven't change the page)
        await auth_msg.reply(', '.join(cards))       
    return cards


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you playing Tofu'))
    
@client.event
async def on_message(message):
    #if message.author == client.user:
     #   return
    #elif message.content.startswith('_'):
     #   cmd = message.content.split()[0].replace("_","")
      #  if len(message.content.split()) > 1:
       #     parameters = message.content.split()[1:]
       
    # to check if the user give the reaction or no          
    def check(reaction, user):
        return user == auth and str(reaction.emoji) == emot
    
    if message.content.lower() == 'on?':
        await message.channel.send("I'm ready to help you, senpai~")
    
    if any(message.embeds):
        if message.embeds[0].author.name == discord.Embed.Empty:
            # 5. Get the card owner's information
            if (message.author.id == 792827809797898240) and (("Card View" in message.embeds[0].title) or ("Hex" in message.embeds[0].title) or ("Aura" in message.embeds[0].title) or ("Spell" in message.embeds[0].title) or ("Gear" in message.embeds[0].title)):
                emot = '🔍'
                await asyncio.sleep(2)
                await message.add_reaction(emot)
                found = False
                async for msg in message.channel.history(limit=2):
                    if msg.author.bot == False and found == False:
                        if ('v' in msg.content.lower().split()[0]) or ('view' in msg.content.lower().split()[0]):
                            auth = msg.author
                            name = msg.author.name
                            auth_msg = msg
                            found = True
                                
                await client.wait_for("reaction_add", check=check)   # Wait for a reactiontion
                
                if "Card View" in message.embeds[0].title:
                    user_id = message.embeds[0].description.split('·')[1].split()[0][2:-1]
                else:
                    user_id = message.embeds[0].description.split()[1][2:-1]
                        
                try:
                    await client.fetch_user(user_id)
                except:
                    await message.channel.send("The user isn't exist anymore. 🪦")
                else:
                    the_name = await client.fetch_user(user_id)  
                    info = discord.Embed(title=f"The Owner's Information",
                                         description=f"Username: {the_name} \nUser id: {user_id}",
                                         color=0x30ff00)
                    await auth_msg.reply(embed=info)
                            
        else:   
            # 1 Spells
            if (message.author.id == 792827809797898240) and ('Spells' in message.embeds[0].author.name): 
                emot = '🌹'
                await asyncio.sleep(2)
                await message.add_reaction(emot)
                found = False
                async for msg in message.channel.history(limit=2):
                    if msg.author.bot == False and found == False:
                        if 'sp' in msg.content.lower():
                            auth = msg.author
                            name = msg.author.name
                            auth_msg = msg
                            found = True
                try:
                    bot_msg_sp = await message.channel.send(f"Please react the {emot} within 3s if you wanna get the codes senpai!")
                    await client.wait_for("reaction_add", timeout=3, check=check)  # Wait for a reaction                    
                except:
                    await bot_msg_sp.edit(content=f"Seems senpai don't need my service yet~")
                    await bot_msg_sp.delete(delay=1)
                else:
                    await bot_msg_sp.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                    t_end = time.time() + 60
                    spells = []
                    stop = False
                    while time.time() < t_end and stop == False:
                        await message.remove_reaction(emoji = emot, member=auth)
                        try:
                            await client.wait_for("reaction_add", timeout=15, check=check)   # Wait for a reactiontion
                        except:
                            # If need more time and the user is still changing page
                            if time.time() >= t_end:
                                await bot_msg_sp.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_sp.add_reaction(emot)
                                bot_msg_sp = await message.channel.fetch_message(bot_msg_sp.id)
                                reaction = discord.utils.get(bot_msg_sp.reactions, emoji=emot)
                                    
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_sp.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                            else:
                                pass
                        else:
                            spells = await get_spells(message, auth_msg, spells)   # Get the spells on the current page
                            # If need more time, but after you get the code~
                            if time.time() >= t_end:
                                await bot_msg_sp.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_sp.add_reaction(emot)
                                bot_msg_sp = await message.channel.fetch_message(bot_msg_sp.id)
                                reaction = discord.utils.get(bot_msg_sp.reactions, emoji=emot)
                                    
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_sp.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                                    
                    if time.time() >= t_end:
                        await bot_msg_sp.edit(content=f"Time's up, thanks for using my service senpai~")    
                    elif stop == True:    
                        await bot_msg_sp.edit(content=f"I guess you've done(?), thanks for using my service senpai~")    
                            
                
            # 2 Hexes
            if (message.author.id == 792827809797898240) and ('Hexes' in message.embeds[0].author.name): 
                emot = '🌼'
                await asyncio.sleep(2)
                await message.add_reaction(emot)
                found = False
                async for msg in message.channel.history(limit=2):
                    if msg.author.bot == False and found == False:
                        if 'hex' in msg.content.lower():
                            auth = msg.author
                            name = msg.author.name
                            auth_msg = msg
                            found = True
                try:
                    bot_msg_hex = await message.channel.send(f"Please react the {emot} within 3s if you wanna get the codes senpai!")
                    await client.wait_for("reaction_add", timeout=3, check=check)  # Wait for a reaction                    
                except:
                    await bot_msg_hex.edit(content=f"Seems senpai don't need my service yet~")
                    await bot_msg_hex.delete(delay=1)
                else:
                    await bot_msg_hex.edit(content=f"Ok {name}-senpai! In 60s Please react the {emot} to copy the codes, feel free to switch the page!")
                    t_end = time.time() + 60
                    hexes = []
                    stop = False
                    while time.time() < t_end and stop == False:
                        await message.remove_reaction(emoji = emot, member=auth)
                        try:
                            await client.wait_for("reaction_add", timeout=15, check=check)   # Wait for a reactiontion
                        except:
                            # If need more time and the user is still changing page
                            if time.time() >= t_end:
                                await bot_msg_hex.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_hex.add_reaction(emot)
                                bot_msg_hex = await message.channel.fetch_message(bot_msg_hex.id)
                                reaction = discord.utils.get(bot_msg_hex.reactions, emoji=emot)
                                
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_hex.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                            else:
                                pass
                        else:
                            hexes = await get_hexes(message, auth_msg, hexes)   # Get the hexes on the current page
                            # If need more time, but after you get the code~
                            if time.time() >= t_end:
                                await bot_msg_hex.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_hex.add_reaction(emot)
                                bot_msg_hex = await message.channel.fetch_message(bot_msg_hex.id)
                                reaction = discord.utils.get(bot_msg_hex.reactions, emoji=emot)
                                
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_hex.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                                            
                    if time.time() >= t_end:    
                        await bot_msg_hex.edit(content=f"Time's up, thanks for using my service senpai~")    
                    elif stop == True:    
                        await bot_msg_hex.edit(content=f"I guess you've done(?), thanks for using my service senpai~")                
                            
                        
            # 3. Auras
            if (message.author.id == 792827809797898240) and ('Auras' in message.embeds[0].author.name): 
                emot = '🌻'
                await asyncio.sleep(2)
                await message.add_reaction(emot)
                found = False
                async for msg in message.channel.history(limit=2):
                    if msg.author.bot == False and found == False:
                        if 'aura' in msg.content.lower():
                            auth = msg.author
                            name = msg.author.name
                            auth_msg = msg
                            found = True
                try:
                    bot_msg_aura = await message.channel.send(f"Please react the {emot} within 3s if you wanna get the codes senpai!")
                    await client.wait_for("reaction_add", timeout=3, check=check)  # Wait for a reaction                    
                except:
                    await bot_msg_aura.edit(content=f"Seems senpai don't need my service yet~")
                    await bot_msg_aura.delete(delay=1)
                else:
                    await bot_msg_aura.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                    t_end = time.time() + 60
                    auras = []
                    stop = False
                    while time.time() < t_end and stop == False:
                        await message.remove_reaction(emoji = emot, member=auth)
                        try:
                            await client.wait_for("reaction_add", timeout=15, check=check)   # Wait for a reactiontion
                        except:
                            # If need more time and the user is still changing page
                            if time.time() >= t_end:
                                await bot_msg_aura.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_aura.add_reaction(emot)
                                bot_msg_aura = await message.channel.fetch_message(bot_msg_aura.id)
                                reaction = discord.utils.get(bot_msg_aura.reactions, emoji=emot)
                                    
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_aura.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                            else:
                                pass
                        else:
                            auras = await get_auras(message, auth_msg, auras)   # Get the hexes on the current page
                            # If need more time, but after you get the code~
                            if time.time() >= t_end:
                                await bot_msg_aura.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_aura.add_reaction(emot)
                                bot_msg_aura = await message.channel.fetch_message(bot_msg_aura.id)
                                reaction = discord.utils.get(bot_msg_aura.reactions, emoji=emot)
                                
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_aura.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                                        
                    if time.time() >= t_end:    
                        await bot_msg_aura.edit(content=f"Time's up, thanks for using my service senpai~")    
                    elif stop == True:    
                        await bot_msg_aura.edit(content=f"I guess you've done(?), thanks for using my service senpai~")    
                                    
                        
            # 4. Cards
            if (message.author.id == 792827809797898240) and ('Card Collection' in message.embeds[0].author.name): 
                emot = '🎲'
                await asyncio.sleep(2)
                await message.add_reaction(emot)
                found = False
                async for msg in message.channel.history(limit=2):
                    if msg.author.bot == False and found == False:
                        if 'c' in msg.content.lower().split()[0]:
                            auth = msg.author
                            name = msg.author.name
                            auth_msg = msg
                            found = True
                try:
                    bot_msg_card = await message.channel.send(f"Please react the {emot} within 3s if you wanna get the codes senpai!")
                    await client.wait_for("reaction_add", timeout=3, check=check)  # Wait for a reaction                    
                except:
                    await bot_msg_card.edit(content=f"Seems senpai don't need my service yet~")
                    await bot_msg_card.delete(delay=1)
                else:
                    await bot_msg_card.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                    t_end = time.time() + 60
                    cards = []
                    stop = False
                    while time.time() < t_end and stop == False:
                        await message.remove_reaction(emoji = emot, member=auth)
                        try:
                            await client.wait_for("reaction_add", timeout=15, check=check)   # Wait for a reactiontion
                        except:
                            # If need more time and the user is still changing page
                            if time.time() >= t_end:
                                await bot_msg_card.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_card.add_reaction(emot)
                                bot_msg_card = await message.channel.fetch_message(bot_msg_card.id)
                                reaction = discord.utils.get(bot_msg_card.reactions, emoji=emot)
                                    
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_card.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                            else:
                                pass
                        else:
                            cards = await get_cards(message, auth_msg, cards)   # Get the hexes on the current page
                            # If need more time, but after you get the code~
                            if time.time() >= t_end:
                                await bot_msg_card.edit(content=f"Time's up, need more time senpai? if yes, please react {emot} within 10s~")
                                await bot_msg_card.add_reaction(emot)
                                bot_msg_card = await message.channel.fetch_message(bot_msg_card.id)
                                reaction = discord.utils.get(bot_msg_card.reactions, emoji=emot)
                                        
                                try: # React if you need more time
                                    await client.wait_for("reaction_add", timeout=10, check=check)   # Wait for a reactiontion
                                except: # To exit the loop, if no react
                                    await reaction.clear()
                                    stop = True
                                    pass
                                else: # If need more time
                                    await reaction.clear()
                                    t_end = time.time() + 60
                                    await bot_msg_card.edit(content=f"Ok {name}-senpai! In 60s please react the {emot} to copy the codes, feel free to switch the page!")
                                    pass
                                    
                    if time.time() >= t_end:    
                        await bot_msg_card.edit(content=f"Time's up, thanks for using my service senpai~")    
                    elif stop == True:    
                        await bot_msg_card.edit(content=f"I guess you've done(?), thanks for using my service senpai~")                
                        
                  
keep_alive() 

TOKEN = os.environ.get("DISCORD_BOT_SECRET") # your bot token

client.run(TOKEN)
# rencana              
# hex = '🌼'
# aura = '🌻'               
# nama = dadu
            
