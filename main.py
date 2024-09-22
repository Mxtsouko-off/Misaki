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

    if "Notre Pub" in message.content:
        await message.channel.send(content=message.author.mention)
        await message.channel.send(Pub)

    if "Hierarchie" in message.content:
        await message.channel.send(content=message.author.mention)
        await message.channel.send("https://discord.com/channels/1251476405112537148/1268870540794269698")

    salutations = ["Bonjour", "Salut", "Coucou", "Yo"]
    if any(salutation in message.content for salutation in salutations):
        await message.channel.send(f"{message.content} {message.author.mention} <:coucouw:1282620654788542509>", delete_after=5)

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
        embed = disnake.Embed(title="Soutien", color=disnake.Color.blue())
        embed.add_field(name="Aide", value="Pour toute demande de soutien, veuillez contacter un modérateur.", inline=False)
        embed.add_field(name="Ressources", value="Vous pouvez consulter le canal de support pour des ressources supplémentaires.", inline=False)
        embed.add_field(name="Contact", value="N'hésitez pas à @mentionner un modérateur pour obtenir de l'aide.", inline=False)

        if channel:
            await channel.send(embed=embed)


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

@bot.command(name='promotion', description='promouvoir un membre')
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




banners = [
    "https://media.discordapp.net/attachments/1287467634534776923/1287467675362267267/JdnYHMP.png?ex=66f1a735&is=66f055b5&hm=57920b8135ee12c11386c360b99e94afc6eafc089add5dc3058fa8ab9572812b&=&format=webp&quality=lossless&width=960&height=320",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467676360380446/dNL13qo.png?ex=66f1a736&is=66f055b6&hm=5e7f20874ae8db6836afb862a40767455da466db95d370a1dd29a5a96ca679ad&=&format=webp&quality=lossless&width=960&height=320",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467676784136213/EWjjW4O.png?ex=66f1a736&is=66f055b6&hm=25d56c54155e04d989056da10ffa95281cb12d925df416b9c3d53b4dd1c0c9a6&=&format=webp&quality=lossless&width=960&height=320",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467677312352396/BRgncbr.png?ex=66f1a736&is=66f055b6&hm=f675c290d6cf6b32182f29efc93e1b4a4420ac7b92678201eb8ce7e854edda33&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467677819994132/pURXY13.png?ex=66f1a736&is=66f055b6&hm=b9ac3e700ed79ce203cbcc9b75dcf4b02f2d06e8a6eeb8510cab54ddbcca3b4c&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467678243623012/FUFqQfP.png?ex=66f1a736&is=66f055b6&hm=be3f528da10697872e10d297d7e7b44bc54e69d732f667a53024384490a0b439&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467717216960573/8WcvlSM.png?ex=66f1a73f&is=66f055bf&hm=bf274601495f24cca77a60d1f7422c6e70e0e5bcf900023f14dc18614e7d9b54&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467719683215360/qfevvsx.png?ex=66f1a740&is=66f055c0&hm=5f319ad55254da4375e196f28597eacbd494086c03eb56df8242fb21cf955215&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467720262025246/Tcvd7mp.png?ex=66f1a740&is=66f055c0&hm=4b00625ae94eb897591f3445869a4784bacfe8f83ea0c49de1974aa35f3d2acc&=&format=webp&quality=lossless&width=1440&height=415",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467720803356764/wy1dwCj.jpg?ex=66f1a740&is=66f055c0&hm=2af957d1d3ef1b0a12e9fc760be8b4a6d70c62601b20c21329d7603191cf32ff&=&format=webp&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467721205743647/YSXtX99.png?ex=66f1a740&is=66f055c0&hm=f1a8bab3a08e3807b0d3bb2fe46f154958da3246e94cfd06a7236a5639efea2c&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467721663189063/2Qv7NpL.png?ex=66f1a740&is=66f055c0&hm=383eeacc405ad72eccbdfed23aa8c6628db6b597d0bfca5249a7b313df1aaaed&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467722191667261/JtGDXts.png?ex=66f1a740&is=66f055c0&hm=ca04d562b530eb881442ca46f744dd83a2911a2cb39fc559025c40cb093e8232&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287467722740863077/DJDdYry.png?ex=66f1a741&is=66f055c1&hm=3579a450552026de1da347ac063a61d803f8c952011fa1ac72c80e11ee1d3fc1&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470796083695717/VOYGrMx.png?ex=66f1aa1d&is=66f0589d&hm=cb6f29b383779422cc764ada7cbf5c017c80382a9dc757624eb2d7d3f2931310&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470796603916338/Fm1XIGk.png?ex=66f1aa1d&is=66f0589d&hm=c9adfea7cff13af2cfca5ba6ffd0d612afd478dbcf28a296f9a331c2b7ba1864&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470797019021476/5rEHGf6.png?ex=66f1aa1e&is=66f0589e&hm=389a455cb50f857f3e63492d0d8fc28045f346c0af81e5bd61597ab4687f511f&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470797413421198/jOsmUKF.png?ex=66f1aa1e&is=66f0589e&hm=b23e58c00b97c1986865eebe9dc9c4f5e0219ef655061034ff93be960eeaef0f&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470797836783717/P5oXwbc.png?ex=66f1aa1e&is=66f0589e&hm=f6008b57b1f6ed0e66721f0959b5dc9c51b797549092d33bf0a2218a27b5e755&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470798315196448/x3jvSPu.png?ex=66f1aa1e&is=66f0589e&hm=c4c226f42f982c53749d03edd7b14deedbac700d1f7618296412b369d0df2eed&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470799011446815/9Vprxs1.png?ex=66f1aa1e&is=66f0589e&hm=6c8819353c7e29c65338c46a58db866f2e5edb033c21afdcb0e627ca2bf9d667&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470799443333202/4vZmqgf.png?ex=66f1aa1e&is=66f0589e&hm=707b7620c98e20af39086246b374febb0cba912df63d69de1bcfe4794b589d72&=&format=webp&quality=lossless&width=1440&height=480",
    "https://media.discordapp.net/attachments/1287467634534776923/1287470799850049658/1vAKYFF.png?ex=66f1aa1e&is=66f0589e&hm=7cfdc607bdd0891f7b16f7fd3421911efec8552086fb6ccddad86ef25f4ce069&=&format=webp&quality=lossless&width=1440&height=480"
]

