import disnake
from disnake.ext import commands, tasks
import requests
import random
import asyncio
import os
import speech_recognition as sr
from datetime import datetime, timedelta
import json
import aiohttp
from flask import Flask
from threading import Thread

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

pokedex_data = {}

current_pokemon = None

def get_random_pokemon():
    pokemon_id = random.randint(1, 898) 
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_name = pokemon_data['name'].capitalize()
        pokemon_image = pokemon_data['sprites']['other']['official-artwork']['front_default']
        return pokemon_name, pokemon_image
    else:
        return None, None
    
        
@tasks.loop(seconds=25)
async def spawn_pokemon():
    global current_pokemon
    pokemon_name, pokemon_image = get_random_pokemon()
    
    if pokemon_name:
        current_pokemon = pokemon_name
        channel = disnake.utils.get(bot.get_all_channels(), name="🐧〃poké-game")
        
        if channel:
            try:
                await channel.purge(limit=100, check=lambda m: m.author == bot.user)
            except Exception as e:
                print(f"Erreur lors de la purge des messages: {e}")
            
            embed = disnake.Embed(title=f"**`Un {pokemon_name} sauvage est apparu !`**", color=disnake.Colour.dark_gray())
            embed.set_image(url=pokemon_image)
            embed.set_footer(text="Utilisez .capture pour tenter de le capturer !")
            
            await channel.send("https://media.discordapp.net/attachments/1281045310310711358/1281158205405270080/loading-6324_256.gif")
            await channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    await bot.change_presence(
        status=disnake.Status.online,
        activity=disnake.Activity(
            type=disnake.ActivityType.streaming,
            name=".help & created by Mxtsouko", 
            url='https://www.twitch.tv/mxtsouko666'
        )
    )

    spawn_pokemon.start()
    
bot.load_extension('cogs.quest')
    
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

        warning_message = "⚠️ Attention : cette conversation est retranscrite dans le serveur **La Taverne 🍻**. N'envoyez pas d'informations personnelles."
        await message.channel.send(warning_message)

        embed = disnake.Embed(
            title="Nouveau Message Privé",
            description=f"**Auteur**: {message.author.mention}\n**Contenu**: {message.content}",
            color=disnake.Color.blue()
        )
        await logs_channel.send(embed=embed)
    
    await bot.process_commands(message)


class Gif():
    
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




@bot.command()
async def capture(ctx):
    if ctx.channel.name != "🐧〃poké-game":
        em = disnake.Embed(
            title="Commande invalide",
            description="Cette commande ne peut être utilisée que dans le salon `🐧〃poké-game`.",
            color=disnake.Color.red()
        )
        msg = await ctx.send(embed=em)
        await asyncio.sleep(5)
        await msg.delete()
        return
    
    global current_pokemon
    if current_pokemon is None:
        em = disnake.Embed(
            title="<a:SalamLaMeche:1281159228337160272> Aucun Pokémon sauvage n'est présent actuellement ! <a:SalamLaMeche:1281159228337160272>",
            color=disnake.Colour.dark_gray()
        )
        await ctx.send(content=ctx.author.mention, embed=em)
        return
    
    if ctx.author.id not in pokedex_data:
        pokedex_data[ctx.author.id] = []

    pokedex_data[ctx.author.id].append(current_pokemon)
    em = disnake.Embed(
        title=f"<:pokeball:1281159305579724860> Bravo {ctx.author.name} tu viens de capturer {current_pokemon} ! <:pokeball:1281159305579724860>",
        color=disnake.Colour.dark_gray()
    )
    await ctx.send(content=ctx.author.mention, embed=em)
    
    current_pokemon = None

