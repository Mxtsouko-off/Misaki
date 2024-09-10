import disnake
from disnake.ext import commands, tasks

class StaffStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff_status_message = None
        self.channel_id = 1283104286271864913
        self.role_name = "📂〢Staff" 
        self.update_staff_status.start()

    @tasks.loop(seconds=1)
    async def update_staff_status(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            return

        guild = channel.guild
        role = disnake.utils.get(guild.roles, name=self.role_name)
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

        if self.staff_status_message is None:
            self.staff_status_message = await channel.send(embed=embed)
        else:
            await self.staff_status_message.edit(embed=embed)

    @update_staff_status.before_loop
    async def before_update_staff_status(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(StaffStatus(bot))
