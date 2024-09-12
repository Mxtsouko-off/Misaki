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
from flask import Flask
from threading import Thread


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

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

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
        name=".cookies @utilisateur",
        value="Donnez un cookie à un autre utilisateur.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".pokeball @utilisateur",
        value="Utilisez cette commande pour capturer un utilisateur.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".teddy @utilisateur",
        value="Donnez un ours en peluche à un autre utilisateur.",
        inline=False
    )
    
    embed_fun.add_field(
        name=".murder @utilisateur",
        value="Utilisez cette commande pour 'tuer' un utilisateur pour un chips et un coca.",
        inline=False
    )

    embed_fun.add_field(
        name=".match random",
        value="Découvrez le pourcentage d'amour que vous avez avec un membre aléatoire du serveur.",
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
        name="/promouvoir @utilisateur",
        value="Promouvez un membre.",
        inline=False
    )

    await ctx.send(embed=embed_moderation)


    embed_owner = disnake.Embed(
        title="**Owner (Mxtsouko)** - Commandes",
        description="Commandes réservées à l'owner.",
        color=disnake.Color.gold()
    )
    
    embed_owner.add_field(
        name=".banner channel link",
        value="Ajoutez une bannière dans nos bannières.",
        inline=False
    )
    
    embed_owner.add_field(
        name=".logo channel link",
        value="Ajoutez un logo dans nos logos.",
        inline=False
    )
    
    embed_owner.add_field(
        name=".minia channel link",
        value="Ajoutez une miniature dans nos miniatures.",
        inline=False
    )

    await ctx.send(embed=embed_owner)

    


Pub = '''
_ _                               ***/LaTaverne*** ``🍻`` *!*

_ _    ✧･    ``🌸``** Animes**    ⨯˚₊‧    ``🎉`` **Giveaways**    ･⊹

_ _                ⊹･    ``🎨``** Graphisme**    ⨯˚₊‧    ``🎊`` **Nitro**    ･✧

_ _    ✧･    ``🎮``** Gaming**    ⨯˚₊‧    ``💻`` **Developement**    ･⊹

_ _                           ⊹･    ``⚙️``** Optimisation**    ･⊹

_ _``📣`` **Recrutement Ouvert & Partenariat également ouvert**

_ _                                     [``🪭`` **Rejoignez-nous **](https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66de1bfd&is=66dcca7d&hm=2101c534687cb4eab0396f632e53817f56db5fcbf0175b0304ebd375abd39c2b&=&width=1193&height=671) *!*  

_ _                                https://discord.gg/x7G3vgx9kK
'''