@bot.command()
async def pokedex(ctx):
    if ctx.channel.name != "🐧〃poké-game":
        em = disnake.Embed(
            title="Commande invalide",
            description="Cette commande ne peut être utilisée que dans le salon `🐧〃poké-game`.",
            color=disnake.Color.red()
        )
        msg = await ctx.send(embed=em)
        await asyncio.sleep(5)
        await msg.delete()
        return
    user_pokedex = pokedex_data.get(ctx.author.id, [])
    if user_pokedex:
        pokemon_list = ', '.join(user_pokedex)
        em = disnake.Embed(
            title=f"Pokédex de {ctx.author.name}",
            description=f"Tu as un total de {len(user_pokedex)} Pokémon : {pokemon_list}",
            color=disnake.Colour.blue()
        )
        await ctx.send(embed=em)
    else:
        em = disnake.Embed(
            title=f"Pokédex de {ctx.author.name}",
            description="Ton Pokédex est vide. Capture des Pokémon avec `.capture` !",
            color=disnake.Colour.red()
        )
        await ctx.send(embed=em)
        
@bot.command()
async def trade(ctx, user: disnake.Member):
    if ctx.channel.name != "🐧〃poké-trade":
        em = disnake.Embed(
            title="Commande invalide",
            description="Cette commande ne peut être utilisée que dans le salon `🐧〃poké-trade`.",
            color=disnake.Color.red()
        )
        msg = await ctx.send(embed=em)
        await asyncio.sleep(5)
        await msg.delete()
        return
    
    user_pokedex = pokedex_data.get(ctx.author.id, [])
    target_pokedex = pokedex_data.get(user.id, [])
    
    if not user_pokedex:
        em = disnake.Embed(
            title="Échange impossible",
            description=f"{ctx.author.name}, tu n'as aucun Pokémon à échanger.",
            color=disnake.Colour.red()
        )
        await ctx.send(embed=em)
        return
    
    if not target_pokedex:
        em = disnake.Embed(
            title="Échange impossible",
            description=f"{user.name} n'a aucun Pokémon à échanger.",
            color=disnake.Colour.red()
        )
        await ctx.send(embed=em)
        return
    
    embed = disnake.Embed(
        title=f"Échange de Pokémon entre {ctx.author.name} et {user.name}",
        description="Chacun doit choisir un Pokémon à échanger",
        color=disnake.Color.blue()
    )
    
    select_author = disnake.ui.Select(placeholder="Choisis ton Pokémon", options=[disnake.SelectOption(label=pokemon) for pokemon in user_pokedex])
    select_target = disnake.ui.Select(placeholder=f"{user.name}, choisis ton Pokémon", options=[disnake.SelectOption(label=pokemon) for pokemon in target_pokedex])
    
    trade_data = {"author_choice": None, "target_choice": None}
    
    async def author_callback(interaction: disnake.Interaction):
        if interaction.user != ctx.author:
            await interaction.response.send_message("Seul l'utilisateur hôte peut faire cette sélection.", ephemeral=True)
            return
        trade_data["author_choice"] = select_author.values[0]
        await interaction.response.send_message(f"Tu as choisi {trade_data['author_choice']}.")
    
    async def target_callback(interaction: disnake.Interaction):
        if interaction.user != user:
            await interaction.response.send_message("Seul l'utilisateur ciblé peut faire cette sélection.", ephemeral=True)
            return
        trade_data["target_choice"] = select_target.values[0]
        await interaction.response.send_message(f"Tu as choisi {trade_data['target_choice']}.")
    
    select_author.callback = author_callback
    select_target.callback = target_callback
    
    view = disnake.ui.View()
    view.add_item(select_author)
    view.add_item(select_target)
    
    async def finalize_trade(interaction: disnake.Interaction):
        if trade_data["author_choice"] and trade_data["target_choice"]:
            pokedex_data[ctx.author.id].remove(trade_data["author_choice"])
            pokedex_data[ctx.author.id].append(trade_data["target_choice"])
            pokedex_data[user.id].remove(trade_data["target_choice"])
            pokedex_data[user.id].append(trade_data["author_choice"])
            
            await interaction.response.send_message(
                f"Échange terminé ! {ctx.author.name} a échangé {trade_data['author_choice']} contre {trade_data['target_choice']} de {user.name}."
            )
        else:
            await interaction.response.send_message("Les deux utilisateurs doivent sélectionner un Pokémon avant de valider l'échange.", ephemeral=True)

    finalize_button = disnake.ui.Button(label="Finaliser l'échange", style=disnake.ButtonStyle.green)
    finalize_button.callback = finalize_trade
    view.add_item(finalize_button)
    
    await ctx.send(embed=embed, view=view)


