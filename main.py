import disnake
from disnake.ext import commands, tasks
import asyncio
import os
from flask import Flask
from threading import Thread
import re
import random
import requests
import aiohttp

pokedex_data = {}
current_pokemon = None

anime_list = []
global_anime_name = None
global_anime_link = None
accept_count = 0
pass_count = 0

staff_status_message = None
channel_id = 1283104286271864913
role_name = "📂〢Staff" 

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
    
    send_random_question.start()
    spawn_pokemon.start
    update_staff_status.start()
    remind_bumping.start()
    load_animes()  
    if not anime_vote_task.is_running():  
        anime_vote_task.start()  
    await load_cogs()


async def load_cogs():
    cogs = [
        'cogs.Utility'
    ]

    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f"Successfully loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")
        await asyncio.sleep(1) 
        
@tasks.loop(hours=2)
async def remind_bumping():
    for guild in bot.guilds:
        channel = disnake.utils.get(guild.text_channels, name='🌊〃bump')
        role = disnake.utils.get(guild.roles, name='🌊〢Ping Bumping')
        if channel is not None and role is not None:
            embed = disnake.Embed(
                title="Rappel de Bump",
                description="Il est temps de bump le serveur !",
                color=0xFF5733
            )
            await channel.send(content=role.mention, embed=embed)
            
@tasks.loop(minutes=3)
async def update_staff_status():
        channel = bot.get_channel(channel_id)
        if channel is None:
            return

        guild = channel.guild
        role = disnake.utils.get(guild.roles, name=role_name)
        if role is None:
            return

        online_members = []
        idle_members = []
        dnd_members = []
        offline_members = []

        for member in guild.members:
            if role in member.roles:
                if member.status == disnake.Status.online:
                    online_members.append(member.mention)
                elif member.status == disnake.Status.idle:
                    idle_members.append(member.mention)
                elif member.status == disnake.Status.dnd:
                    dnd_members.append(member.mention)
                else:
                    offline_members.append(member.mention)

        embed = disnake.Embed(
            title="Statut du Staff",
            color=0x00ff00,
            description="Voici les statuts actuels des membres du staff."
        )
        embed.add_field(name="`🟢` **En ligne**", value='\n'.join(online_members) or "Aucun", inline=False)
        embed.add_field(name="`🌙` **Inactif**", value='\n'.join(idle_members) or "Aucun", inline=False)
        embed.add_field(name="`⛔` **Ne pas déranger**", value='\n'.join(dnd_members) or "Aucun", inline=False)
        embed.add_field(name="`⚫` **Hors ligne**", value='\n'.join(offline_members) or "Aucun", inline=False)

        if staff_status_message is None:
            staff_status_message = await channel.send(embed=embed)
        else:
            await staff_status_message.edit(embed=embed)

@update_staff_status.before_loop
async def before_update_staff_status(self):
        await bot.wait_until_ready()

def load_animes():
    global anime_list
    try:
        response = requests.get('https://raw.githubusercontent.com/Mxtsouko-off/Misaki/main/Json/anime.json')
        if response.status_code == 200:
            anime_list = response.json()
            print(f"{len(anime_list)} animes chargés.")
            anime_vote_task.start()
        else:
            print(f"Erreur lors du chargement des animes: {response.status_code}")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement des animes: {e}")


def get_anime_image(anime_name):
    url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
    response = requests.get(url)
    data = response.json()
    if data['data']:
        return data['data'][0]['images']['jpg']['large_image_url']
    return None

@tasks.loop(hours=4)
async def anime_vote_task():
    global global_anime_name, global_anime_link, accept_count, pass_count

    guild = disnake.utils.get(bot.guilds, name="La Taverne 🍻")
    channel = disnake.utils.get(guild.text_channels, name="💐〃anime-vote")
    if channel is None:
        print("Canal non trouvé.")
        return

    total_count = accept_count + pass_count
    if total_count > 0:
        accept_percentage = (accept_count / total_count) * 100
        pass_percentage = (pass_count / total_count) * 100
        results_embed = disnake.Embed(
            title="Résultats du vote anime",
            description=f"**Accepté**: {accept_percentage:.2f}%\n**Passé**: {pass_percentage:.2f}%",
            color=0x00ff00
        )
        await channel.send(embed=results_embed)
        
    accept_count = 0
    pass_count = 0
    
    if not anime_list:
        print("La liste des animes est vide.")
        return
    
    anime = random.choice(anime_list)
    global_anime_name = anime["name"]
    global_anime_link = anime["link"]
    image_url = get_anime_image(global_anime_name)

    role = disnake.utils.get(channel.guild.roles, name='🚀〢Ping Anime vote')
    if image_url:
        embed = disnake.Embed(
            title="Vote pour l'anime",
            description=f"Proposition d'anime : {global_anime_name}\n{global_anime_link}"
        )
        embed.set_image(url=image_url)
        
        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label="Accepter", style=disnake.ButtonStyle.success, custom_id="accept"))
        view.add_item(disnake.ui.Button(label="Passer", style=disnake.ButtonStyle.danger, custom_id="pass"))

        await channel.send(content=role.mention, embed=embed, view=view)
    else:
        await channel.send(content=f"Je n'ai pas pu trouver une image pour l'anime '{global_anime_name}'.")

