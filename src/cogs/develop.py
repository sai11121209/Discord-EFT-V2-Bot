import discord
from discord import app_commands
from discord.ext import commands


class Develop(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="develop", description="開発用(実行権限制限あり)")
    async def develop(self, integration: discord.Integration) -> None:
        if self.bot.LOCAL_HOST: return
        self.bot.develop_mode = not self.bot.develop_mode
        message = "開発モードになりました。機能が一部制限されます。" if self.bot.develop_mode else "通常モードに復帰しました。機能制限が解除されます。"
        if self.bot.develop_mode:
            await self.bot.set_status(
                status=discord.Status.dnd,
                activity_name="機能改善会議(メンテナンス中)",
                activity_type=discord.ActivityType.competing,
            )
            self.bot.enrageCounter = 0
        else:
            await self.bot.set_status()
        await self.bot.send_deletable_message(integration, message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Develop(bot))
