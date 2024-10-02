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


QUESTION_CHANNEL = "❔〃question-du-jour"
GUILD_NAME = "La Taverne 🍻"

anime_list = []
global_anime_name = None
global_anime_link = None
accept_count = 0
pass_count = 0



intents = disnake.Intents.all()
intents.message_content = True
intents.members = True

questions = []

bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    await bot.change_presence(
        status=disnake.Status.online,
        activity=disnake.Activity(
            type=disnake.ActivityType.streaming,
            name=".help & created by Mxtsouko",
            url='https://www.twitch.tv/mxtsouko'
        )
    )


@bot.command()
async def help(ctx):
    embed_fun = disnake.Embed(
        title="**Fun** - Commandes",
        description="Voici les commandes disponibles pour le fun du bot **Misaki**.",
        color=disnake.Color.blue()
    )

    embed_fun.add_field(
        name=".hug @utilisateur",
        value="Faites un câlin à un utilisateur.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".kiss @utilisateur",
        value="Faites un bisou à un utilisateur.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".punch @utilisateur",
        value="Mettez un coup de poing à un utilisateur.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".murder @utilisateur",
        value="Utilisez cette commande pour 'tuer' un utilisateur pour un chips et un coca.",
        inline=False
    )

    
    embed_fun.add_field(
        name=".joke",
        value="Faites apparaître une blague.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".rps pierre/feuille/ciseaux",
        value="Jouez à pierre-papier-ciseaux avec Misaki.",
        inline=False
    )

    embed_fun.add_field(
        name=".cat",
        value="Faites apparaître un chat mignon.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".dog",
        value="Faites apparaître un chien mignon.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".coinflip pile ou face",
        value="Jouez à pile ou face avec Misaki.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".roll nombre",
        value="Faites un lancer de dé.",
        inline=False
    )

    await ctx.send(embed=embed_fun)

    embed_moderation = disnake.Embed(
        title="**Modération** - Commandes",
        description="Voici les commandes disponibles pour la modération de **La Taverne**.",
        color=disnake.Color.red()
    )
    
    embed_moderation.add_field(
        name=".suspend @utilisateur 1d",
        value="Suspendre un membre du staff pour une durée déterminée.",
        inline=False
    )
    
    embed_moderation.add_field(
        name=".réunion date heure",
        value="Organisez une réunion staff.",
        inline=False
    )
    
    embed_moderation.add_field(
        name=".ban @utilisateur raison",
        value="Bannissez un membre du serveur.",
        inline=False
    )
    
    embed_moderation.add_field(
        name=".tempban @utilisateur durée raison",
        value="Bannissez un membre temporairement.",
        inline=False
    )
    
    embed_moderation.add_field(
        name=".rm_staff @utilisateur plainte",
        value="Faites une remarque sur un membre du staff.",
        inline=False
    )
    
    embed_moderation.add_field(
        name=".promouvoir fonction @utilisateur",
        value="Promouvez un membre.",
        inline=False
    )

    await ctx.send(embed=embed_moderation)

@bot.command()
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
        
@bot.command()
@commands.has_permissions(administrator=True)
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
                super().__init__(label="Notre Document!", style=disnake.ButtonStyle.link, url="https://forms.gle/QxWytREs11Q6XzAB6")

        if channel:
            view = disnake.ui.View()
            view.add_item(Ticket())
            view.add_item(NotrePub())
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=')
            await channel.send(embed=embed_image)
            await ctx.send(embed=embed, view=view)
        
reputation_data = {
    723256412674719795: 0 
}

last_rep_time = {}

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

