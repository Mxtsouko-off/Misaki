import disnake
from disnake.ext import commands, tasks
import requests
import random
import asyncio
import os
from datetime import datetime, timedelta
import json
import aiohttp
from flask import Flask
from threading import Thread

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)


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
bot.load_extension('cogs.poke')
bot.load_extension('cogs.Utility')
bot.load_extension('cogs.quest')
bot.load_extension('cogs.anime_vote')
    
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
