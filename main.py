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
from flask import Flask, jsonify, request
from threading import Thread
import json
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='+', intents=disnake.Intents.all(), help_command=None)

lock_data_file = 'locked_channels.json'

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    statut.start()
    remind_bumping.start()
    check_status.start()
    update_staff_status.start()
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            async for message in channel.history(limit=None): 
                if message.author.bot:
                    continue
                
                if message.author.id not in user_stats:
                    user_stats[message.author.id] = {
                        "messages": 0,
                        "voice_time": 0
                    }

                user_stats[message.author.id]["messages"] += 1
    
    save_stats()
    
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


    
staff_status_message = None

@tasks.loop(minutes=3)
async def update_staff_status():
    global staff_status_message  

    channel = bot.get_channel(1293697918364024904)  
    if not channel:
        return

    guild = channel.guild
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

    if staff_status_message is None:
        staff_status_message = await channel.send(embed=embed)
    else:
        await staff_status_message.edit(embed=embed)

@update_staff_status.before_loop
async def before_update_staff_status():
    await bot.wait_until_ready()
    
@bot.event
async def on_member_join(member: disnake.Member):
    guild = member.guild
    channel = disnake.utils.get(guild.text_channels, name='💬•〃général')
    channel2 = disnake.utils.get(guild.text_channels, name='🍂•〃join')
    role = disnake.utils.get(guild.roles, name="🔱〢New Member")

    if channel and role:
        em = disnake.Embed(
            title=f'Bienvenue {member.name} <a:aw_str:1282653955498967051>, dans {guild.name} <a:3895blueclouds:1255574701909086282>',  
            description=f'Nous sommes désormais {guild.member_count} membres, je te laisse les instructions. Si tu as besoin d\'aide, n\'hésite pas à ping un membre du staff.',
            color=0x3f9eff
        )
        em.add_field(name='Tu peux retrouver notre règlement ici', value='https://discord.com/channels/1251476405112537148/1293641075881283605', inline=False)
        em.add_field(name="N'oublie pas de prendre tes rôles ici", value="https://discord.com/channels/1251476405112537148/1293720766717890631", inline=False)
        em.add_field(name="ici tu peut voir les rank vocal/message", value="https://discord.com/channels/1251476405112537148/1293641087696633896", inline=False)
        em.add_field(name="Si tu souhaites être recruté, voici notre salon de recrutement", value="https://discord.com/channels/1251476405112537148/1293641081421824112", inline=False)
        em.set_thumbnail(url='https://cdn.discordapp.com/icons/1251476405112537148/a_8727a3a7984464a7df1bb14ed39db0a4.gif?size=1024&width=0&height=256')

        await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66f993cf&is=66f8424f&hm=f14094491366b83448d82b6c4fc17128561f4c54465a5ba9fa2fffe1fb83dda3&=')
        await channel.send(embed=em, content=f"{member.mention} {role.mention}")  
        msg = 'Bienvenue jespere que tu va passer un execelent moment avec nous'
        await channel.send(content=f'{msg} {member.mention} <:portal:1282654939402862675>')
        await channel2.send(embed=em, content=f"{member.mention}")  
    else:
        print("Erreur: Le salon '💬〃chat' ou le rôle '🔱〢New Member' est introuvable.")
        
@bot.command(name='miyako_stat', description='Show the number of users with /miyakofr in their status or description')
async def miyako_stat(ctx):
    miyako_users = 0

    for member in ctx.guild.members:
        if member.bot:
            continue
        
        has_custom_status = any(
            activity.type == disnake.ActivityType.custom and activity.state and '/miyakofr' in activity.state
            for activity in member.activities
        )
        
        has_custom_description = '/miyakofr' in member.display_name.lower() or '/miyakofr' in member.nick.lower() if member.nick else False

        if has_custom_status or has_custom_description:
            miyako_users += 1

    em = disnake.Embed(title='Miyako Stats', description=f"There are **{miyako_users}** users with '/miyakofr' in their status or description.", color=disnake.Colour.dark_gray())
    await ctx.send(embed=em)

