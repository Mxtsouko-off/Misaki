import disnake
from disnake.ext import commands
import random
import aiohttp


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
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
        
    @commands.command()
    async def joke(self, ctx):
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
                    
    @commands.command()
    async def rps(self, ctx, choice: str):
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

    @commands.command()
    async def cat(self, ctx):
        embed = disnake.Embed(title="Chat Mignon", description="Voici un chat mignon ! 🐱", color=disnake.Color.dark_gray())
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        embed = disnake.Embed(title="Chien Mignon", description="Voici un chien mignon ! 🐶", color=disnake.Color.dark_gray())
        await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx):
        result = "Pile" if random.choice([True, False]) else "Face"
        embed = disnake.Embed(title="Lancer de pièce", description=f"Le résultat du lancer est : **{result}**", color=disnake.Color.dark_gray())
        await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, max_value: int):
        roll = random.randint(1, max_value)
        embed = disnake.Embed(title="Lancer de dé", description=f"Tu as lancé un dé et obtenu : **{roll}**", color=disnake.Color.dark_gray())
        await ctx.send(embed=embed)
        
        
    @commands.command()
    async def murder(self, ctx, user: disnake.Member):
        em = disnake.Embed(
            color=disnake.Colour.dark_gray()
        )
        em.set_image(url='https://media.tenor.com/NbBCakbfZnkAAAAM/die-kill.gif')
        em.set_footer(text=f'{ctx.author.name} a tué {user.name} pour une chips et un coca')
        await ctx.send(content=user.mention, embed=em)
        
    @commands.command()
    async def teddy(self, ctx, user: disnake.Member):
        em = disnake.Embed(
            color=disnake.Colour.dark_gray()
        )
        em.set_image(url='https://lh4.googleusercontent.com/proxy/jezHogr9Elw7BYouFaWMZ8rFhjF9VrqaQ3_wbzvsSHEqA0s_oJ_xpSG4as4-tnp8MQScBR7DrndEGiR5XR7UByjZZNUWMOzT')
        em.set_footer(text=f'{ctx.author.name} a donné à {user.name} un ours en peluche')
        await ctx.send(content=user.mention, embed=em)

    PunchList = [Gif.Punch1, Gif.Punch2, Gif.Punch3, Gif.Punch4, Gif.Punch5, Gif.Punch6, Gif.Punch7, Gif.Punch8, Gif.Punch9, Gif.Punch10, Gif.Punch11, Gif.Punch12, Gif.Punch13, Gif.Punch14, Gif.Punch15]

    @commands.command()
    async def punch(self, ctx, user: disnake.Member):
        PunchResult = random.choice(self.PunchList)  
        em = disnake.Embed(
            color=disnake.Colour.dark_gray()
        )
        em.set_image(url=PunchResult)
        em.set_footer(text=f'{ctx.author.name} a donné un coup de poing à {user.name}')
        await ctx.send(content=user.mention, embed=em)
        

    KissList =  [Gif.Kiss1, Gif.Kiss2, Gif.Kiss3, Gif.Kiss4, Gif.Kiss5, Gif.Kiss6, Gif.Kiss7, Gif.Kiss8, Gif.Kiss9, Gif.Kiss10, Gif.Kiss11, Gif.Kiss12, Gif.Kiss13, Gif.Kiss14, Gif.Kiss15]

    @commands.command()
    async def kiss(self, ctx, user: disnake.Member):
        KissResult = random.choice(self.KissList)  
        em = disnake.Embed(
            color=disnake.Colour.dark_gray()
        )
        em.set_image(url=KissResult)
        em.set_footer(text=f'{ctx.author.name} a fait un bisou à {user.name}')
        await ctx.send(content=user.mention, embed=em)
        

    HugList = [Gif.Hug1, Gif.Hug2, Gif.Hug3, Gif.Hug4, Gif.Hug5, Gif.Hug6, Gif.Hug7, Gif.Hug8, Gif.Hug9, Gif.Hug10, Gif.Hug11, Gif.Hug12, Gif.Hug13, Gif.Hug14, Gif.Hug15]
    
    @commands.command()
    async def hug(self, ctx, user: disnake.Member):
        HugResult = random.choice(self.HugList)  
        em = disnake.Embed(
            color=disnake.Colour.dark_gray()
        )
        em.set_image(url=HugResult)
        em.set_footer(text=f'{ctx.author.name} a fait un câlin à {user.name}')
        await ctx.send(content=user.mention, embed=em)

def setup(bot):
    bot.add_cog(Utility(bot))
