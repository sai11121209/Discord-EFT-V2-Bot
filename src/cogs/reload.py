import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import datetime
from datetime import datetime as dt
from const import CommandCategory


JST = datetime.timezone(datetime.timedelta(hours=9) , 'JST')

class Reload(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="reload", description="Wikiデータの最新化")
    @app_commands.describe(category="更新カテゴリ")
    @app_commands.choices(
        category = [
            Choice(name="マップ", value="map"),
            Choice(name="キャラクター(トレーダー・ボス)", value="character"),
            Choice(name="タスク", value="task"),
            Choice(name="武器・弾薬", value="weapon"),
            Choice(name="全て", value="all")
        ]
    )
    async def reload(self, integration: discord.Integration, category: str) -> None:
        await integration.response.defer(thinking=True)
        await self.bot.data_reload(category)
        embed = self.bot.create_base_embed(
            title="データのリロード完了",
            color=0xFF0000,
        )
        embed.add_field(
            name="リロードカテゴリ",
            value=CommandCategory.COMMAND_CATEGORY_MAP.get(category),
            inline=False,
        )
        await self.bot.send_deletable_message(integration, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Reload(bot))
