import disnake
from disnake.ext import commands
import asyncio

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def banner(self, ctx, channel: disnake.TextChannel, link: str):
        utilisateur_autorise = 723256412674719795  

        if ctx.author.id != utilisateur_autorise:
            message = await ctx.send("Seule Mxtsouko peut utiliser cette commande.")
            await asyncio.sleep(3)
            await message.delete()
            return
        
        if channel:
            role = disnake.utils.get(channel.guild.roles, name='📣〢Notification Boutique')
            em = disnake.Embed(
                title='Nouvelle bannière ajoutée', 
                description='Nos bannières sont entièrement faites à la main. Aucun site ou autre, elles sont toutes réalisées par notre graphiste.'
            )
            em.set_image(url=f'{link}')
            em.set_footer(text=f'Cette bannière a été postée par {ctx.author.name}')
            await channel.send(content=role.mention, embed=em)

    @commands.command()
    async def logo(self, ctx, channel: disnake.TextChannel, link: str):
        utilisateur_autorise = 723256412674719795

        if ctx.author.id != utilisateur_autorise:
            message = await ctx.send("Seule Mxtsouko peut utiliser cette commande.")
            await asyncio.sleep(3)
            await message.delete()
            return

        if channel:
            role = disnake.utils.get(channel.guild.roles, name='📣〢Notification Boutique')
            em = disnake.Embed(
                title='Nouveau logo ajouté', 
                description='Nos logos sont entièrement faits à la main. Aucun site ou autre, ils sont tous réalisés par notre graphiste.'
            )
            em.set_image(url=f'{link}')
            em.set_footer(text=f'Ce logo a été posté par {ctx.author.name}')
            await channel.send(content=role.mention, embed=em)

    @commands.command()
    async def minia(self, ctx, channel: disnake.TextChannel, link: str):
        utilisateur_autorise = 723256412674719795

        if ctx.author.id != utilisateur_autorise:
            message = await ctx.send("Seule Mxtsouko peut utiliser cette commande.")
            await asyncio.sleep(3)
            await message.delete()
            return

        if channel:
            role = disnake.utils.get(channel.guild.roles, name='📣〢Notification Boutique')
            em = disnake.Embed(
                title='Nouvelle miniature ajoutée', 
                description='Nos miniatures sont entièrement faites à la main. Aucun site ou autre, elles sont toutes réalisées par notre graphiste.'
            )
            em.set_image(url=f'{link}')
            em.set_footer(text=f'Cette miniature a été postée par {ctx.author.name}')
            await channel.send(content=role.mention, embed=em)

def setup(bot):
    bot.add_cog(Owner(bot))
