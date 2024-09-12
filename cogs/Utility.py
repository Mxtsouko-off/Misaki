import disnake
from disnake.ext import commands
import random
import aiohttp
import asyncio
from datetime import timedelta

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
            await asyncio.sleep(3)
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e2818f&is=66e1300f&hm=9afa8257e50733f4c7670d94d261c8d7e61c15bc50822a35db913495821b21c2&=')
            await asyncio.sleep(3)
            await channel.send(embed=em_img)
            await asyncio.sleep(3)
            await channel.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reglement(self, ctx, channel: disnake.TextChannel):
        em_img = disnake.Embed(color=disnake.Colour.dark_gray())
        em_img.set_image(url='https://media.discordapp.net/attachments/1280352059031425035/1282095507841351692/1af689d42bdb7686df444f22925f9e89.gif?ex=66e2107d&is=66e0befd&hm=b87f41cf5dd73f7ba8435b0b74b3829f32068f7a5998cb09f2b6e30031c7a60a&=&width=832&height=468')
        
        em = disnake.Embed(title='Reglement', color=disnake.Colour.dark_gray())
        em.add_field(name='Tos', value='Nous vous demandons de respecter les tos discord', inline=False)
        em.add_field(name='Interdiction:', value="1. D'insulter, d'imposer vos religion au autre chacun est libre, manque de respect au staff, toute sorte de discrimination est interdites", inline=False)
        em.add_field(name="Acte Méritent un Bannisement:", value="Dox, phishing ou toute forme de hack", inline=False)

        if channel:
            await asyncio.sleep(3)
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e2818f&is=66e1300f&hm=9afa8257e50733f4c7670d94d261c8d7e61c15bc50822a35db913495821b21c2&=')
            await asyncio.sleep(3)
            await channel.send(embed=em_img)
            await asyncio.sleep(3)
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
            await asyncio.sleep(3)
            await channel.send('https://media.discordapp.net/attachments/1038084584149102653/1283304082286579784/2478276E-41CA-4738-B961-66A84B918163-1-1-1-1-1.gif?ex=66e2818f&is=66e1300f&hm=9afa8257e50733f4c7670d94d261c8d7e61c15bc50822a35db913495821b21c2&=')
            await asyncio.sleep(3)
            await channel.send(embed=em_img)
            await asyncio.sleep(3)
            await channel.send(embed=em)

    @commands.command(name='suspension', description='Permet de suspendre un membre du staff')
    @commands.has_role('📖〢Gestion Serveur')
    async def suspension(self, ctx, membre: disnake.Member, temps: str):
        time_mapping = {
            "s": 1,    # Secondes
            "m": 60,   # Minutes
            "h": 3600, # Heures
            "d": 86400 # Jours
        }

        if temps[-1] in time_mapping:
            try:
                duration = int(temps[:-1]) * time_mapping[temps[-1]]
            except ValueError:
                await ctx.response.send_message("Format de temps invalide.", ephemeral=True)
                return
        else:
            await ctx.response.send_message("Format de temps invalide. Utilisez 's', 'm', 'h', ou 'd'.", ephemeral=True)
            return

        suspension_role = disnake.utils.get(ctx.guild.roles, name='📉〢Suspension staff')
        if not suspension_role:
            await ctx.response.send_message("Rôle de suspension non trouvé.", ephemeral=True)
            return
        
        previous_staff_roles = [role for role in membre.roles if role.name in ['📂〢Staff', '📂〢Haut staff']]

        await membre.add_roles(suspension_role)
        for role in previous_staff_roles:
            await membre.remove_roles(role)

        try:
            await membre.send(f"Vous avez été suspendu pour {temps}. Vos rôles de staff ont été temporairement retirés.")
        except disnake.Forbidden:
            await ctx.response.send_message("Impossible d'envoyer un message privé à ce membre.", ephemeral=True)

        await asyncio.sleep(duration)

        if suspension_role in membre.roles:
            await membre.remove_roles(suspension_role)
        
        if previous_staff_roles:
            await membre.add_roles(*previous_staff_roles)

        await ctx.response.send_message(f"La suspension de {membre.mention} est terminée.", ephemeral=True)

    # Commande pour organiser une réunion
    @commands.command(name='réunion', description='Organiser une réunion staff')
    @commands.has_any_role('📖〢Gestion Serveur', '📂〢Haut staff')
    async def réunion(self, ctx, date: str, heures: str):
        channel = disnake.utils.get(ctx.guild.text_channels, name='salon-réunion')  # Remplacez par le nom correct du salon
        role_staff = disnake.utils.get(ctx.guild.roles, name='📂〢Staff')
        role_haut_staff = disnake.utils.get(ctx.guild.roles, name='📂〢Haut staff')

        if channel:
            em = disnake.Embed(
                title='Annonce Réunion', 
                description=f'Une réunion aura lieu le {date} à {heures}.', 
                color=disnake.Color.blue()
            )
            em.set_image(url='https://i.ibb.co/dbPZcmV/c92885e55b3f6deb5a626d0e4f984040.gif')

            await channel.send(content=f"{role_staff.mention} {role_haut_staff.mention}", embed=em)
            await ctx.response.send_message(f"Réunion organisée pour le {date} à {heures}.", delete_after=3)
        else:
            await ctx.response.send_message("Le salon de réunion spécifié n'existe pas.", delete_after=3)

    # Commande pour bannir un utilisateur
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: disnake.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("Vous ne pouvez pas vous bannir vous-même !")
            return
        if reason is None:
            reason = "Aucune raison fournie"

        await member.ban(reason=reason)
        embed = disnake.Embed(
            title=f"{member.name} a été banni",
            description=f"Raison: {reason}",
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed)

    # Commande pour bannir temporairement un utilisateur
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tempban(self, ctx, member: disnake.Member, time: int, unit: str, *, reason=None):
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

    # Gestion des erreurs des commandes ban et tempban
    @ban.error
    @tempban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Utilisateur non trouvé ou mauvais argument.")
        else:
            await ctx.send("Une erreur est survenue.")

    # Commande pour enregistrer une plainte contre un staff
    @commands.command()
    @commands.has_role('📂〢Staff')
    async def rm_staff(self, ctx, membre: disnake.Member, plainte: str):
        guild = ctx.guild
        channel = disnake.utils.get(guild.text_channels, name="📑〃staff-bilan")
        if channel:
            em = disnake.Embed(
                title=f"Plainte déposée contre {membre.name}",
                description=f"Raison : {plainte}",
                color=disnake.Colour.dark_gray()
            )
            await channel.send(embed=em)
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

    @commands.command(name='promouvoir', description='Promouvoir un membre')
    @commands.has_role('📖〢Gestion Serveur')  
    async def promouvoir(self, ctx, membre: disnake.Member, role: str):
        roles_to_give = self.PROMOTION_ROLES.get(role)

        if roles_to_give:
            roles_to_add = [disnake.utils.get(ctx.guild.roles, name=role_name) for role_name in roles_to_give]

            if None in roles_to_add:
                await ctx.send("Un ou plusieurs rôles spécifiés n'existent pas.", delete_after=5)
                return

            await membre.add_roles(*roles_to_add)
            await ctx.send(f"{membre.mention} a été promu au rôle {role}.")
        else:
            await ctx.send(f"Rôle {role} invalide.", delete_after=5)

        
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