def load_lock_data():
    try:
        with open(lock_data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_lock_data(data):
    with open(lock_data_file, 'w') as f:
        json.dump(data, f)
        
@bot.event
async def on_command(ctx):
    lock_data = load_lock_data()
    if str(ctx.channel.id) in lock_data:
        await ctx.send("This channel is locked. Commands are not allowed.")
        raise disnake.ext.commands.CommandError("Command execution blocked in locked channel.")


@bot.command()
async def cmd(ctx, option: str):
    if option not in ["lock", "unlock"]:
        await ctx.send("Invalid option. Use `lock` or `unlock`.")
        return

    lock_data = load_lock_data()
    channel_id = str(ctx.channel.id)

    if option == "lock":
        if channel_id not in lock_data:
            lock_data[channel_id] = True
            save_lock_data(lock_data)
            await ctx.send(f"Channel {ctx.channel.name} locked.")
        else:
            await ctx.send("This channel is already locked.")
    
    elif option == "unlock":
        if channel_id in lock_data:
            del lock_data[channel_id]
            save_lock_data(lock_data)
            await ctx.send(f"Channel {ctx.channel.name} unlocked.")
        else:
            await ctx.send("This channel is not locked.")

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
            
@bot.command(name="rename_emojis", description="Remove duplicate emojis and rename all emojis.")
@commands.has_permissions(administrator=True)
async def rename_emojis(ctx):
    guild = ctx.guild
    emojis = guild.emojis

    seen = {}
    duplicate_count = 0
    rename_count = 0
    
    for emoji in emojis:
        if emoji.name not in seen:
            seen[emoji.name] = emoji
        else:
            try:
                await emoji.delete()
                duplicate_count += 1
            except Exception:
                pass
    
    for idx, emoji in enumerate(seen.values(), start=1):
        new_name = f"{guild.name.lower().replace(' ', '_')}_{idx}"
        try:
            await emoji.edit(name=new_name)
            rename_count += 1
        except Exception:
            pass

    await ctx.send(f"Processed emojis: {duplicate_count} duplicates removed, {rename_count} renamed to '{guild.name}_x' format.")

            
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





STATS_FILE = "user_stats.json"
REMOTE_STATS_URL = "https://miyako-pkzr.onrender.com/stats"

def load_stats():
    global user_stats
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            user_stats = json.load(f)
    else:
        user_stats = {}

def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(user_stats, f, indent=4)

load_stats()

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
    save_stats()

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

    save_stats()

@bot.command(name='stat', description='+stat @user (beta)')
async def stat(ctx, user: disnake.Member = None):
    load_stats()

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

    guild_icon = ctx.guild.icon.url if ctx.guild.icon else None

    em = disnake.Embed(title=f'Stats of {user.display_name}', description=f"Here are the statistics for {user.display_name}:", color=disnake.Colour.blue())
    em.add_field(name='Voice', value=f'Time spent in voice channels: **{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds**.', inline=False)
    em.add_field(name='Messages', value=f'Total messages sent: **{message_count}**.', inline=False)

    if guild_icon:
        em.set_thumbnail(url=guild_icon)

    await ctx.send(embed=em)




@bot.command(name='msg_partner', descriptions='+msg_partner (Only for manage_messages=True)')
@commands.has_permissions(manage_messages=True)
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
        
@bot.command(name='recrutement', description='+recrutement (Only for manage_messages=True)')
@commands.has_permissions(manage_messages=True)
async def recrutement(ctx):
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

        view = disnake.ui.View()
        view.add_item(Ticket())
        view.add_item(NotrePub())
        await ctx.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=')
        await ctx.send(embed=embed_image)
        await ctx.send(embed=embed, view=view)
        
@bot.command(name='moveall', description='+moveall (Only for administrator=True)')
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
        
@bot.command(name="renew", description='+renew (Only for manage_channel=True)')
@commands.has_permissions(manage_channels=True)
async def renew(ctx):
    channel = ctx.channel
    category = channel.category

    new_channel = await ctx.guild.create_text_channel(channel.name, category=category)

    for perm in channel.overwrites:
        await new_channel.set_permissions(perm, overwrite=channel.overwrites[perm])

    await channel.delete()

    await new_channel.send("This channel has been renewed.")

@bot.command(name='clear', description='+clear (Amount: Max(1000)), (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount > 1000:
        await ctx.send("You can only delete up to 1000 messages at once.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)

    confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages.")
    await asyncio.sleep(5)
    await confirmation.delete()

        
@bot.command(name="help", description='Show all commands')
async def help_command(ctx):
    embed_color = 0x5ba6f3
    max_fields_per_embed = 25  # Maximum number of fields per embed
    command_fields = []

    for command in bot.commands:
        command_fields.append(
            (f"`+{command.name}`", f"**Usage:** {command.description or 'No description provided.'}")
        )

    total_commands = len(command_fields)
    total_embeds = (total_commands + max_fields_per_embed - 1) // max_fields_per_embed  # Calculate number of embeds needed

    for i in range(total_embeds):
        embed = disnake.Embed(
            title="Help Menu" if i == 0 else None,
            description=f"Total commands: {total_commands}",
            color=embed_color
        )
        if i == 0:
            embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
            embed.set_image(url=ctx.guild.banner.url if ctx.guild.banner else None)

        start_index = i * max_fields_per_embed
        end_index = start_index + max_fields_per_embed
        for field in command_fields[start_index:end_index]:
            embed.add_field(name=field[0], value=field[1], inline=False)

        await ctx.send(embed=embed)



giveaways = {}


@bot.command(name='giveaway', description='+giveaway (Only for administrator=True)')
@commands.has_permissions(administrator=True)
async def start_giveaway(ctx):
    # Demande le prix et supprime les messages
    question = await ctx.send("What is the prize for the giveaway?")
    prize_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    prize = prize_msg.content
    await question.delete()
    await prize_msg.delete()

    # Demande la durée et supprime les messages
    question = await ctx.send("What is the duration of the giveaway? (Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days)")
    duration_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    duration = duration_msg.content
    await question.delete()
    await duration_msg.delete()

    duration_seconds = convert_duration(duration)
    if duration_seconds is None:
        await ctx.send("Invalid duration format. Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.")
        return

    # Demande l'image et supprime les messages
    question = await ctx.send("Provide an image URL (or type 'none' if you don't want to add an image).")
    image_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    image = image_msg.content if image_msg.content.lower() != 'none' else None
    await question.delete()
    await image_msg.delete()

    # Création de l'embed du giveaway
    embed = disnake.Embed(
        title="New Giveaway",
        description=f"Prize: ```{prize}```",
        color=disnake.Color.dark_gray()
    )
    embed.add_field(name="Author", value=ctx.author.mention, inline=True)
    embed.add_field(name="Time", value=f"**`{duration}`**", inline=True)
    embed.add_field(name="Conditions", value='/miyakofr in status', inline=False)
    
    if image:
        embed.set_image(url=image)

    message = await ctx.send(embed=embed)
    
    await message.add_reaction("🌴")

    giveaways[message.id] = {
        "prize": prize,
        "conditions": '/miyakofr in status',
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
            await message.edit(embed=embed)
            await winner.send(f"Congratulations! You've won: **{giveaway_data['prize']}**. Open a ticket to claim your prize.")
        else:
            embed.add_field(name="Winner", value="No participants.", inline=False)
            await message.edit(embed=embed)
    
    await message.clear_reaction("🌴")

@bot.command(name='reroll')
@commands.has_permissions(manage_messages=True)
async def reroll_giveaway(ctx, message_id: int):
    message = await ctx.fetch_message(message_id)
    if message_id in giveaways:
        giveaway_data = giveaways[message_id]
        participants = giveaway_data["participants"]
        if participants:
            winner = random.choice(participants)
            embed = message.embeds[0]
            embed.add_field(name="New Winner", value=winner.mention, inline=False)
            await message.edit(embed=embed)
            await winner.send(f"Congratulations! You've won: **{giveaway_data['prize']}**. Open a ticket to claim your prize.")
        else:
            await ctx.send("No participants to reroll.")
    else:
        await ctx.send("Giveaway not found.")

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "🌴" and not user.bot:
        message_id = reaction.message.id
        if message_id in giveaways:
            giveaways[message_id]["participants"].append(user)

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.emoji == "🌴" and not user.bot:
        message_id = reaction.message.id
        if message_id in giveaways:
            giveaways[message_id]["participants"].remove(user)

def convert_duration(duration):
    try:
        time_unit = duration[-1]
        time_value = int(duration[:-1])
        if time_unit == 's':
            return time_value
        elif time_unit == 'm':
            return time_value * 60
        elif time_unit == 'h':
            return time_value * 3600
        elif time_unit == 'd':
            return time_value * 86400
        else:
            return None
    except (ValueError, IndexError):
        return None

            
@bot.command(name='rules', description='+rules (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def rules(ctx):
    em_img = disnake.Embed()
    em_img.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')

    embed = disnake.Embed(title="Règlement du Serveur", color=disnake.Colour.dark_gray())
    embed.add_field(name="Tos", value="Nous vous demandons de formellement respecter les termes de service de Discord.", inline=False)
    embed.add_field(name="Interdiction", value="Il est interdit d'insulter les autres utilisateurs, d'imposer vos croyances religieuses. Chacun est libre de ses choix. Le manque de respect et toute forme de discrimination sont strictement interdits.", inline=False)
    embed.add_field(name="Bannissement", value="Les actes suivants entraîneront un bannissement : toute forme de hacking, phishing, faux cadeaux Nitro, doxing, ou dérangements vocaux.", inline=False)
    embed.add_field(name="Pub, lien", value="Il est interdit de faire de la publicité sans permission. Vous pouvez toutefois faire une demande de partenariat si vous remplissez les conditions indiquées [ici](https://discord.com/channels/1251476405112537148/1293641123046359120).", inline=False)
    embed.add_field(name="But", value="Notre serveur a pour but de divertir les membres, de leur apporter du sourire, et de réaliser divers projets à l'avenir.", inline=False)
    embed.add_field(name="But 2", value="Nous prévoyons de vous offrir une variété de divertissements, y compris des giveaways et des projets uniques.", inline=False)

    await ctx.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=")
    await ctx.send(embed=em_img)
    await ctx.send(embed=embed)

@bot.command(name='support', description='+support (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def soutien(ctx):
    embed = disnake.Embed(title="Nous Soutenir `🔎`", color=disnake.Color.dark_gray())
    embed.add_field(name="/miyakofr dans votre statut", value="Obtenez le rôle <@&1293640997225369650>", inline=False)
    embed.add_field(name="Boostez le serveur", value="Obtenez le rôle <@&1256932646903091291> et ses avantages : https://discord.com/channels/1251476405112537148/1268927834714542183", inline=False)
    
    em2 = disnake.Embed()
    em2.set_image(url='https://giffiles.alphacoders.com/728/72850.gif')
    

    await ctx.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66fe310f&is=66fcdf8f&hm=4b9aca670052feb715f185c930165955d5809e277009bb314cd240167507901c&=")
    await ctx.send(embed=em2)
    await ctx.send(embed=embed)
            
@bot.command(name='embed', description='+embed (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def em(ctx):
    question = await ctx.send("In which channel would you like to send the embed? Mention the channel.")
    channel_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    channel = channel_msg.channel_mentions[0] if channel_msg.channel_mentions else None
    await question.delete()
    await channel_msg.delete()

    if not channel:
        await ctx.send("Invalid channel. Please mention a valid text channel.")
        return

    question = await ctx.send("What is the title of the embed?")
    title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    title = title_msg.content
    await question.delete()
    await title_msg.delete()

    question = await ctx.send("What is the description of the embed?")
    description_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    description = description_msg.content
    await question.delete()
    await description_msg.delete()

    embed = disnake.Embed(title=title, description=description, color=disnake.Color.dark_gray())
    await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66fe310f&is=66fcdf8f&hm=4b9aca670052feb715f185c930165955d5809e277009bb314cd240167507901c&=")
    await channel.send(embed=embed)

@bot.command(name='embed_edit', description='+embed_edit (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def emedit(ctx):
    question = await ctx.send("What is the ID of the message to edit?")
    id_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    message_id = int(id_msg.content)
    await question.delete()
    await id_msg.delete()

    question = await ctx.send("What is the new title of the embed?")
    title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    title = title_msg.content
    await question.delete()
    await title_msg.delete()

    question = await ctx.send("What is the new description of the embed?")
    description_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    description = description_msg.content
    await question.delete()
    await description_msg.delete()

    embed = disnake.Embed(title=title, description=description, color=disnake.Color.dark_gray())
    message = await ctx.channel.fetch_message(message_id)
    await message.edit(embed=embed)

@bot.command(name='say', description='+say (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def say(ctx):
    question = await ctx.send("What message do you want to send?")
    message_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    message_content = message_msg.content
    await question.delete()
    await message_msg.delete()

    await ctx.send(message_content)

@bot.command(name='modify', description='+modify (Only for manage_message=True)')
@commands.has_permissions(manage_messages=True)
async def modify(ctx):
    question = await ctx.send("What is the ID of the message to modify?")
    id_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    message_id = int(id_msg.content)
    await question.delete()
    await id_msg.delete()

    question = await ctx.send("What is the new content of the message?")
    new_message_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    new_message = new_message_msg.content
    await question.delete()
    await new_message_msg.delete()

    try:
        message = await ctx.channel.fetch_message(message_id)
        await message.edit(content=new_message)

        embed = disnake.Embed(
            description="Message modified successfully.",
            color=disnake.Color.dark_gray()
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

    except disnake.NotFound:
        await ctx.send("Message not found.")
        

    
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

@bot.command(name='lock', description='+lock (Only for manage_channels=true)')
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


@bot.command(name='unlock', description='+unlock (Only for manage_channels=true)')
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

@bot.command(name="give", description="+give (@user or all) @role")
@commands.has_permissions(manage_guild=True)
async def give(ctx, member: str, *, role_name: disnake.Role):
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


@bot.command(name='suspend', description='+suspend @user time(Ex:10s), roles: (Only for manage_guild=True)')
@commands.has_permissions(manage_guild=True)
async def suspend(ctx, membre: disnake.Member, temps: str, roles: disnake.Role):
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



@bot.command(name='ban', description='+ban @user reason, (Only for ban_member=True)')
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


@bot.command(name='tempban', description='+tempban @user time(Ex:10 s), reason, (Only for ban_member=True)')
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

        await ctx.msg.edit(f"{member.name} has been unbanned after {time} {unit}.")

    except disnake.Forbidden:
        await ctx.msg.edit("I don't have permission to ban this user.")
    except Exception as e:
        await ctx.msg.edit(f"An error occurred: {str(e)}")


@ban.error
@tempban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Make sure to mention a valid member and role.", delete_after=5)
    else:
        await ctx.msg.edit(f"An error occurred")




@bot.command(name='rank', description='+rank @user role: (Only Administrator)')
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

@app.route("/stats")
def get_stats():
    try:
        response = requests.get(REMOTE_STATS_URL)
        response.raise_for_status() 
        return response.json() 
    except requests.RequestException:
        return user_stats

@app.route('/locked_channels', methods=['GET'])
def get_locked_channels():
    return json.dumps(load_lock_data()), 200

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()


bot.run(os.getenv('TOKEN'))
