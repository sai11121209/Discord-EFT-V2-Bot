import json
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from pytz import timezone
import datetime
from datetime import datetime as dt
from util import get_requests_response, get_translate_text
from const import Url, ServerStatusCode, ServerStatusColorCode


JST = datetime.timezone(datetime.timedelta(hours=9) , 'JST')

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.status_data = {
            "status": None,
            "service": None,
            "datacenter": None,
            "information": None,
        }

    @app_commands.command(name="status", description="EscapefromTarkovサーバのステータスを表示")
    async def status(self, integration: discord.Integration) -> None:
        await integration.response.defer(thinking=True)
        for key, value in Url.SERVER_STATUS_MAP.items():
            res = get_requests_response(value)
            self.status_data[key] = json.loads(res.text)
        embed = self.bot.create_base_embed(
            title=f"EscapeTarkovServerStatus",
            color=ServerStatusColorCode.SERVER_STATUS_COLOR_CODE_MAP.get(str(self.status_data["status"]["status"])),
            url="https://status.escapefromtarkov.com/",
            thumbnail="https://status.escapefromtarkov.com/favicon.ico",
            footer="Source: Escape from Tarkov Status 最終更新"
        )
        for key, values in self.status_data.items():
            if key == "status":
                embed.add_field(
                    name=f"ステータス: {ServerStatusCode.SERVER_STATUS_CODE_MAP.get(str(values['status']))}",
                    value=f"> {values['message']}",
                    inline=False,
                )
            if key == "service":
                text = ""
                for value in values:
                    text += (
                        f"> **{value['name']}** : {ServerStatusCode.SERVER_STATUS_CODE_MAP.get(str(value['status']))}\n"
                    )
                embed.add_field(
                    name="各種サービスステータス",
                    value=text,
                    inline=False,
                )
            if key == "information":
                try:
                    message = ""
                    res = get_translate_text(values[0]["content"]).json()
                    if res["code"] == 200:
                        text = res["text"]
                    message += f"\n> {values[0]['content']}\n"
                    message += f"\n> {text}"
                    message += "\n> Google翻訳"
                    embed.add_field(
                        name=f"アナウンス最終更新 {dt.fromisoformat(values[0]['time']).astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')}",
                        value=f"{message} ",
                        inline=False,
                    )
                except:
                    pass
        await self.bot.send_deletable_message(integration, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Status(bot))
