import disnake
from disnake.ext import commands, tasks
import random
import requests

class AnimeVote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.questions = []
        self.anime_list = []
        self.global_anime_name = None
        self.global_anime_link = None
        self.load_animes()

    def load_animes(self):
        try:
            response = requests.get('https://raw.githubusercontent.com/Mxtsouko-off/Misaki/main/Json/anime.json')
            if response.status_code == 200:
                data = response.json()
                self.anime_list = data
                print(f"{len(self.anime_list)} animes chargés.")
                print("Animes are loaded.")
                self.anime_vote_task.start()
            else:
                print(f"Erreur lors du chargement des animes: {response.status_code}")
        except Exception as e:
            print(f"Une erreur s'est produite lors du chargement des animes: {e}")

    def get_anime_image(self, anime_name):
        url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
        response = requests.get(url)
        data = response.json()
        if data['data']:
            return data['data'][0]['images']['jpg']['large_image_url']
        return None

    @tasks.loop(hours=4)
    async def anime_vote_task(self):
        guild = disnake.utils.get(self.bot.guilds, name="La Taverne 🍻")
        channel = disnake.utils.get(guild.text_channels, name="💐〃anime-vote")
        if channel is None:
            print("Canal non trouvé.")
            return

        if hasattr(self.anime_vote_task, "accept_count") and hasattr(self.anime_vote_task, "pass_count"):
            total_count = self.anime_vote_task.accept_count + self.anime_vote_task.pass_count
            if total_count > 0:
                accept_percentage = (self.anime_vote_task.accept_count / total_count) * 100
                pass_percentage = (self.anime_vote_task.pass_count / total_count) * 100
                results_embed = disnake.Embed(
                    title="Résultats du vote anime",
                    description=f"**Accepté**: {accept_percentage:.2f}%\n**Passé**: {pass_percentage:.2f}%",
                    color=0x00ff00
                )
                await channel.send(embed=results_embed)

        self.anime_vote_task.accept_count = 0
        self.anime_vote_task.pass_count = 0

        if not self.anime_list:
            print("La liste des animes est vide.")
            return

        anime = random.choice(self.anime_list)
        self.global_anime_name = anime["name"]
        self.global_anime_link = anime["link"]
        image_url = self.get_anime_image(self.global_anime_name)

        role = disnake.utils.get(channel.guild.roles, name='🚀〢Ping Anime vote')
        if image_url:
            embed = disnake.Embed(
                title="Vote pour l'anime",
                description=f"Proposition d'anime : {self.global_anime_name}\n{self.global_anime_link}"
            )
            embed.set_image(url=image_url)
            
            view = disnake.ui.View()
            view.add_item(disnake.ui.Button(label="Accepter", style=disnake.ButtonStyle.success, custom_id="accept"))
            view.add_item(disnake.ui.Button(label="Passer", style=disnake.ButtonStyle.danger, custom_id="pass"))

            await channel.send(content=role.mention, embed=embed, view=view)
        else:
            await channel.send(content=f"Je n'ai pas pu trouver une image pour l'anime '{self.global_anime_name}'.")

    @anime_vote_task.before_loop
    async def before_anime_vote_task(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.Interaction):
        if interaction.type == disnake.InteractionType.component:
            custom_id = interaction.data.get("custom_id")
            if custom_id == "accept":
                self.anime_vote_task.accept_count += 1
                await interaction.response.send_message(f"Vous avez accepté l'anime '{self.global_anime_name}'. Vous pouvez le voir ici : {self.global_anime_link}", ephemeral=True)
            elif custom_id == "pass":
                self.anime_vote_task.pass_count += 1
                await interaction.response.send_message(f"Vous avez passé l'anime '{self.global_anime_name}'.", ephemeral=True)

def setup(bot):
    bot.add_cog(AnimeVote(bot))