@bot.command()
async def drop(ctx, user: disnake.Member):
    if ctx.channel.name != "🐧〃poké-trade":
        em = disnake.Embed(
            title="Commande invalide",
            description="Cette commande ne peut être utilisée que dans le salon `🐧〃poké-trade`.",
            color=disnake.Color.red()
        )
        msg = await ctx.send(embed=em)
        await asyncio.sleep(5)
        await msg.delete()
        return

    user_pokedex = pokedex_data.get(ctx.author.id, [])
    
    if not user_pokedex:
        em = disnake.Embed(
            title="Don impossible",
            description=f"{ctx.author.name}, tu n'as aucun Pokémon à donner.",
            color=disnake.Colour.red()
        )
        await ctx.send(embed=em)
        return
    
    embed = disnake.Embed(
        title=f"Donner un Pokémon à {user.name}",
        description="Choisis un Pokémon à donner",
        color=disnake.Color.red()
    )
    
    select_author = disnake.ui.Select(placeholder="Choisis un Pokémon", options=[disnake.SelectOption(label=pokemon) for pokemon in user_pokedex])
    
    async def author_callback(interaction: disnake.Interaction):
        if interaction.user != ctx.author:
            await interaction.response.send_message("Seul l'utilisateur hôte peut choisir.", ephemeral=True)
            return
        selected_pokemon = select_author.values[0]
        
        pokedex_data[ctx.author.id].remove(selected_pokemon)
        if user.id not in pokedex_data:
            pokedex_data[user.id] = []
        pokedex_data[user.id].append(selected_pokemon)
        
        await interaction.response.send_message(f"{ctx.author.name} a donné {selected_pokemon} à {user.name}.")
    
    select_author.callback = author_callback
    view = disnake.ui.View()
    view.add_item(select_author)
    
    await ctx.send(embed=embed, view=view)


@bot.command()
async def help(ctx):
    # Embed pour Poké Game
    embed = disnake.Embed(
        title="**Poké Game** - Aide",
        description="Voici les commandes disponibles pour jouer à **Poké Game**",
        color=disnake.Color.green()
    )
    
    embed.add_field(
        name=".capture",
        value="Utilisez cette commande pour capturer le Pokémon sauvage qui apparaît aléatoirement.",
        inline=False
    )
    
    embed.add_field(
        name=".pokedex",
        value="Affiche les Pokémon que vous avez capturés dans votre Pokédex.",
        inline=False
    )
    
    embed.add_field(
        name=".trade @utilisateur",
        value="Échange un Pokémon avec un autre utilisateur. Les deux utilisateurs doivent sélectionner un Pokémon pour l'échanger.",
        inline=False
    )
    
    embed.add_field(
        name=".drop @utilisateur",
        value="Donne un Pokémon à un autre utilisateur. Vous devez sélectionner un Pokémon à donner.",
        inline=False
    )
    
    # Embed pour Fun Commands
    embed1 = disnake.Embed(
        title="**Fun** - Commandes",
        description="Voici les commandes disponibles pour le fun du bot **Misaki**",
        color=disnake.Color.green()
    )
    
    embed1.add_field(
        name=".hug @utilisateur",
        value="Utilisez cette commande pour faire un câlin à un utilisateur.",
        inline=False
    )
    
    embed1.add_field(
        name=".kiss @utilisateur",
        value="Utilisez cette commande pour faire un bisou à un utilisateur.",
        inline=False
    )
    
    embed1.add_field(
        name=".punch @utilisateur",
        value="Utilisez cette commande pour mettre un coup de poing.",
        inline=False
    )
    
    embed1.add_field(
        name=".cookies @utilisateur",
        value="Donne un cookie à un autre utilisateur.",
        inline=False
    )
    
    embed1.add_field(
        name=".pokeball @utilisateur",
        value="Utilisez cette commande pour capturer un utilisateur.",
        inline=False
    )
    
    embed1.add_field(
        name=".teddy @utilisateur",
        value="Donne un ours en peluche à un autre utilisateur.",
        inline=False
    )
    
    embed1.add_field(
        name=".murder @utilisateur",
        value="Utilisez cette commande pour tuée un utilisateur pour une chips est un coca.",
        inline=False
    )

    embed1.add_field(
        name=".match random",
        value="Utilisez cette commande pour savoir le pourcentage d'amour que vous avez avec un membre aleatoire du serveur.",
        inline=False
    )


    await ctx.send(embed=embed)
    await ctx.send(embed=embed1)

    


