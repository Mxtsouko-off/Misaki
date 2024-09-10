import disnake
from disnake.ext import commands
import aiohttp
import base64
import io
import json

class Fivem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fivemlookup', help="Recherche un serveur FiveM par son tag")
    async def fivemlookup(self, ctx, tag: str):
            urlfivem = f"https://servers-frontend.fivem.net/api/servers/single/{tag}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.3",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(urlfivem, headers=headers) as res:
                    if res.status == 404:
                        await ctx.send("Le tag fourni est invalide.")
                    else:
                        data = await res.json()


                        json_data = json.dumps(data, indent=4) 
                        json_file = io.BytesIO(json_data.encode('utf-8'))   

                        dm_channel = await ctx.author.create_dm()
                        await dm_channel.send("Voici les informations du serveur FiveM que vous avez demandées.", file=disnake.File(fp=json_file, filename=f"fivem_data_{tag}.json"))
                        
                        await ctx.send(f"Les informations sur le serveur {tag} ont été envoyées en message privé.")

    @commands.command(name='cip', help="Obtenir l'IP et le port d'un serveur FiveM")
    async def cip(self, ctx, tag: str):
        urlfivem = f"https://servers-frontend.fivem.net/api/servers/single/{tag}"

        async with aiohttp.ClientSession() as session:
            async with session.get(urlfivem) as res:
                if res.status == 404:
                    embed = disnake.Embed(
                        title="Invalid Code",
                        color=0xc73e10,
                    )
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    data = await res.json()
                    connect_endpoint = data["Data"]["connectEndPoints"][0]

                    embed = disnake.Embed(
                        color=0xc73e10,
                    )
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    embed.add_field(name="IP:Port", value=f"`{connect_endpoint}`")
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fivem(bot))