logos = [
    "https://media.discordapp.net/attachments/1287472129864110092/1287474008249598124/1lsA8z4.png?ex=66f1ad1b&is=66f05b9b&hm=f2f0bf96c629eedd6ee0e469637d4dd85077d0605cb45d165cdb02fc7279f1fd&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474008509382808/zVbtEFN.png?ex=66f1ad1b&is=66f05b9b&hm=0467009e6265a1d26323f69036537da294cbbae9f9880880ecc6230c17e4fd6e&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474008798920815/yQzTZYD.png?ex=66f1ad1b&is=66f05b9b&hm=70cb518cbdc7305889017fac3f2fa00932cc19d6c76ea71ebfd9469f84bfb2b1&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474009042321509/Dy85dEu.png?ex=66f1ad1b&is=66f05b9b&hm=ec216c9ef9cc9fef09fc2a62632e7a072c339aa5c20c399e5126ebc778e62377&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474009272745994/p1xf4mB.jpg?ex=66f1ad1b&is=66f05b9b&hm=5fbd8021e2c4133c70e2e1751562b4e7ffae4294748ca0731ba88cd0586283fe&=&format=webp",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474009570672727/ULFUjAS.png?ex=66f1ad1b&is=66f05b9b&hm=ce278cbaca90f1dc32fe9bb1f103e21fc45a6cdc1de857fce32cc0a2c9ee9148&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474009851822101/eivPDfs.png?ex=66f1ad1c&is=66f05b9c&hm=b40e6b90114b3722c27d8e56edd70bdc6f6c37fe6269e4f0d69460579a97771e&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474010128384010/xxAddbA.png?ex=66f1ad1c&is=66f05b9c&hm=f479b425d465923e1fe6d54a12017abe26e92ab4a4439b9a873ee4b6585983ae&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474010367590410/xkVIJ38.png?ex=66f1ad1c&is=66f05b9c&hm=c775b960872bbc1da6a592af071e64766f296f9c5cb7ab72bfa234b8538216a5&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474053841686660/tEAbQ20.png?ex=66f1ad26&is=66f05ba6&hm=b4e5b83c3036e4b1358f02d019aa223968bfbe450543d037a8cf752adf90febe&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474054202265630/Q6f4Gs3.png?ex=66f1ad26&is=66f05ba6&hm=71c20a72e2104cdb133e8318c6bffd69ecd47eb8fde80bfbc58f1f429ce18527&=&format=webp&quality=lossless",
    "https://media.discordapp.net/attachments/1287472129864110092/1287474054617370716/FWcfmX0.png?ex=66f1ad26&is=66f05ba6&hm=caffbdeb86ec7012aa58dd36d2148606a141185b461aa8db7f8ec9c6a6a2ddaa&=&format=webp&quality=lossless",
]

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

