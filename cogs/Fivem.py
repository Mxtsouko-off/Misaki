import disnake
from disnake.ext import commands
import aiohttp
import base64
import io


class Fivem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        
        @commands.slash_command()
        async def fivemlookup(ctx, tag):
            urlfivem = f"https://servers-frontend.fivem.net/api/servers/single/{tag}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.3",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(urlfivem, headers=headers) as res:
                    if res.status == 404:
                        embed = disnake.Embed(
                            title="Invalid Code",
                            color=0xc73e10,
                        )
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    else:
                        data = await res.json()
                        connect_endpoint = data["Data"]["connectEndPoints"][0]

                        if not connect_endpoint.startswith("http"):
                            split = connect_endpoint.split(":")
                            urlip = f"http://ip-api.com/json/{split[0]}"
                            async with session.get(urlip) as res2:
                                out2 = await res2.json()

                                if "icon" in out2:
                                    icon = out2["icon"]
                                    file = disnake.File(io.BytesIO(base64.b64decode(icon)), filename="graph.png")
                                    embed = disnake.Embed(
                                        color=0xc73e10,
                                    )
                                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                                    embed.add_field(name="IP:Port", value=f"`{connect_endpoint}`")
                                    embed.add_field(name="Server Details", value=f"IP: `{split[0]}`\n Country: `{out2['country']}`\n City: `{out2['city']}`\n ISP: `{out2['isp']}`\n Org: `{out2['org']}`\n Zip Code: `{out2['zip']}`\n Timezone: `{out2['timezone']}`\n")
                                    embed.add_field(name="FiveM Server", value=f"Server Name: `{data['Data']['hostname'][:390]}`\n Online Players: `{len(data['Data']['players'])}`\n Max Players: `{data['Data']['svMaxclients']}`\n Artifacts: `{data['Data']['server']}`\n Resources: `{len(data['Data']['resources'])}`\n Onesync Enabled?: `{data['Data']['vars']['onesync_enabled']}`\n", inline=True)
                                    embed.set_footer(text="By Mxtsouko")
                                    embed.set_thumbnail(url="attachment://graph.png")
                                    await ctx.send(embed=embed, file=file)
                                else:
                                    embed = disnake.Embed(
                                        color=0xc73e10,
                                    )
                                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                                    embed.add_field(name="IP:Port", value=f"`{connect_endpoint}`")
                                    embed.add_field(name="Server Details", value=f"IP: `{split[0]}`\n Country: `{out2['country']}`\n City: `{out2['city']}`\n ISP: `{out2['isp']}`\n Org: `{out2['org']}`\n Zip Code: `{out2['zip']}`\n Timezone: `{out2['timezone']}`\n")
                                    embed.add_field(name="FiveM Server", value=f"Server Name: `{data['Data']['hostname'][:390]}`\n Online Players: `{len(data['Data']['players'])}`\n Max Players: `{data['Data']['svMaxclients']}`\n Artifacts: `{data['Data']['server']}`\n Resources: `{len(data['Data']['resources'])}`\n Onesync Enabled?: `{data['Data']['vars']['onesync_enabled']}`\n", inline=True)
                                    embed.set_footer(text="By Mxtsouko")
                                    await ctx.send(embed=embed)
                        else:
                            embed = disnake.Embed(
                                title="Cannot find server details...",
                                description=f"`{connect_endpoint}`",
                                color=0xc73e10,
                            )
                            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                            await ctx.send(embed=embed)
    
            @commands.slash_command()
            async def cip(ctx, tag):
                    urlfivem = f"https://servers-frontend.fivem.net/api/servers/single/{tag}"

                    async with aiohttp.ClientSession() as session:
                        async with session.get(urlfivem) as res:
                            if res.status == 404:
                                embed = disnake.Embed(
                                    title="Invalid Code",
                                    color=0xc73e10,
                                )
                                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                                await ctx.send(embed=embed)
                            else:
                                data = await res.json()
                                connect_endpoint = data["Data"]["connectEndPoints"][0]

                                embed = disnake.Embed(
                                    color=0xc73e10,
                                )
                                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                                embed.add_field(name="IP:Port", value=f"`{connect_endpoint}`")
                                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fivem(bot))