class Gif:
    Punch1 = 'https://c.tenor.com/f3J-yZcZfU0AAAAC/tenor.gif'
    Punch2 = 'https://media.tenor.com/nF_grpASXygAAAAj/bubu-dudu.gif'
    Punch3 = 'https://media.tenor.com/XIkC63044qYAAAAj/nico-and-sen-frog-helicopter-punch.gif'
    Punch4 = 'https://media.tenor.com/_xAtEAKEbuQAAAAj/porkcoin-pork.gif'
    Punch5 = 'https://media.tenor.com/CArnMwDCNPwAAAAj/jinzhan-lily-and-marigold.gif'
    Punch6 = 'https://media.tenor.com/ntFYu5-eBy4AAAAj/fgo-fate.gif'
    Punch7 = 'https://c.tenor.com/kw5lYGbw8oAAAAAC/tenor.gif'
    Punch8 = 'https://media.tenor.com/yA_KtmPI1EMAAAAM/hxh-hunter-x-hunter.gif'
    Punch9 = 'https://media.tenor.com/YGKPpkNN6g0AAAAM/anime-jujutsu-kaisen-anime-punch.gif'
    Punch10 = 'https://media.tenor.com/Kbit6lroRFUAAAAM/one-punch-man-saitama.gif'
    Punch11 = 'https://media.tenor.com/gmvdv-e1EhcAAAAM/weliton-amogos.gif'
    Punch12 = 'https://media.tenor.com/YQ08ifsOb0EAAAAM/anime-angry.gif'
    Punch13 = 'https://media.tenor.com/hu9e3k1zr0IAAAAM/pjsk-pjsk-anime.gif'
    Punch14 = 'https://media.tenor.com/OYv6aDua76wAAAAM/hanagaki-takemichi-takemichi.gif'
    Punch15 = 'https://media.tenor.com/tItp51ABXK4AAAAM/punch-eren.gif'

    Hug1 = 'https://media.tenor.com/MVK93pHLpz4AAAAM/anime-hug-anime.gif'
    Hug2 = 'https://media.tenor.com/c2SMIhi33DMAAAAM/cuddle-bed-hug.gif'
    Hug3 = 'https://media.tenor.com/J7eGDvGeP9IAAAAM/enage-kiss-anime-hug.gif'
    Hug4 = 'https://media.tenor.com/wWFm70VeC7YAAAAM/hug-darker-than-black.gif'
    Hug5 = 'https://media.tenor.com/kCZjTqCKiggAAAAM/hug.gif'
    Hug6 = 'https://media.tenor.com/qVWUEYImyKAAAAAM/sad-hug-anime.gif'
    Hug7 = 'https://media.tenor.com/bLttPccI_I4AAAAM/cuddle-anime.gif'
    Hug8 = 'https://media.tenor.com/iyztKN68avcAAAAM/aharen-san-aharen-san-anime.gif'
    Hug9 = 'https://media.tenor.com/RWD2XL_CxdcAAAAM/hug.gif'
    Hug10 = 'https://media.tenor.com/jSr41Jz0CQYAAAAM/anime-hug-anime-girls.gif'
    Hug11 = 'https://media.tenor.com/sl3rfZ7mQBsAAAAM/anime-hug-canary-princess.gif'
    Hug12 = 'https://media.tenor.com/SAL_XAuyuJAAAAAM/cute-anime.gif'
    Hug13 = 'https://media.tenor.com/Y9J2vBrjPCsAAAAM/anime-anime-hug.gif'
    Hug14 = 'https://media.tenor.com/oB-fcENXEasAAAAM/juvia-meredy.gif'
    Hug15 = 'https://media.tenor.com/kCBUETL9jPAAAAAM/anime-hug.gif'

    Kiss1 = 'https://media.tenor.com/OByUsNZJyWcAAAAM/emre-ada.gif'
    Kiss2 = 'https://media.tenor.com/rm3WYOj5pR0AAAAM/engage-kiss-anime-kiss.gif'
    Kiss3 = 'https://media.tenor.com/XB3mEB77l7EAAAAM/kiss.gif'
    Kiss4 = 'https://media.tenor.com/dn_KuOESmUYAAAAM/engage-kiss-anime-kiss.gif'
    Kiss5 = 'https://media.tenor.com/79RkCtre5XYAAAAM/a-sign-of-affection-yuki-and-itsuomi-kiss.gif'
    Kiss6 = 'https://media.tenor.com/sn-5HBmgdPgAAAAM/kiss-anime-anime.gif'
    Kiss7 = 'https://media.tenor.com/GoPV-W2pxMUAAAAM/kiss.gif'
    Kiss8 = 'https://media.tenor.com/6HDHE1KRK_wAAAAM/kiss-anime.gif'
    Kiss9 = 'https://media.tenor.com/3xrkm45MqkIAAAAM/anime-kiss.gif'
    Kiss10 = 'https://media.tenor.com/YHxJ9NvLYKsAAAAM/anime-kiss.gif'
    Kiss11 = 'https://media.tenor.com/cKJjPT4OdC0AAAAM/kiss-anime-kiss-anime-couple-gif.gif'
    Kiss12 = 'https://media.tenor.com/Fyq9izHlreQAAAAM/my-little-monster-haru-yoshida.gif'
    Kiss13 = 'https://media.tenor.com/GdQYPbRffvAAAAAM/matching-anime.gif'
    Kiss14 = 'https://media.tenor.com/0bVlu72sZGMAAAAM/tonikawa-tonikaku-kawaii.gif'
    Kiss15 = 'https://media.tenor.com/1jXN_ObuwV0AAAAM/lick-cat-licking.gif'


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "/Taverne/Pub" in message.content:
        await message.channel.send(content=message.author.mention)
        await message.channel.send(Pub)

    if "/Taverne/Hierarchie" in message.content:
        await message.channel.send(content=message.author.mention)
        await message.channel.send("https://discord.com/channels/1251476405112537148/1268870540794269698")

    if "Bonjour" in message.content:
        await message.channel.send(f"Bonjour {message.author.mention} <:coucouw:1282620654788542509>")

    if "Salut" in message.content:
        await message.channel.send(f"Salut {message.author.mention} <:coucouw:1282620654788542509>")

    if "Coucou" in message.content:
        await message.channel.send(f"Coucou {message.author.mention} <:coucouw:1282620654788542509>")

    if isinstance(message.channel, disnake.DMChannel) and message.author != bot.user:
        guild = disnake.utils.get(bot.guilds, name="La Taverne 🍻")
        logs_channel = disnake.utils.get(guild.text_channels, name="📁〃logs-misaki")

        if logs_channel is None:
            return

        warning_message = "⚠️ Attention : cette conversation est retranscrite dans le serveur **La Taverne 🍻**. N'hésitez pas à poser toutes vos questions ici."
        await message.channel.send(warning_message)

        embed = disnake.Embed(
            title="Nouveau Message Privé",
            description=f"**Auteur**: {message.author.mention}\n**Contenu**: {message.content}",
            color=disnake.Color.blue()
        )
        await logs_channel.send(embed=embed)

        member = guild.get_member(message.author.id)
        if member and (member.guild_permissions.administrator or any(role.id == 1280429826414477373 for role in member.roles)):
            await bot.process_commands(message)
            return

        if re.search(r'discord\.gg|discord\.com|discord\.me|discord\.app|discord\.io', message.content, re.IGNORECASE):
            await message.delete()
            warning_message = await message.channel.send(f"{message.author.mention}, les liens Discord ne sont pas autorisés dans ce serveur.")
            await asyncio.sleep(5)
            await warning_message.delete()
            return

    await bot.process_commands(message)