PunchList = [Gif.Punch1, Gif.Punch2, Gif.Punch3, Gif.Punch4, Gif.Punch5, Gif.Punch6, Gif.Punch7, Gif.Punch8, Gif.Punch9, Gif.Punch10, Gif.Punch11, Gif.Punch12, Gif.Punch13, Gif.Punch14, Gif.Punch15]

@bot.command()
async def punch(ctx, user: disnake.Member):
    PuncfhResult = random.choice(PunchList)  
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url=PuncfhResult)
    em.set_footer(text=f'{ctx.author.name} a donné un coup de poing à {user.name}')
    await ctx.send(content=user.mention, embed=em)
    

KissList =  [Gif.Kiss1, Gif.Kiss2, Gif.Kiss3, Gif.Kiss4, Gif.Kiss5, Gif.Kiss6, Gif.Kiss7, Gif.Kiss8, Gif.Kiss9, Gif.Kiss10, Gif.Kiss11, Gif.Kiss12, Gif.Kiss13, Gif.Kiss14, Gif.Kiss15]

@bot.command()
async def kiss(ctx, user: disnake.Member):
    KissResult = random.choice(KissList)  
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url=KissResult)
    em.set_footer(text=f'{ctx.author.name} a fait un bisou à {user.name}')
    await ctx.send(content=user.mention, embed=em)
    

HugList = [Gif.Hug1, Gif.Hug2, Gif.Hug3, Gif.Hug4, Gif.Hug5, Gif.Hug6, Gif.Hug7, Gif.Hug8, Gif.Hug9, Gif.Hug10, Gif.Hug11, Gif.Hug12, Gif.Hug13, Gif.Hug14, Gif.Hug15]

@bot.command()
async def hug(ctx, user: disnake.Member):
    HugResult = random.choice(HugList)  
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url=HugResult)
    em.set_footer(text=f'{ctx.author.name} a fait un calins à {user.name}')
    await ctx.send(content=user.mention, embed=em)
    

@bot.command()
async def cookies(ctx, user: disnake.Member):
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url='https://itadakimasuanime.wordpress.com/wp-content/uploads/2013/03/checkerboard-cookies-ginga-e-kickoff.jpg')
    em.set_footer(text=f'{ctx.author.name} a donné un cookies à {user.name}')
    await ctx.send(content=user.mention, embed=em)
    
@bot.command()
async def pokeball(ctx, user: disnake.Member):
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Pokebola-pokeball-png-0.png/601px-Pokebola-pokeball-png-0.png')
    em.set_footer(text=f'{ctx.author.name} a choper {user.name} dans sa pokeball')
    await ctx.send(content=user.mention, embed=em)
    
@bot.command()
async def teddy(ctx, user: disnake.Member):
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url='https://lh4.googleusercontent.com/proxy/jezHogr9Elw7BYouFaWMZ8rFhjF9VrqaQ3_wbzvsSHEqA0s_oJ_xpSG4as4-tnp8MQScBR7DrndEGiR5XR7UByjZZNUWMOzT')
    em.set_footer(text=f'{ctx.author.name} a donné à {user.name} un ours en peluche')
    await ctx.send(content=user.mention, embed=em)
    