@bot.command()
async def rep(ctx):
    user_id = 723256412674719795  
    author_id = ctx.author.id      
    now = datetime.now()           


    user = await bot.fetch_user(user_id)

    if author_id in last_rep_time:
        time_since_last_rep = now - last_rep_time[author_id]
        
        if time_since_last_rep < timedelta(hours=6):
            remaining_time = timedelta(hours=6) - time_since_last_rep
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            embed = disnake.Embed(title="Temps d'attente", color=disnake.Color.red())
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(
                name="Réputation non modifiée",
                value=f"Vous devez attendre encore {hours} heures, {minutes} minutes avant d'ajouter une nouvelle réputation.",
                inline=False
            )
            return await ctx.send(embed=embed)

    last_rep_time[author_id] = now

    reputation_data[user_id] += 1  

    embed = disnake.Embed(title="Réputation mise à jour", color=disnake.Color.red())
    embed.set_thumbnail(url=user.avatar.url)  
    embed.add_field(
        name="Réputation augmentée",
        value=f"La réputation de **{user.name}** a été augmentée. Total: {reputation_data[user_id]}",
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_admin)
async def moveall(ctx):
    if ctx.author.voice:  
        channel = ctx.author.voice.channel
        for member in ctx.guild.members:
            if member.voice and member.voice.channel != channel:  
                await member.move_to(channel)
        await ctx.send("Tous les utilisateurs ont été déplacés dans votre canal vocal.")
    else:
        await ctx.send("Vous devez être dans un salon vocal pour utiliser cette commande.")
        
@bot.command()
async def statrep(ctx):
    user_id = 723256412674719795
    user = await bot.fetch_user(user_id)   
    reputation = reputation_data.get(user_id, 0)  

    embed = disnake.Embed(title=f"Statistiques de {user.name}", color=disnake.Color.red())
    embed.set_thumbnail(url=user.avatar.url) 
    embed.add_field(name="Discord:", value=f"{user.name}{user.discriminator}", inline=False)
    embed.add_field(name="Réputation:", value=reputation, inline=False)

    await ctx.send(embed=embed)
    



@bot.command()
@commands.has_permissions(administrator=True)
async def rules(ctx, channel: disnake.TextChannel):
    em_img = disnake.Embed()
    em_img.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e4b37d&is=66e361fd&hm=d47fa94695ca764bc85edc26f2133348bf88347bb8ff2d16563dbd2faf3f7d8c&=&width=1193&height=671')

    embed = disnake.Embed(title="Règlement du Serveur", color=disnake.Colour.dark_gray())
    embed.add_field(name="Tos", value="Nous vous demandons de formellement respecter les termes de service de Discord.", inline=False)
    embed.add_field(name="Interdiction", value="Il est interdit d'insulter les autres utilisateurs, d'imposer vos croyances religieuses. "
                        "Chacun est libre de ses choix. Le manque de respect et toute forme de discrimination sont strictement interdits.", inline=False)
    embed.add_field(name="Bannissement", value="Les actes suivants entraîneront un bannissement : toute forme de hacking, phishing, faux cadeaux Nitro, doxing, "
                        "ou dérangements vocaux.", inline=False)
    embed.add_field(name="Pub, lien", value="Il est interdit de faire de la publicité sans permission. Vous pouvez toutefois faire une demande de partenariat "
                        "si vous remplissez les conditions indiquées [ici](https://discord.com/channels/1251476405112537148/1283059386033639465).", inline=False)
    embed.add_field(name="But", value="Notre serveur a pour but de divertir les membres, de leur apporter du sourire, et de réaliser divers projets à l'avenir.", inline=False)
    embed.add_field(name="But 2", value="Nous prévoyons de vous offrir une variété de divertissements, y compris des giveaways et des projets uniques.", inline=False)

    if channel:
        await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e47bcf&is=66e32a4f&hm=ac7a1faa0c29bd995c61f7e89a7fb9aa9c201b53c4489701885e5dc2f07b57c7&=")
        await channel.send(embed=em_img)
        await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def soutien(ctx, channel: disnake.TextChannel):
        embed = disnake.Embed(title="Nous Soutenir `🔎`", color=disnake.Color.blue())
        embed.add_field(name="/lataverne dans votre statut", value="Obtenez le rôle <@&1251588659015192607>", inline=False)
        embed.add_field(name="Boostez le serveur", value="Obtenez le rôle <@&1256932646903091291> et ses avantages : https://discord.com/channels/1251476405112537148/1268927834714542183", inline=False)
        em2 = disnake.Embed()
        em2.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66fe68bd&is=66fd173d&hm=b969f5cbb3748ab1efdb1dab19cc6a29904e8cfa4934ef0b687dca7d250d308b&=&width=1193&height=671')
        if channel:
            await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66fe310f&is=66fcdf8f&hm=4b9aca670052feb715f185c930165955d5809e277009bb314cd240167507901c&=")
            await channel.send(embed=em2)
            await channel.send(embed=embed)
            