@bot.command()
@commands.has_permissions(administrator=True)
async def partner(self, ctx, channel: disnake.TextChannel):
        embed_image = disnake.Embed(color=disnake.Colour.dark_gray())
        embed_image.set_image(url='...')

        embed = disnake.Embed(title='Conditions', color=disnake.Colour.dark_gray())
        embed.add_field(name='Membres:', value='Minimum 15 (sans les bots)', inline=False)
        embed.add_field(name='Partenariat:', value="Pas de serveur NSFW...", inline=False)

        if channel:
            await channel.send('...')
            await channel.send(embed=embed_image)
            await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def reglement(self, ctx, channel: disnake.TextChannel):
        embed = disnake.Embed(title="Règlement du Serveur", color=disnake.Color.green())
        embed.add_field(name="Règle 1", value="Soyez respectueux envers les autres membres.", inline=False)
        embed.add_field(name="Règle 2", value="Pas de spam ni de publicité non autorisée.", inline=False)
        embed.add_field(name="Règle 3", value="Aucune forme de harcèlement ne sera tolérée.", inline=False)
        embed.add_field(name="Règle 4", value="Respectez les décisions des modérateurs.", inline=False)
        embed.add_field(name="Règle 5", value="Amusez-vous et faites-vous des amis!", inline=False)

        if channel:
            await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def soutien(self, ctx, channel: disnake.TextChannel):
        embed = disnake.Embed(title="Soutien", color=disnake.Color.blue())
        embed.add_field(name="Aide", value="Pour toute demande de soutien, veuillez contacter un modérateur.", inline=False)
        embed.add_field(name="Ressources", value="Vous pouvez consulter le canal de support pour des ressources supplémentaires.", inline=False)
        embed.add_field(name="Contact", value="N'hésitez pas à @mentionner un modérateur pour obtenir de l'aide.", inline=False)

        if channel:
            await channel.send(embed=embed)


