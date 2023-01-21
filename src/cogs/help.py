import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import datetime
from datetime import datetime as dt


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="使用可能コマンド表示")
    async def help(self, intrtaction: discord.Integration) -> None:
        await intrtaction.response.defer(thinking=True)
        embed = discord.Embed(
            title="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧だよ!",
            description=f"```Prefix:{self.bot.command_prefix}```",
            color=0x2ECC69,
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.strptime(
                    list(self.bot.PATCH_NOTES.keys())[0].split(":", 1)[1] + "+09:00",
                    "%Y/%m/%d %H:%M%z",
                ).timestamp()
            )

        )
        for command in self.bot.tree.get_commands():
            try:
                if command.name == "weapon":
                    text = f"```{self.bot.command_prefix}{command.name}```"
                    text += "```/weapon {武器名}```"
                elif command.name == "market":
                    text = f"```{self.bot.command_prefix}{command.name}```"
                    text += "```!p {アイテム名}```"
                elif command.name == "map":
                    text = f"```{self.bot.command_prefix}{command.name}```"
                    text += "```/map {マップ名}```"
                elif command.name == "task":
                    text = f"```{self.bot.command_prefix}{command.name}```"
                    text += "```/task {タスク名}```"
                else:
                    text = f"```{self.bot.command_prefix}{command.name}```"
                if command.name != "help":
                    embed.add_field(
                        name=f"{command.description}コマンド",
                        value=text,
                    )
            except:
                pass
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_author(
            name="EFT(Escape from Tarkov) Wiki Bot",
            url="https://github.com/sai11121209",
            icon_url=self.bot.user.avatar.url,
        )
        embed.set_footer(text="EFT Wiki Bot最終更新")
        await self.bot.send_deletable_message(intrtaction, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
