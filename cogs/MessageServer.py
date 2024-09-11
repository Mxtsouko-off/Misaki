import disnake
from disnake.ext import commands


class MessageServer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def partner(self, ctx, channel: disnake.TextChannel):
        em_img = disnake.Embed(color=disnake.Colour.dark_gray())
        em_img.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e2107d&is=66e0befd&hm=b87f41cf5dd73f7ba8435b0b74b3829f32068f7a5998cb09f2b6e30031c7a60a&=&width=832&height=468')
        
        em = disnake.Embed(title='Conditions', color=disnake.Colour.dark_gray())
        em.add_field(name='Membres:', value='Minimum 15 (sans les bots)', inline=False)
        em.add_field(name='Partenariat:', value="Pas de serveur NSFW, boutique uniquement, toxique, ou ne respectant pas les ToS. Pas de serveurs pratiquant du ficha, dox ou autres abus.", inline=False)
        em.add_field(name="Important:", value="Si vous supprimez notre pub ou quittez le serveur, le partenariat sera annulé.", inline=False)
        em.add_field(name="Mentions:", value="Nous mentionnons uniquement <@&1280683305548906536>. Si votre serveur a moins de 20 membres, vous devez ping everyone.", inline=False)
        em.add_field(name="Vérification:", value="Votre serveur sera vérifié avant de publier votre pub. Si vous cachez un everyone, vous serez sur notre blacklist.", inline=False)
        
        if channel:
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e2818f&is=66e1300f&hm=9afa8257e50733f4c7670d94d261c8d7e61c15bc50822a35db913495821b21c2&=')
            await channel.send(embed=em_img)
            await channel.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def soutien(self, ctx, channel: disnake.TextChannel):
        em_img = disnake.Embed(color=disnake.Colour.dark_gray())
        em_img.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e2107d&is=66e0befd&hm=b87f41cf5dd73f7ba8435b0b74b3829f32068f7a5998cb09f2b6e30031c7a60a&=&width=832&height=468')
        
        em = disnake.Embed(title='Nous Soutenir `🔎`', color=disnake.Colour.dark_gray())
        em.add_field(name='/Taverne dans votre statut', value='Obtenez le rôle <@&1251588659015192607>', inline=False)
        em.add_field(name='Boostez le serveur', value='Obtenez le rôle <@&1256932646903091291> et ses avantages : https://discord.com/channels/1251476405112537148/1268927834714542183', inline=False)
        
        if channel:
            await channel.send("https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e2818f&is=66e1300f&hm=9afa8257e50733f4c7670d94d261c8d7e61c15bc50822a35db913495821b21c2&=")
            await channel.send(embed=em_img)
            await channel.send(embed=em)


def setup(bot):
    bot.add_cog(MessageServer(bot))