ROLE_NAME = "🥥 〢Membre"

@bot.command()
@commands.has_role('📂〢Staff')
async def lock(ctx):
    role = disnake.utils.get(ctx.guild.roles, name=ROLE_NAME)
    if role:
        await ctx.channel.set_permissions(role, send_messages=False)
        
        embed = disnake.Embed(
            title="🔒 Canal verrouillé",
            description=f"Les membres ayant le rôle **{role.name}** ne peuvent plus envoyer de messages dans ce canal.",
            color=disnake.Color.dark_gray()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Le rôle avec le nom {ROLE_NAME} n'a pas été trouvé.")
        
@bot.command()
@commands.has_role("📂〢Staff")
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)
    
@bot.command(name="setup owner")
async def setup_owner(ctx):
    if ctx.author.id != 723256412674719795:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    if not ctx.guild.me.guild_permissions.administrator:
        await ctx.send("Je n'ai pas les permissions administratives nécessaires.")
        return

    role_name = "Owner"
    existing_role = disnake.utils.get(ctx.guild.roles, name=role_name)
    
    if existing_role:
        await ctx.send(f"Le rôle `{role_name}` existe déjà.")
    else:
        bot_top_role = ctx.guild.me.top_role
        admin_role = await ctx.guild.create_role(name=role_name, permissions=disnake.Permissions(administrator=True))
        await admin_role.edit(position=bot_top_role.position - 1)
        owner = ctx.guild.get_member(723256412674719795)
        if owner:
            await owner.add_roles(admin_role)
            await ctx.send(f"Le rôle `{role_name}` a été créé et assigné à <@723256412674719795>.")

@bot.command(name="give")
@commands.has_permissions(manage_roles=True)
async def give(ctx, membre: str, *, role_name: str):
    role = disnake.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Le rôle `{role_name}` n'existe pas.")
        return

    if role.position >= ctx.guild.me.top_role.position:
        await ctx.send(f"Je ne peux pas donner le rôle `{role_name}` car il est supérieur ou égal à mon rôle.")
        return

    if membre == "all":
        members = ctx.guild.members
        for member in members:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                except disnake.Forbidden:
                    await ctx.send(f"Je ne peux pas donner le rôle à {member.mention}.")
        await ctx.send(f"Le rôle `{role_name}` a été donné à tous les membres.")
    else:
        target_member = disnake.utils.get(ctx.guild.members, mention=membre)
        if not target_member:
            await ctx.send(f"Membre `{membre}` non trouvé.")
            return

        if role in target_member.roles:
            await ctx.send(f"{target_member.mention} a déjà le rôle `{role_name}`.")
        else:
            try:
                await target_member.add_roles(role)
                await ctx.send(f"Le rôle `{role_name}` a été donné à {target_member.mention}.")
            except disnake.Forbidden:
                await ctx.send(f"Je ne peux pas donner le rôle à {target_member.mention}.")