@bot.command(name='suspension', description='Permet de suspendre un membre du staff')
@commands.has_role('📖〢Gestion Serveur')
async def suspension(ctx, membre: disnake.Member, temps: str):
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


@bot.command(name='réunion', description='Organiser une réunion staff')
@commands.has_any_role('📖〢Gestion Serveur', '📂〢Haut staff')
async def réunion(ctx, date: str, heures: str):
    channel = disnake.utils.get(ctx.guild.text_channels, name='💠〃réunion')  
    role_staff = disnake.utils.get(ctx.guild.roles, name='📂〢Staff')
    role_haut_staff = disnake.utils.get(ctx.guild.roles, name='📂〢Haut staff')

    if not channel:
        await ctx.send("Le salon de réunion spécifié n'existe pas.", delete_after=5)
        return

    embed = disnake.Embed(
        title='Annonce Réunion', 
        description=f'Une réunion aura lieu le {date} à {heures}.', 
        color=disnake.Color.blue()
    )
    embed.set_image(url='https://i.ibb.co/dbPZcmV/c92885e55b3f6deb5a626d0e4f984040.gif')

    await channel.send(content=f"{role_staff.mention} {role_haut_staff.mention}", embed=embed)
    await ctx.send(f"Réunion organisée pour le {date} à {heures}.", delete_after=3)


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


@bot.command(name='rm_staff', description='Enregistrer une plainte contre un membre du staff')
@commands.has_role('📂〢Staff')
async def rm_staff(ctx, membre: disnake.Member, plainte: str):
    guild = ctx.guild
    channel = disnake.utils.get(guild.text_channels, name="📑〃staff-bilan")
    if channel:
        embed = disnake.Embed(
            title=f"Plainte déposée contre {membre.name}",
            description=f"Raison : {plainte}",
            color=disnake.Colour.dark_gray()
        )
        await channel.send(embed=embed)
        await ctx.send(f"Plainte enregistrée contre {membre.name}.")
    else:
        await ctx.send("Le canal de bilan spécifié n'existe pas.")

PROMOTION_ROLES = {
    "Gestion": ['📖〢Gestion Serveur', '📂〢Staff', '📂〢Haut staff'],
    "Manager": ['⚙️〢Manager', '📂〢Staff', '📂〢Haut staff'],
    "BotManager": ['🤖〢Bot Manager', '📂〢Haut staff', '📂〢Staff'],
    "Gerant": ['⚒️〢Gerant', '📂〢Staff', '📂〢Haut staff'],
    "SuperModérateur": ['🌺〢Super Modérateur', '📂〢Staff'],
    "Moderateur": ['🛠️〢Modérateur', '📂〢Staff'],
    "Helpeur": ['🎽〢Helpeur', '📂〢Staff'],
    "Interim": ['🎇〢Interim', '📂〢Staff']
}

@bot.command(name='promouvoir', description='Promouvoir un membre')
@commands.has_role('📖〢Gestion Serveur')  
async def promouvoir(ctx, membre: disnake.Member, role: str):
    roles_to_give = PROMOTION_ROLES.get(role)

    if roles_to_give:
        roles_to_add = [disnake.utils.get(ctx.guild.roles, name=role_name) for role_name in roles_to_give]
        roles_to_add = [r for r in roles_to_add if r is not None]

        if not roles_to_add:
            await ctx.send("Aucun rôle valide trouvé pour la promotion.", delete_after=5)
            return

        await membre.add_roles(*roles_to_add)
        await ctx.send(f"{membre.mention} a été promu au rôle {role}.")
    else:
        await ctx.send(f"Rôle {role} invalide.", delete_after=5)


