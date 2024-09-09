import disnake
from disnake.ext import commands, tasks
import random
import json

with open('Json/question.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    questions = [item['question'] for item in data]

class Quest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.send_random_question.start()

    @tasks.loop(hours=5) 
    async def send_random_question(self):
        guild = disnake.utils.get(self.bot.guilds, name="La Taverne 🍻")
        channel = disnake.utils.get(guild.text_channels, name="❔〃question-du-jour")
        role = disnake.utils.get(channel.guild.roles, name="❔〢Ping Question !")

        if channel is not None and role is not None:
            try:
                await channel.purge(limit=100)
            except Exception as e:
                print(f"Erreur lors de la purge des messages: {e}")

            question = random.choice(questions)

            embed = disnake.Embed(
                title="Question du jour",
                description=question,
                color=0x00ff00
            )
            embed.add_field(name='Hésitez pas à répondre dans :', value='https://discord.com/channels/1251476405112537148/1269373203650973726')

            await channel.send(content=role.mention, embed=embed)

    @send_random_question.before_loop
    async def before_send_random_question(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Quest(bot))