@bot.command()
async def murder(ctx, user: disnake.Member):
    em = disnake.Embed(
        color=disnake.Colour.dark_gray()
    )
    em.set_image(url='https://media.tenor.com/NbBCakbfZnkAAAAM/die-kill.gif')
    em.set_footer(text=f'{ctx.author.name} a tuée {user.name} pour une chips est un coca')
    await ctx.send(content=user.mention, embed=em)
    
@bot.command()
async def match(ctx, option=None, user: disnake.Member = None):
    if option == "random":
        members = [member for member in ctx.guild.members if not member.bot]
        
        if not members:
            await ctx.send("Je ne trouve aucun membre humain dans ce serveur !")
            return
        
        random_user = random.choice(members)
        while random_user == ctx.author:
            random_user = random.choice(members)

        percentage = random.randint(0, 100)

        if percentage < 40:
            message = "Tu ferais mieux de chercher une autre personne."
        elif percentage > 50:
            message = "Oh, on dirait que j'aperçois une lueur d'amour, tu devrais tenter ta chance !"
        else:
            message = "Hum, c'est difficile à dire... Peut-être que ça pourrait marcher, qui sait ?"

        embed = disnake.Embed(
            title=f"**Compatibilité Amoureuse :** {ctx.author.name} x {random_user.name}",
            description=f"Compatibilité : {percentage}%\n{message}",
            color=disnake.Colour.red()
        )
        await ctx.send(embed=embed)

    elif user:
        percentage = random.randint(0, 100)
        
        if percentage < 40:
            message = "Tu ferais mieux de chercher une autre personne."
        elif percentage > 50:
            message = "Oh, on dirait que j'aperçois une lueur d'amour, tu devrais tenter ta chance !"
        else:
            message = "Hum, c'est difficile à dire... Peut-être que ça pourrait marcher, qui sait ?"
        
        embed = disnake.Embed(
            title=f"**Compatibilité Amoureuse :** {ctx.author.name} x {user.name}",
            description=f"Compatibilité : {percentage}%\n{message}",
            color=disnake.Colour.purple()
        )
        await ctx.send(embed=embed)

    else:
        await ctx.send("Veuillez utiliser `.match @utilisateur` ou `.match random`.")
        
@bot.command()
async def joke(ctx):
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun,Spooky,Christmas?lang=fr"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data['type'] == 'single':
                    joke_text = data['joke']
                else:
                    joke_text = f"{data['setup']} - {data['delivery']}"
                embed = disnake.Embed(title="Blague du jour", description=joke_text, color=disnake.Color.dark_gray())
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(title="Erreur", description="Impossible de récupérer une blague. Réessayez plus tard.", color=disnake.Color.red())
                await ctx.send(embed=embed)
Pub = '''
_ _                               ***/LaTaverne*** ``🍻`` *!*

_ _    ✧･    ``🌸``** Animes**    ⨯˚₊‧    ``🎉`` **Giveaways**    ･⊹

_ _                ⊹･    ``🎨``** Graphisme**    ⨯˚₊‧    ``🎊`` **Nitro**    ･✧

_ _    ✧･    ``🎮``** Gaming**    ⨯˚₊‧    ``💻`` **Developement**    ･⊹

_ _                           ⊹･    ``⚙️``** Optimisation**    ･⊹

_ _``📣`` **Recrutement Ouvert & Partenariat également ouvert**

_ _                                     [``🪭`` **Rejoignez-nous **](https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66de1bfd&is=66dcca7d&hm=2101c534687cb4eab0396f632e53817f56db5fcbf0175b0304ebd375abd39c2b&=&width=1193&height=671) *!*  

_ _                              https://discord.gg/XE56h5V9rs
'''                

@bot.command()
async def np(ctx):
    em = disnake.Embed(
        title=f'Voici Notre Pub',
        description=Pub,
        color=disnake.Colour.dark_grey
    )

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