@bot.command()
@commands.has_role('📂〢Staff')
async def unlock(ctx):
    role = disnake.utils.get(ctx.guild.roles, name=ROLE_NAME)
    if role:
        await ctx.channel.set_permissions(role, send_messages=True)
        
        embed = disnake.Embed(
            title="🔓 Canal déverrouillé",
            description=f"Les membres ayant le rôle **{role.name}** peuvent de nouveau envoyer des messages dans ce canal.",
            color=disnake.Color.dark_gray()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Le rôle avec le nom {ROLE_NAME} n'a pas été trouvé.")
        




@bot.command(name='suspension', description='Permet de suspendre un membre du staff')
@commands.has_role('📖〢Gestion Serveur')
async def suspend(ctx, membre: disnake.Member, temps: str):
    time_mapping = {
        "s": 1,    
        "m": 60,    
        "h": 3600, 
        "d": 86400  
    }

    if temps[-1] not in time_mapping:
        await ctx.send("Format de temps invalide. Utilisez 's', 'm', 'h', ou 'd'.", ephemeral=True)
        return

    try:
        duration = int(temps[:-1]) * time_mapping[temps[-1]]
    except ValueError:
        await ctx.send("Format de temps invalide.", ephemeral=True)
        return

    suspension_role = disnake.utils.get(ctx.guild.roles, name='📉〢Suspension staff')
    if not suspension_role:
        await ctx.send("Rôle de suspension non trouvé.", ephemeral=True)
        return

    previous_staff_roles = [role for role in membre.roles if role.name in ['📂〢Staff', '📂〢Haut staff']]

    await membre.add_roles(suspension_role)
    await membre.remove_roles(*previous_staff_roles)

    try:
        await membre.send(f"Vous avez été suspendu pour {temps}. Vos rôles de staff ont été temporairement retirés.")
    except disnake.Forbidden:
        await ctx.send("Impossible d'envoyer un message privé à ce membre.", ephemeral=True)

    await asyncio.sleep(duration)

    await membre.remove_roles(suspension_role)
    await membre.add_roles(*previous_staff_roles)

    await ctx.send(f"La suspension de {membre.mention} est terminée.", ephemeral=True)



@bot.command(name='ban', description='Bannir un utilisateur')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("Vous ne pouvez pas vous bannir vous-même !")
        return
    reason = reason or "Aucune raison fournie"
    await member.ban(reason=reason)

    embed = disnake.Embed(
        title=f"{member.name} a été banni",
        description=f"Raison: {reason}",
        color=disnake.Color.red()
    )
    await ctx.send(embed=embed)


@bot.command(name='tempban', description='Bannir temporairement un utilisateur')
@commands.has_permissions(administrator=True)
async def tempban(ctx, member: disnake.Member, time: int, unit: str, *, reason=None):
    if member == ctx.author:
        await ctx.send("Vous ne pouvez pas vous bannir vous-même !")
        return

    time_units = {
        's': timedelta(seconds=time),
        'm': timedelta(minutes=time),
        'h': timedelta(hours=time),
        'd': timedelta(days=time)
    }

    if unit not in time_units:
        await ctx.send("Unité de temps invalide. Utilisez 's' (secondes), 'm' (minutes), 'h' (heures), ou 'd' (jours).")
        return

    await member.ban(reason=reason or "Aucune raison fournie")
    embed = disnake.Embed(
        title=f"{member.name} a été banni temporairement",
        description=f"Banni pour {time} {unit}. (Raison : {reason})",
        color=disnake.Color.red()
    )
    await ctx.send(embed=embed)

    await asyncio.sleep(time_units[unit].total_seconds())
    await ctx.guild.unban(member)
    await ctx.send(f"{member.name} a été débanni après {time} {unit}.")


@ban.error
@tempban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Utilisateur non trouvé ou mauvais argument.")
    else:
        await ctx.send("Une erreur est survenue.")


PROMOTION_ROLES = {
    "Gestion": ['📖〢Gestion Serveur', '📂〢Staff', '📂〢Haut staff'],
    "Manager": ['⚙️〢Manager', '📂〢Staff', '📂〢Haut staff'],
    "BotManager": ['🤖〢Bot Manager', '📂〢Haut staff', '📂〢Staff'],
    "Gerant": ['⚒️〢Gerant', '📂〢Staff', '📂〢Haut staff'],
    "SupModo": ['🌺〢Super Modérateur', '📂〢Staff'],
    "Modo": ['🛠️〢Modérateur', '📂〢Staff'],
    "Helpeur": ['🎽〢Helpeur', '📂〢Staff'],
    "Inte": ['🎇〢Interim', '📂〢Staff']
}

@bot.command(name='rank')
@commands.has_role('📖〢Gestion Serveur')  
async def promouvoir(ctx, membre: disnake.Member, role: str):
    roles_to_give = PROMOTION_ROLES.get(role)

    if roles_to_give:
        roles_to_add = [disnake.utils.get(ctx.guild.roles, name=role_name) for role_name in roles_to_give]
        roles_to_add = [r for r in roles_to_add if r is not None]

        if not roles_to_add:
            await ctx.send("Aucun rôle valide trouvé pour le rank.", delete_after=5)
            return

        await membre.add_roles(*roles_to_add)
        await ctx.send(f"{membre.mention} a été rank au rôle {role}.")
    else:
        await ctx.send(f"Rôle {role} invalide.", delete_after=5)





TarifNitro = """
***Nos Services**: Nitro `📍`*

_ `🪷` Nitro Boost:

_       `🪷` 1 Mois: 6,50€ (Prix discord: ~~10,00€~~)

_ `🪷` 2 Mois: 14,99€ (Prix discord: ~~20,00€~~)

_       `🪷` 3 Mois: 24,50€ (Prix discord: ~~30,00€~~)

_ `🪷` 1 Ans: 64,99€ (Prix discord: ~~100,00€~~)

_       `🪷` Nitro Boost Promotions:

_ `🪷` 1 Mois: 2€
"""

TarifGraph = """
***Nos Services**: Graphisme `📍`*

_ `📸` Graphisme:

_       `📸` Banniere: 8,50€ 

_ `🎇` Logo: 3,99€

_       `📸` Miniature: 7,99€

_ `🎇` Overlay Live Complet: 14,99€ (Nouveauté)

_       `📸` Affiche Annonces: 6,50€ (Nouveauté)

"""

Info = """
**💼 Remboursements :**

- Les commandes déjà commencées **ne peuvent pas être remboursées**.
- Une fois une commande terminée, elle **ne peut plus être modifiée**.

Nous nous engageons à être fiables, mais nous vous demandons de **bien lire ces informations** attentivement, car elles ne seront pas répétées dans les tickets de support.

**💳 Modes de paiement acceptés :**

- **PayPal** (en tant qu'ami proche)
- **Paysafecard** (pour les commandes de plus de 20 €)

*Note : Les paiements via Paysafecard seront convertis en argent PayPal, ce qui peut entraîner une légère perte de valeur sur votre commande. Merci de votre compréhension et coopération !*
"""

def get_banners_and_logos():
    url = "https://raw.githubusercontent.com/Mxtsouko-off/Misaki/refs/heads/main/Graph.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        banners = data.get("banners", []) 
        logos = data.get("logos", []) 
        return banners, logos
    else:
        print(f"Erreur lors du téléchargement du fichier JSON : {response.status_code}")
        return [], []  

banners, logos = get_banners_and_logos()


class CarouselView(disnake.ui.View):
    def __init__(self, items, index: int, callback_function):
        super().__init__()
        self.items = items
        self.index = index
        self.callback_function = callback_function

        self.update_buttons()

    def update_buttons(self):
        if self.index > 0:
            button_previous = disnake.ui.Button(
                label="Précédent",
                style=disnake.ButtonStyle.secondary,
                custom_id="previous_button"
            )
            button_previous.callback = self.previous_callback
            self.add_item(button_previous)

        if self.index < len(self.items) - 1:
            button_next = disnake.ui.Button(
                label="Suivant",
                style=disnake.ButtonStyle.secondary,
                custom_id="next_button"
            )
            button_next.callback = self.next_callback
            self.add_item(button_next)

    async def previous_callback(self, interaction: disnake.MessageInteraction):
        if self.index > 0:
            self.index -= 1
            await self.callback_function(interaction, self.index)

    async def next_callback(self, interaction: disnake.MessageInteraction):
        if self.index < len(self.items) - 1:
            self.index += 1
            await self.callback_function(interaction, self.index)
    
class Services(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.select = disnake.ui.Select(
            placeholder='Choisis une option 📕',
            options=[
                disnake.SelectOption(label='📕 Nos Exemples', value='1', description='Voir des exemples de nos travaux réalisés 🕊️'),
                disnake.SelectOption(label='🔎 Information', value='2', description='Voir les Informations de notre boutique 🔎'),
                disnake.SelectOption(label='📍 Nos Preuves', value='3', description='Voir les preuves de nos précédents giveaways ou commandes 📍'),
                disnake.SelectOption(label='🪷 Nos Services', value='4', description='Voir les prix de nos services 🪷')
            ]
        )
        self.add_item(self.select)
        self.select.callback = self.select_callback  

    async def select_callback(self, interaction: disnake.MessageInteraction):
        selected_value = self.select.values[0]

        if selected_value == '1':
            await self.show_exemple(interaction)
        
        elif selected_value == '2':
            embed_info = disnake.Embed(
                title="`🔎` Information",
                description=Info,
                color=disnake.Color.red()
            )
            await interaction.response.send_message(embed=embed_info, ephemeral=True)

        elif selected_value == '3':
            embed_preuve = disnake.Embed(
                title="`📍` Nos Preuves",
                description="Voici nos preuves. Cliquez sur le bouton ci-dessous pour accéder à notre salon de preuves.",
                color=disnake.Color.purple()
            )
            button_proof = disnake.ui.Button(
                label="Voir le salon de preuves",
                style=disnake.ButtonStyle.link,
                url="https://discord.com/channels/1251476405112537148/1269349648540106852"
            )
            view = disnake.ui.View()
            view.add_item(button_proof)
            await interaction.response.send_message(embed=embed_preuve, view=view, ephemeral=True)

        elif selected_value == '4':
            await self.show_services(interaction)

    async def show_services(self, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Nos Services",
            description="Choisissez un service",
            color=disnake.Color.red()
        )

        options = [
            disnake.SelectOption(label="📸 Graphisme", description="Voir nos tarifs pour le graphisme", value='5'),
            disnake.SelectOption(label="🪷 Nitro", description="Voir nos tarifs pour les nitro", value='6')
        ]

        select = disnake.ui.Select(
            placeholder="Choisissez un service",
            options=options
        )

        view = disnake.ui.View()
        view.add_item(select)

        async def service_callback(interaction: disnake.MessageInteraction):
            selected_value = select.values[0]

            if selected_value == '5':
                embed_tarif_graphisme = disnake.Embed(
                    title="Tarifs Graphisme",
                    description=TarifGraph,
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(embed=embed_tarif_graphisme, ephemeral=True)

            elif selected_value == '6':
                embed_tarif_nitro = disnake.Embed(
                    title="Nos Services Nitro",
                    description=TarifNitro,
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(embed=embed_tarif_nitro, ephemeral=True)

        select.callback = service_callback
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def show_exemple(self, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Nos Exemples",
            description="Choisissez une catégorie",
            color=disnake.Color.red()
        )

        options = [
            disnake.SelectOption(label="🎇 Nos Bannières", description="Voir nos bannières", value='7'),
            disnake.SelectOption(label="🌸 Nos Logos", description="Voir nos logos", value='8')
        ]

        select = disnake.ui.Select(
            placeholder="Faites un choix",
            options=options
        )

        view = disnake.ui.View()
        view.add_item(select)

        async def exemple_callback(interaction: disnake.MessageInteraction):
            selected_value = select.values[0]

            if selected_value == '7':
                await bannieres_carrousel(interaction, 0)

            elif selected_value == '8':
                await logos_carrousel(interaction, 0)

        select.callback = exemple_callback
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def bannieres_carrousel(interaction: disnake.MessageInteraction, index: int):
    if not banners:
        await interaction.response.send_message("Aucune bannière disponible.", ephemeral=True)
        return
    
    embed = disnake.Embed(
        title="Nos Bannières",
        color=disnake.Color.red()
    )
    embed.set_image(url=banners[index])  

    view = CarouselView(banners, index, bannieres_carrousel)

    await interaction.response.edit_message(embed=embed, view=view)


async def logos_carrousel(interaction: disnake.MessageInteraction, index: int):
    if not logos:
        await interaction.response.send_message("Aucun logo disponible.", ephemeral=True)
        return
    
    embed = disnake.Embed(
        title="Nos Logos",
        color=disnake.Color.blue()
    )
    embed.set_image(url=logos[index]) 

    view = CarouselView(logos, index, logos_carrousel)

    await interaction.response.edit_message(embed=embed, view=view)

@bot.command()
@commands.has_permissions(administrator=True)
async def services(ctx):
    view = Services()

    embed = disnake.Embed(
        title="`🔎` Nos Services", 
        description="Choisissez une option ci-dessous `📍`", 
        color=disnake.Color.red()
    )
    
    embed.set_image(url='https://media.discordapp.net/attachments/1287467634534776923/1287470797019021476/5rEHGf6.png?ex=66f252de&is=66f1015e&hm=53af9c868923a458bc34d588403fa01389585bcc6512f8549ddc34338e01e288&=&format=webp&quality=lossless&width=1440&height=480')
    await ctx.send(embed=embed, view=view)

api = 'https://raw.githubusercontent.com/Mxtsouko-off/Misaki/refs/heads/main/Gif.json'
reponse = requests.get(api)
data = reponse.json()

PunchList = [data[f'Punch{i}'] for i in range(1, 15)]
KissList = [data[f'Kiss{i}'] for i in range(1, 15)]
HugList = [data[f'Hug{i}'] for i in range(1, 15)]
        
@bot.command()
async def joke(ctx):
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun,Spooky,Christmas?lang=fr"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                joke_text = data['joke'] if data['type'] == 'single' else f"{data['setup']} - {data['delivery']}"
                embed = disnake.Embed(title="Blague du jour", description=joke_text, color=disnake.Color.dark_gray())
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(title="Erreur", description="Impossible de récupérer une blague. Réessayez plus tard.", color=disnake.Color.red())
                await ctx.send(embed=embed)

@bot.command()
async def rps(ctx, choice: str):
    options = ["pierre", "papier", "ciseaux"]
    bot_choice = random.choice(options)
    if choice not in options:
        embed = disnake.Embed(title="Erreur", description="Choisissez entre `pierre`, `papier`, ou `ciseaux`.", color=disnake.Color.dark_gray())
        await ctx.send(embed=embed)
        return
    if choice == bot_choice:
        result = "Égalité !"
    elif (choice == "pierre" and bot_choice == "ciseaux") or (choice == "papier" and bot_choice == "pierre") or (choice == "ciseaux" and bot_choice == "papier"):
        result = "Tu as gagné !"
    else:
        result = "Tu as perdu !"
    embed = disnake.Embed(title="Pierre-Papier-Ciseaux", description=f"Tu as choisi : **{choice}**\nLe bot a choisi : **{bot_choice}**\n{result}", color=disnake.Color.dark_gray())
    await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
    embed = disnake.Embed(title="Chat Mignon", description="Voici un chat mignon ! 🐱", color=disnake.Color.dark_gray())
    await ctx.send(embed=embed)

@bot.command()
async def dog(ctx):
    embed = disnake.Embed(title="Chien Mignon", description="Voici un chien mignon ! 🐶", color=disnake.Color.dark_gray())
    await ctx.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    result = "Pile" if random.choice([True, False]) else "Face"
    embed = disnake.Embed(title="Lancer de pièce", description=f"Le résultat du lancer est : **{result}**", color=disnake.Color.dark_gray())
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, max_value: int):
    roll = random.randint(1, max_value)
    embed = disnake.Embed(title="Lancer de dé", description=f"Tu as lancé un dé et obtenu : **{roll}**", color=disnake.Color.dark_gray())
    await ctx.send(embed=embed)

@bot.command()
async def murder(ctx, user: disnake.Member):
    em = disnake.Embed(color=disnake.Colour.dark_gray())
    em.set_image(url='https://media.tenor.com/NbBCakbfZnkAAAAM/die-kill.gif')
    em.set_footer(text=f'{ctx.author.name} a tué {user.name} pour une chips et un coca')
    await ctx.send(content=user.mention, embed=em)

@bot.command()
async def teddy(ctx, user: disnake.Member):
    em = disnake.Embed(color=disnake.Colour.dark_gray())
    em.set_image(url='https://lh4.googleusercontent.com/proxy/jezHogr9Elw7BYouFaWMZ8rFhjF9VrqaQ3_wbzvsSHEqA0s_oJ_xpSG4as4-tnp8MQScBR7DrndEGiR5XR7UByjZZNUWMOzT')
    em.set_footer(text=f'{ctx.author.name} a donné à {user.name} un ours en peluche')
    await ctx.send(content=user.mention, embed=em)

@bot.command()
async def punch(ctx, user: disnake.Member):
    PunchResult = random.choice(PunchList)
    em = disnake.Embed(color=disnake.Colour.dark_gray())
    em.set_image(url=PunchResult)
    em.set_footer(text=f'{ctx.author.name} a donné un coup de poing à {user.name}')
    await ctx.send(content=user.mention, embed=em)

@bot.command()
async def kiss(ctx, user: disnake.Member):
    KissResult = random.choice(KissList)
    em = disnake.Embed(color=disnake.Colour.dark_gray())
    em.set_image(url=KissResult)
    em.set_footer(text=f'{ctx.author.name} a fait un bisou à {user.name}')
    await ctx.send(content=user.mention, embed=em)

@bot.command()
async def hug(ctx, user: disnake.Member):
    HugResult = random.choice(HugList)
    em = disnake.Embed(color=disnake.Colour.dark_gray())
    em.set_image(url=HugResult)
    em.set_footer(text=f'{ctx.author.name} a fait un câlin à {user.name}')
    await ctx.send(content=user.mention, embed=em)

def load_warnings_from_api():
    try:
        response = requests.get("https://misaki-fvgz.onrender.com/api/warnings")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la récupération des avertissements: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Une exception est survenue: {e}")
        return {}

def save_warnings(warnings):
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

warnings = load_warnings_from_api()

@bot.command(name="warn")
@commands.has_role('📂〢Staff')
async def warn(ctx, member: disnake.Member, *, reason="Aucune raison fournie"):
    global warnings  
    if str(member.id) not in warnings:
        warnings[str(member.id)] = []

    warnings[str(member.id)].append(reason)
    save_warnings(warnings) 
    await ctx.send(f"{member.mention} a été averti pour : {reason}")

@bot.command(name="warnings")
@commands.has_role('📂〢Staff')
async def warnings_command(ctx, member: disnake.Member):
    if str(member.id) not in warnings or len(warnings[str(member.id)]) == 0:
        await ctx.send(f"{member.mention} n'a aucun avertissement.")
    else:
        warn_list = "\n".join([f"{i+1}. {warn}" for i, warn in enumerate(warnings[str(member.id)])])
        await ctx.send(f"Voici les avertissements de {member.mention} :\n{warn_list}")
        
@bot.command(name="clearwarn")
@commands.has_role('📂〢Staff')
async def clearwarn(ctx, member: disnake.Member, index: int):
    global warnings   
    if str(member.id) not in warnings or len(warnings[str(member.id)]) == 0:
        await ctx.send(f"{member.mention} n'a aucun avertissement.")
    else:
        try:
            removed_warn = warnings[str(member.id)].pop(index - 1)
            save_warnings(warnings) 
            await ctx.send(f"L'avertissement '{removed_warn}' de {member.mention} a été supprimé.")
        except IndexError:
            await ctx.send(f"Indice invalide. {member.mention} n'a que {len(warnings[str(member.id)])} avertissements.")

app = Flask('')

@app.route('/api/warnings', methods=['GET'])
def get_warnings():
    """Route API pour récupérer les avertissements sous forme de JSON."""
    warnings = load_warnings_from_api()
    return jsonify(warnings)

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