@anime_vote_task.before_loop
async def before_anime_vote_task():
    await bot.wait_until_ready()

@bot.event
async def on_interaction(interaction: disnake.Interaction):
    global accept_count, pass_count, global_anime_name, global_anime_link

    if interaction.type == disnake.InteractionType.component:
        custom_id = interaction.data.get("custom_id")
        if custom_id == "accept":
            accept_count += 1
            await interaction.response.send_message(f"Vous avez accepté l'anime '{global_anime_name}'. Vous pouvez le voir ici : {global_anime_link}", ephemeral=True)
        elif custom_id == "pass":
            pass_count += 1
            await interaction.response.send_message(f"Vous avez passé l'anime '{global_anime_name}'.", ephemeral=True)



                
def load_questions():
    global questions
    try:
        response = requests.get('https://raw.githubusercontent.com/Mxtsouko-off/Misaki/main/Json/question.json')
        if response.status_code == 200:
            data = response.json()
            questions = [item['question'] for item in data]
            print(f"{len(questions)} questions chargées.")  
            print("Questions are loaded.")  
        else:
            print(f"Erreur lors du chargement des questions: {response.status_code}")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement des questions: {e}")
        
load_questions()

@tasks.loop(minutes=3)
async def check_status():
    for guild in bot.guilds:
        role = disnake.utils.get(guild.roles, name='🦾〢Soutient Bio')
        if role is None:
            print(f"Rôle '🦾〢Soutient Bio' non trouvé dans {guild.name}.")
            continue

        for member in guild.members:
            if member.bot:
                    continue   
            if member.status == disnake.Status.offline:
                    continue   

            has_custom_status = any(
                    activity.type == disnake.ActivityType.custom and activity.state and '/Taverne' in activity.state
                    for activity in member.activities
                )

            if has_custom_status:
                if role not in member.roles:
                    await member.add_roles(role)
                    print(f'Rôle ajouté à {member.display_name} dans {guild.name}')
            else:
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f'Rôle retiré de {member.display_name} dans {guild.name}')

async def get_random_pokemon():
    pokemon_id = random.randint(1, 898)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}") as response:
            if response.status == 200:
                pokemon_data = await response.json()
                pokemon_name = pokemon_data['name'].capitalize()
                pokemon_image = pokemon_data['sprites']['other']['official-artwork']['front_default']
                return pokemon_name, pokemon_image
            else:
                return None, None
            
@tasks.loop(seconds=20)
async def spawn_pokemon():
    global current_pokemon
    pokemon_name, pokemon_image = await get_random_pokemon()
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
            
            await channel.send(embed=embed)
            
@bot.command()
async def capture(ctx):
    global current_pokemon
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
    
    if current_pokemon is None:
        em = disnake.Embed(
            title="Aucun Pokémon sauvage n'est présent actuellement !",
            color=disnake.Colour.dark_gray()
        )
        await ctx.send(content=ctx.author.mention, embed=em)
        return
    
    if ctx.author.id not in pokedex_data:
        pokedex_data[ctx.author.id] = []

    pokedex_data[ctx.author.id].append(current_pokemon)
    em = disnake.Embed(
        title=f"Bravo {ctx.author.name}, tu viens de capturer {current_pokemon} !",
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
                description="Tu n'as aucun Pokémon à donner.",
                color=disnake.Colour.red()
            )
            await ctx.send(embed=em)
            return
        
        select = disnake.ui.Select(placeholder="Choisis le Pokémon à donner", options=[disnake.SelectOption(label=pokemon) for pokemon in user_pokedex])
        
        async def select_callback(interaction: disnake.Interaction):
            pokemon_to_give = select.values[0]
            pokedex_data[ctx.author.id].remove(pokemon_to_give)
            if user.id not in pokedex_data:
                pokedex_data[user.id] = []
            pokedex_data[user.id].append(pokemon_to_give)
            await interaction.response.send_message(f"{ctx.author.name} a donné {pokemon_to_give} à {user.name}.")

        select.callback = select_callback
        
        view = disnake.ui.View()
        view.add_item(select)
        
        await ctx.send(f"{ctx.author.name}, choisis un Pokémon à donner à {user.name} :", view=view)


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

@remind_bumping.before_loop
@check_status.before_loop
async def before_tasks(self):
    await bot.wait_until_ready()   
    
