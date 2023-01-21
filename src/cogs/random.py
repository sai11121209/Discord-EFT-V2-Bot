import random as r
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

class Random(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="random", description="マップ・武器抽選")
    @app_commands.describe(type="抽選種類")
    @app_commands.choices(
        type = [
            Choice(name="マップ", value="map"),
            Choice(name="武器", value="weapon"),
        ]
    )
    async def random(self, intrtaction: discord.Integration, type: str) -> None:
        if type=="map":
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選",
                description=f"{intrtaction.user.mention}が赴くマップは...",
                color=0x2ECC69,
            )
            map = r.choice(
                [key for key, val in self.bot.maps_detail.items() if val["Duration"] != ""]
            ).lower()
            embed.add_field(name="MAP", value=map, inline=False)
        else:
            embed = discord.Embed(
                title="迷ったときのEFT武器抽選",
                description=f"{intrtaction.user.mention}が使用する武器は...",
                color=0x2ECC69,
            )
            weapon = r.choice(self.bot.weapons_name)
            embed.add_field(name="WEAPON", value=weapon, inline=False)
        await self.bot.send_deletable_message(intrtaction, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Random(bot))
