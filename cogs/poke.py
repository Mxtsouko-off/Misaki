import disnake
from disnake.ext import commands, tasks
import aiohttp
import random
import asyncio


class Poke(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pokedex_data = {}
        self.current_pokemon = None
        self.spawn_pokemon.start()  # Démarrer la boucle pour faire apparaître les Pokémon

    # Appel asynchrone à l'API pour obtenir un Pokémon aléatoire
    async def get_random_pokemon(self):
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

    # Tâche récurrente pour faire apparaître un Pokémon toutes les 20 secondes
    @tasks.loop(seconds=20)
    async def spawn_pokemon(self):
        pokemon_name, pokemon_image = await self.get_random_pokemon()
        if pokemon_name:
            self.current_pokemon = pokemon_name
            channel = disnake.utils.get(self.bot.get_all_channels(), name="🐧〃poké-game")
            if channel:
                try:
                    await channel.purge(limit=100, check=lambda m: m.author == self.bot.user)
                except Exception as e:
                    print(f"Erreur lors de la purge des messages: {e}")
                
                embed = disnake.Embed(title=f"**`Un {pokemon_name} sauvage est apparu !`**", color=disnake.Colour.dark_gray())
                embed.set_image(url=pokemon_image)
                embed.set_footer(text="Utilisez .capture pour tenter de le capturer !")
                
                await channel.send(embed=embed)

    # Commande pour capturer le Pokémon
    @commands.command()
    async def capture(self, ctx):
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
        
        if self.current_pokemon is None:
            em = disnake.Embed(
                title="Aucun Pokémon sauvage n'est présent actuellement !",
                color=disnake.Colour.dark_gray()
            )
            await ctx.send(content=ctx.author.mention, embed=em)
            return
        
        if ctx.author.id not in self.pokedex_data:
            self.pokedex_data[ctx.author.id] = []

        self.pokedex_data[ctx.author.id].append(self.current_pokemon)
        em = disnake.Embed(
            title=f"Bravo {ctx.author.name}, tu viens de capturer {self.current_pokemon} !",
            color=disnake.Colour.dark_gray()
        )
        await ctx.send(content=ctx.author.mention, embed=em)
        
        self.current_pokemon = None

    # Commande pour consulter son Pokédex
    @commands.command()
    async def pokedex(self, ctx):
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

        user_pokedex = self.pokedex_data.get(ctx.author.id, [])
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

    # Commande pour échanger des Pokémon avec un autre utilisateur
    @commands.command()
    async def trade(self, ctx, user: disnake.Member):
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
        
        user_pokedex = self.pokedex_data.get(ctx.author.id, [])
        target_pokedex = self.pokedex_data.get(user.id, [])
        
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
        
        # Sélections pour choisir le Pokémon
        select_author = disnake.ui.Select(placeholder="Choisis ton Pokémon", options=[disnake.SelectOption(label=pokemon) for pokemon in user_pokedex])
        select_target = disnake.ui.Select(placeholder=f"{user.name}, choisis ton Pokémon", options=[disnake.SelectOption(label=pokemon) for pokemon in target_pokedex])
        
        trade_data = {"author_choice": None, "target_choice": None}
        
        # Callbacks pour la sélection des Pokémon
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
        
        # Bouton pour finaliser l'échange
        async def finalize_trade(interaction: disnake.Interaction):
            if trade_data["author_choice"] and trade_data["target_choice"]:
                self.pokedex_data[ctx.author.id].remove(trade_data["author_choice"])
                self.pokedex_data[ctx.author.id].append(trade_data["target_choice"])
                self.pokedex_data[user.id].remove(trade_data["target_choice"])
                self.pokedex_data[user.id].append(trade_data["author_choice"])
                
                await interaction.response.send_message(
                    f"Échange terminé ! {ctx.author.name} a échangé {trade_data['author_choice']} contre {trade_data['target_choice']} de {user.name}."
                )
            else:
                await interaction.response.send_message("Les deux utilisateurs doivent sélectionner un Pokémon avant de valider l'échange.", ephemeral=True)

        finalize_button = disnake.ui.Button(label="Finaliser l'échange", style=disnake.ButtonStyle.green)
        finalize_button.callback = finalize_trade
        view.add_item(finalize_button)
        
        await ctx.send(embed=embed, view=view)

    # Commande pour donner un Pokémon à un autre utilisateur
    @commands.command()
    async def drop(self, ctx, user: disnake.Member):
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

        user_pokedex = self.pokedex_data.get(ctx.author.id, [])
        
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
            self.pokedex_data[ctx.author.id].remove(pokemon_to_give)
            if user.id not in self.pokedex_data:
                self.pokedex_data[user.id] = []
            self.pokedex_data[user.id].append(pokemon_to_give)
            await interaction.response.send_message(f"{ctx.author.name} a donné {pokemon_to_give} à {user.name}.")

        select.callback = select_callback
        
        view = disnake.ui.View()
        view.add_item(select)
        
        await ctx.send(f"{ctx.author.name}, choisis un Pokémon à donner à {user.name} :", view=view)


def setup(bot):
    bot.add_cog(Poke(bot))