_ `📸`:

_       `📸` Banniere: 8,50€ 

_ `🎇` Logo: 3,99€

_       `📸` Miniature: 7,99€

_ `🎇` Overlay Live Complet: 14,99€ (Nouveauté)

_       `📸` Affiche Annonces: 6,50€ (Nouveauté)

"""

Info = """
_ Pour les remboursements :
_  **Les commandes déjà commencées ne peuvent pas être remboursées.**
_ Une fois qu'une commande est terminée, elle **ne peut plus être modifiée.**Nous nous engageons à être fiables, 
_     mais nous vous demandons de bien vouloir lire attentivement ces informations, 
_ car nous ne répéterons pas ces détails dans les tickets de support.n**Modes de paiement acceptés :****PayPal** (en tant qu’ami proche)**Paysafecard** (pour les commandes dépassant 20 €) Note : Les paiements effectués via Paysafecard seront convertis en argent PayPal, 
_ ce qui peut entraîner une perte de valeur sur votre commande. Merci pour votre compréhension et coopération !
"""

@bot.command()
@commands.has_permissions(administrator=True)
async def services(ctx):
    embed = disnake.Embed(
        title="`🔎` Nos Services", 
        description="Choisissez une option ci-dessous `📍`", 
        color=disnake.Color.red()
    )
    
    options = [
        disnake.SelectOption(label="📕 Nos Exemples", description="Voir des exemples de nos travaux réalisés 🕊️"),
        disnake.SelectOption(label="🔎 Information", description="Obtenir des informations sur nos services 🔎"),
        disnake.SelectOption(label="🪷 Nos Services", description="Voir nos services et tarifs 🪷"),
        disnake.SelectOption(label="📍 Nos Preuves", description="Voir les preuves de nos services 📸")
    ]
    
    select = disnake.ui.Select(
        placeholder="Clique ici pour choisir 📕", 
        options=options
    )

    view = disnake.ui.View()
    view.add_item(select)

    @select.callback
    async def select_callback(interaction: disnake.MessageInteraction):
        # Ensure the interaction is valid
        if interaction.user != ctx.author:
            return await interaction.response.send_message("Ce menu n'est pas pour vous.", ephemeral=True)

        selected_option = interaction.values[0]

        if selected_option == "📕 Nos Exemples":
            await exemples_menu(interaction)
        elif selected_option == "🔎 Information":
            embed_info = disnake.Embed(
                title="`🔎` Information", 
                description=Info, 
                color=disnake.Color.red()
            )
            await interaction.response.send_message(embed=embed_info, ephemeral=True)
        elif selected_option == "🪷 Nos Services":
            await services_menu(interaction)
        elif selected_option == "📍 Nos Preuves":
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
            view.add_item(button_proof)
            await interaction.response.send_message(embed=embed_preuve, view=view, ephemeral=True)

    await ctx.send(embed=embed, view=view)

# Fonction pour le menu des exemples
async def exemples_menu(interaction: disnake.MessageInteraction):
    embed = disnake.Embed(
        title="Nos Exemples", 
        description="Choisissez une catégorie", 
        color=disnake.Color.red()
    )
    
    options = [
        disnake.SelectOption(label="🎇 Nos Bannières", description="Voir nos bannières"),
        disnake.SelectOption(label="🌸 Nos Logos", description="Voir nos logos")
    ]
    
    select = disnake.ui.Select(
        placeholder="Faites un choix", 
        options=options
    )

    view = disnake.ui.View()
    view.add_item(select)

    @select.callback
    async def exemples_callback(interaction: disnake.MessageInteraction):
        selected_option = interaction.values[0]

        if selected_option == "🎇 Nos Bannières":
            await bannieres_carrousel(interaction, 0)
        elif selected_option == "🌸 Nos Logos":
            await logos_carrousel(interaction, 0)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Carrousel pour les bannières
async def bannieres_carrousel(interaction: disnake.MessageInteraction, index: int):
    embed = disnake.Embed(
        title="Nos Bannières", 
        color=disnake.Color.red()
    )
    embed.set_image(url=banners[index])
    
    button_previous = disnake.ui.Button(
        label="Précédent", 
        style=disnake.ButtonStyle.secondary, 
        custom_id="previous_banner", 
        disabled=(index == 0)
    )
    button_next = disnake.ui.Button(
        label="Suivant", 
        style=disnake.ButtonStyle.secondary, 
        custom_id="next_banner", 
        disabled=(index == len(banners) - 1)
    )

    view = disnake.ui.View()
    view.add_item(button_previous)
    view.add_item(button_next)

    await interaction.response.edit_message(embed=embed, view=view)

    @button_previous.callback
    async def previous_callback(interaction: disnake.MessageInteraction):
        if index > 0:
            index -= 1
            await bannieres_carrousel(interaction, index)

    @button_next.callback
    async def next_callback(interaction: disnake.MessageInteraction):
        if index < len(banners) - 1:
            index += 1
            await bannieres_carrousel(interaction, index)

async def logos_carrousel(interaction: disnake.MessageInteraction, index: int):
    embed = disnake.Embed(
        title="Nos Logos", 
        color=disnake.Color.blue()
    )
    embed.set_image(url=logos[index])
    
    button_previous = disnake.ui.Button(
        label="Précédent", 
        style=disnake.ButtonStyle.secondary, 
        custom_id="previous_logo", 
        disabled=(index == 0)
    )
    button_next = disnake.ui.Button(
        label="Suivant", 
        style=disnake.ButtonStyle.secondary, 
        custom_id="next_logo", 
        disabled=(index == len(logos) - 1)
    )

    view = disnake.ui.View()
    view.add_item(button_previous)
    view.add_item(button_next)

    await interaction.response.edit_message(embed=embed, view=view)

    @button_previous.callback
    async def previous_callback(interaction: disnake.MessageInteraction):
        if index > 0:
            index -= 1
            await logos_carrousel(interaction, index)

    @button_next.callback
    async def next_callback(interaction: disnake.MessageInteraction):
        if index < len(logos) - 1:
            index += 1
            await logos_carrousel(interaction, index)

# Menu pour les services
async def services_menu(interaction: disnake.MessageInteraction):
    embed = disnake.Embed(
        title="Nos Services", 
        description="Choisissez un service", 
        color=disnake.Color.red()
    )
    
    options = [
        disnake.SelectOption(label="📸 Graphisme", description="Voir nos tarifs pour le graphisme"),
        disnake.SelectOption(label="🪷 Nitro", description="Voir nos tarifs pour les nitro")
    ]
    
    select = disnake.ui.Select(
        placeholder="Choisissez un service", 
        options=options
    )

    view = disnake.ui.View()
    view.add_item(select)

    @select.callback
    async def services_callback(interaction: disnake.MessageInteraction):
        selected_option = interaction.values[0]

        if selected_option == "📸 Graphisme":
            embed_tarif_graphisme = disnake.Embed(
                title="Tarifs Graphisme", 
                description=TarifGraph, 
                color=disnake.Color.red()
            )
            embed_tarif_graphisme.add_field(
                name='Ouvre un ticket:', 
                value='https://discord.com/channels/1251476405112537148/1270457969146069124'
            )
            await interaction.response.send_message(embed=embed_tarif_graphisme, ephemeral=True)
        elif selected_option == "🪷 Nitro":
            embed_tarif_nitro = disnake.Embed(
                title="Nos Services Nitro", 
                description=TarifNitro, 
                color=disnake.Color.red()
            )
            embed_tarif_nitro.add_field(
                name='Ouvre un ticket:', 
                value='https://discord.com/channels/1251476405112537148/1270457969146069124'
            )
            await interaction.response.send_message(embed=embed_tarif_nitro, ephemeral=True)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)




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
