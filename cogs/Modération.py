import disnake
from disnake.ext import commands
from datetime import timedelta
import asyncio
import re

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Filtre les messages contenant des liens Discord
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not message.guild:
            await self.bot.process_commands(message)
            return

        member = message.guild.get_member(message.author.id)

        if member:
            admin_roles = [role.id for role in message.guild.roles if "admin" in role.name.lower()]
            partnership_role_id = 1280429826414477373  # Remplacez par l'ID correct
            staff_id = 1268728239010873395  # Remplacez par l'ID correct

            if any(role.id in admin_roles for role in member.roles) or member.guild_permissions.administrator:
                await self.bot.process_commands(message)
                return
            
            if any(role.id == partnership_role_id for role in member.roles):
                await self.bot.process_commands(message)
                return

        if re.search(r'discord\.gg|discord\.com|discord\.me|discord\.app|discord\.io', message.content, re.IGNORECASE):
            await message.delete()
            warning_message = await message.channel.send(f"{message.author.mention}, les liens Discord ne sont pas autorisés dans ce serveur.")
            await asyncio.sleep(5)
            await warning_message.delete()
            return

        await self.bot.process_commands(message)

    # Commande de suspension temporaire d'un membre du staff
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
            await ctx.response.send_message(f"Réunion organisée pour le {date} à {heures}.", ephemeral=True)
        else:
            await ctx.response.send_message("Le salon de réunion spécifié n'existe pas.", ephemeral=True)

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

    # Définir les rôles pour la promotion
    PROMOTION_ROLES = {
        "Gestion Serveur": ['📖〢Gestion Serveur', '📂〢Staff', '📂〢Haut staff'],
        "Manager": ['⚙️〢Manager', '📂〢Staff', '📂〢Haut staff'],
        "Bot Manager": ['🤖〢Bot Manager', '📂〢Haut staff', '📂〢Staff'],
        "Gerant": ['⚒️〢Gerant', '📂〢Staff', '📂〢Haut staff'],
        "Super Modérateur": ['🌺〢Super Modérateur', '📂〢Staff'],
        "Moderateur": ['🛠️〢Modérateur', '📂〢Staff'],
        "Helpeur": ['🎽〢Helpeur', '📂〢Staff'],
        "Interim": ['🎇〢Interim', '📂〢Staff']
    }

    # Commande pour promouvoir un membre
    @commands.command(name='promouvoir', description='Promouvoir un membre')
    @commands.has_role('📖〢Gestion Serveur')
    async def promouvoir(self, ctx, membre: disnake.Member, role: str):
        roles_to_give = self.PROMOTION_ROLES.get(role)

        if roles_to_give:
            roles_to_add = [disnake.utils.get(ctx.guild.roles, name=role_name) for role_name in roles_to_give]

            if any(role is None for role in roles_to_add):
                await ctx.response.send_message("Un ou plusieurs rôles spécifiés n'existent pas.", ephemeral=True)
                return

            await membre.add_roles(*roles_to_add)
            await ctx.response.send_message(f"{membre.mention} a été promu au rôle {role}.", ephemeral=True)
        else:
            await ctx.response.send_message(f"Rôle {role} invalide.", ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
