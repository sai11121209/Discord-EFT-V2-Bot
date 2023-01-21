import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


class test(commands.Cog, commands.HelpCommand):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="test", description="test")
    @app_commands.describe(name="名前")
    async def test(self, intrtaction: discord.Integration, name: str) -> None:
        embeds = []
        embeds.append(discord.Embed(
            title=f"武器一覧1",
            timestamp=self.bot.update_timestamp,
        ))
        embeds.append(discord.Embed(
            title=f"武器一覧2",
            timestamp=self.bot.update_timestamp,
        ))
        paginator = commands.Paginator(embeds)
        # await self.bot.send_deletable_message(intrtaction, name)
        self.send_pages
        await intrtaction.response.send_message(embeds=embeds)

    # @app_commands.command(name="", description="")
    # async def top(self, intrtaction: discord.Integration) -> None:

    #     await self.bot.send_deletable_message(intrtaction, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(test(bot))
