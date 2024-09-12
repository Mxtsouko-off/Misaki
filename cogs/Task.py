import disnake
from disnake.ext import commands, tasks

class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remind_bumping.start()  
        self.check_status.start()   


    @tasks.loop(hours=2)
    async def remind_bumping(self):
        for guild in self.bot.guilds:
            channel = disnake.utils.get(guild.text_channels, name='🌊〃bump')
            role = disnake.utils.get(guild.roles, name='🌊〢Ping Bumping')
            if channel is not None and role is not None:
                embed = disnake.Embed(
                    title="Rappel de Bump",
                    description="Il est temps de bump le serveur !",
                    color=0xFF5733
                )
                await channel.send(content=role.mention, embed=embed)

    @tasks.loop(minutes=3)
    async def check_status(self):
        for guild in self.bot.guilds:
            role = disnake.utils.get(guild.roles, name='🦾〢Soutient Bio')
            if role is None:
                print(f"Rôle '🦾〢Soutient Bio' non trouvé dans {guild.name}.")
                continue

            for member in guild.members:
                if member.bot:
                    continue   
                if member.status == disnake.Status.offline:
                    continue   

                has_custom_status = any(
                    activity.type == disnake.ActivityType.custom and activity.state and '/Taverne' in activity.state
                    for activity in member.activities
                )

                if has_custom_status:
                    if role not in member.roles:
                        await member.add_roles(role)
                        print(f'Rôle ajouté à {member.display_name} dans {guild.name}')
                else:
                    if role in member.roles:
                        await member.remove_roles(role)
                        print(f'Rôle retiré de {member.display_name} dans {guild.name}')

    @remind_bumping.before_loop
    @check_status.before_loop
    async def before_tasks(self):
        await self.bot.wait_until_ready()   

def setup(bot):
    bot.add_cog(Task(bot))