@bot.command(name='banner', description='Ajouter une nouvelle bannière')
async def banner(ctx, channel: disnake.TextChannel, link: str):
    utilisateur_autorise = 723256412674719795  

    if ctx.author.id != utilisateur_autorise:
        await ctx.send("Seule Mxtsouko peut utiliser cette commande.")
        return
    
    if channel:
        role = disnake.utils.get(channel.guild.roles, name='📣〢Notification Boutique')
        embed = disnake.Embed(
            title='Nouvelle bannière ajoutée', 
            description='Nos bannières sont entièrement faites à la main. Aucun site ou autre, elles sont toutes réalisées par notre graphiste.'
        )
        embed.set_image(url=link)
        embed.set_footer(text=f'Cette bannière a été postée par {ctx.author.name}')
        await channel.send(content=role.mention, embed=embed)


@bot.command(name='logo', description='Ajouter un nouveau logo')
async def logo(ctx, channel: disnake.TextChannel, link: str):
    utilisateur_autorise = 723256412674719795

    if ctx.author.id != utilisateur_autorise:
        await ctx.send("Seule Mxtsouko peut utiliser cette commande.")
        return

    if channel:
        role = disnake.utils.get(channel.guild.roles, name='📣〢Notification Boutique')
        embed = disnake.Embed(
            title='Nouveau logo ajouté', 
            description='Nos logos sont entièrement faits à la main. Aucun site ou autre, ils sont tous réalisés par notre graphiste.'
        )
        embed.set_image(url=link)
        embed.set_footer(text=f'Ce logo a été posté par {ctx.author.name}')
        await channel.send(content=role.mention, embed=embed)


@bot.command(name='minia', description='Ajouter une nouvelle miniature')
async def minia(ctx, channel: disnake.TextChannel, link: str):
    utilisateur_autorise = 723256412674719795

    if ctx.author.id != utilisateur_autorise:
        await ctx.send("Seule Mxtsouko peut utiliser cette commande.")
        return

    if channel:
        role = disnake.utils.get(channel.guild.roles, name='📣〢Notification Boutique')
        embed = disnake.Embed(
            title='Nouvelle miniature ajoutée', 
            description='Nos miniatures sont entièrement faites à la main. Aucun site ou autre, elles sont toutes réalisées par notre graphiste.'
        )
        embed.set_image(url=link)
        embed.set_footer(text=f'Cette miniature a été postée par {ctx.author.name}')
        await channel.send(content=role.mention, embed=embed)

PunchList = [Gif.Punch1, Gif.Punch2, Gif.Punch3, Gif.Punch4, Gif.Punch5, Gif.Punch6, Gif.Punch7, Gif.Punch8, Gif.Punch9, Gif.Punch10, Gif.Punch11, Gif.Punch12, Gif.Punch13, Gif.Punch14, Gif.Punch15]
KissList =  [Gif.Kiss1, Gif.Kiss2, Gif.Kiss3, Gif.Kiss4, Gif.Kiss5, Gif.Kiss6, Gif.Kiss7, Gif.Kiss8, Gif.Kiss9, Gif.Kiss10, Gif.Kiss11, Gif.Kiss12, Gif.Kiss13, Gif.Kiss14, Gif.Kiss15]
HugList = [Gif.Hug1, Gif.Hug2, Gif.Hug3, Gif.Hug4, Gif.Hug5, Gif.Hug6, Gif.Hug7, Gif.Hug8, Gif.Hug9, Gif.Hug10, Gif.Hug11, Gif.Hug12, Gif.Hug13, Gif.Hug14, Gif.Hug15]

        
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