@tasks.loop(hours=5)
async def send_random_question():
    guild = disnake.utils.get(bot.guilds, name="La Taverne 🍻")
    channel = disnake.utils.get(guild.text_channels, name="❔〃question-du-jour")
    role = disnake.utils.get(channel.guild.roles, name="❔〢Ping Question !")

    if channel is not None and role is not None:
        try:
            await channel.purge(limit=100) 
        except Exception as e:
            print(f"Erreur lors de la purge des messages: {e}")

        if questions:  
            question = random.choice(questions)
            embed = disnake.Embed(
                title="Question du jour",
                description=question,
                color=0x00ff00
            )
            embed.add_field(name='Hésitez pas à répondre dans :', value='https://discord.com/channels/1251476405112537148/1269373203650973726')
            await channel.send(content=role.mention, embed=embed)
      
        
@bot.command()
async def help(ctx):
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
    
    embed1.add_field(
        name=".joke",
        value="Utilisez cette commande pour faire apparaitre une blague.",
        inline=False
    )
    
    embed1.add_field(
        name=".rps pierre ou ciseaux ou papier",
        value="Utilisez cette commande pour faire pierre papier ciseaux avec misaki.",
        inline=False
    )

    embed1.add_field(
        name=".cat",
        value="Utilisez cette commande pour faire apparaitre un chat mignon.",
        inline=False
    )
    
    embed1.add_field(
        name=".dog",
        value="Utilisez cette commande pour faire apparaitre un chien mignon.",
        inline=False
    )
    
    embed1.add_field(
        name=".coinflip pile ou face",
        value="Utilisez cette commande pour faire un pile ou face avec misaki.",
        inline=False
    )
    
    embed1.add_field(
        name=".roll nombre",
        value="Utilisez cette commande pour faire un lancer de dé.",
        inline=False
    )

    embed2 = disnake.Embed(
        title="**Modération** - Commandes",
        description="Voici les commandes disponibles pour La Modération de **La Taverne**",
        color=disnake.Color.green()
    )
    
    embed2.add_field(
        name=".supension @utilisateur 1 d",
        value="Utilisez cette commande pour suspendre un membre du staff.",
        inline=False
    )
    embed2.add_field(
        name=".réunion date heure",
        value="Utilisez cette commande pour organisé une réunion staff staff.",
        inline=False
    )
    embed2.add_field(
        name=".ban @utilisateur raison",
        value="Utilisez cette commande pour bannir un membre.",
        inline=False
    )
    embed2.add_field(
        name=".tempban @utilisateur time unit raison",
        value="Utilisez cette commande pour bannir un membre temporaorement.",
        inline=False
    )
    embed2.add_field(
        name=".rm_staff @utilisateur pleinte",
        value="Utilisez cette commande pour faire une remarque sur un membre du staff.",
        inline=False
    )
    embed2.add_field(
        name="/promouvoir @utilisateur ",
        value="Utilisez cette commande pour promouvoir un membre .",
        inline=False
    )
    embed3 = disnake.Embed(
        title="**Owner (Mxtsouko)** - Commandes",
        description="Voici les commandes disponibles pour La Modération de **La Taverne**",
        color=disnake.Color.green()
    )
    
    embed3.add_field(
        name=".banner channel link",
        value="Utilisez cette commande pour rajouter une banniere dans nos banniere.",
        inline=False
    )
    embed3.add_field(
        name=".logo channel link",
        value="Utilisez cette commande pour rajouter un logo dans nos logo.",
        inline=False
    )
    embed3.add_field(
        name=".minia channel link",
        value="Utilisez cette commande pour rajouter une miniature dans nos miniature.",
        inline=False
    )
    asyncio.sleep(2)
    await ctx.send(embed=embed)
    asyncio.sleep(3)
    await ctx.send(embed=embed1)
    asyncio.sleep(4)
    await ctx.send(embed=embed2)
    asyncio.sleep(5)
    await ctx.send(embed=embed3)


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
        
        member = message.guild.get_member(message.author.id)

        if member:
            admin_roles = [role.id for role in message.guild.roles if "admin" in role.name.lower()]
            partnership_role_id = 1280429826414477373  
            staff_id = 1268728239010873395  
            if any(role.id in admin_roles for role in member.roles) or member.guild_permissions.administrator:
                await bot.process_commands(message)
                return
            
            if any(role.id == partnership_role_id for role in member.roles):
                await bot.process_commands(message)
                return

        if re.search(r'discord\.gg|discord\.com|discord\.me|discord\.app|discord\.io', message.content, re.IGNORECASE):
            await message.delete()
            warning_message = await message.channel.send(f"{message.author.mention}, les liens Discord ne sont pas autorisés dans ce serveur.")
            await asyncio.sleep(5)
            await warning_message.delete()
            return

    await bot.process_commands(message)

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
