import discord
from discord import app_commands
from discord.ext import commands
import datetime
from datetime import datetime as dt
import pandas as pd
import requests as rq
from matplotlib import pyplot as plt


JST = datetime.timezone(datetime.timedelta(hours=9) , 'JST')

class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="patch", description="パッチノート表示")
    async def patch(self, intrtaction: discord.Integration) -> None:
        if self.bot.NOTIFICATION_INFORMATION:
            embed = self.bot.create_base_embed(
                title="近日大規模なアップデートが行われる予定です。",
                description="近日行われるアップデートでは以下の機能が変更又は追加される予定です。\n※アップデートに伴い現在テストバージョンでの処理となっているため**一部又は全体の動作が不安定**になる恐れがあります。",
                url="https://github.com/sai11121209/Discord-EFT-V2-Bot",
                color=0xFF0000,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.strptime(
                        list(self.bot.PATCH_NOTES.keys())[0].split(":", 1)[1] + "+09:00",
                        "%Y/%m/%d %H:%M%z",
                    ).timestamp()
                ),
                author_url="https://github.com/sai11121209/Discord-EFT-V2-Bot",
                footer="Escape from Tarkov Bot 最終更新",
                thumbnail=self.bot.user.avatar.url
            )
            text = ""
            for index, values in self.bot.NOTIFICATION_INFORMATION.items():
                for N, value in enumerate(values):
                    text += f"{N+1}. {value}\n"
            embed.add_field(
                name=f"version: {index.split(':', 1)[0]}", value=text, inline=False
            )
            await self.bot.send_deletable_message(intrtaction, embed=embed)

        embed = self.bot.create_base_embed(
            title="更新履歴一覧",
            url="https://github.com/sai11121209/Discord-EFT-V2-Bot",
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.strptime(
                    list(self.bot.PATCH_NOTES.keys())[0].split(":", 1)[1] + "+09:00",
                    "%Y/%m/%d %H:%M%z",
                ).timestamp()
            ),
            author_url="https://github.com/sai11121209/Discord-EFT-V2-Bot",
            footer="Escape from Tarkov Bot 最終更新",
            thumbnail=self.bot.user.avatar.url
        )
        for index, values in list(self.bot.PATCH_NOTES.items())[:1]:
            text = ""
            for N, value in enumerate(values):
                text += f"{N+1}. {value}\n\n"
            embed.add_field(
                name=f"version: {index.split(':', 1)[0]}", value=text, inline=False
            )
        await self.bot.send_deletable_message(intrtaction, embed=embed)

    @app_commands.command(name="now", description="現在時刻表示")
    async def now(self, intrtaction: discord.Integration) -> None:
        embed = self.bot.create_base_embed(
            title="現在時刻",
            description="主要タイムゾーン時刻",
            url="https://www.time-j.net/WorldTime/NOW",
            color=0x2ECC69,
            footer="夏時間は3月の第2日曜日午前2時から11月の第1日曜日午前2時まで。"
        )
        embed.add_field(
            name="日本時間(JST)",
            value=dt.now().strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        embed.add_field(
            name="モスクワ時間(EAT)",
            value=dt.now(
                datetime.timezone(datetime.timedelta(hours=3), name="EAT")
            ).strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        embed.add_field(
            name="太平洋標準時刻(PST)",
            value=dt.now(
                datetime.timezone(datetime.timedelta(hours=-8), name="PST")
            ).strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        embed.add_field(
            name="太平洋夏時刻(PDT)",
            value=dt.now(
                datetime.timezone(datetime.timedelta(hours=-7), name="PDT")
            ).strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        await self.bot.send_deletable_message(intrtaction, embed=embed)

    @app_commands.command(name="btc", description="ビットコイン価格表示")
    async def btc(self, intrtaction: discord.Integration) -> None:
        timestamp = dt.now(JST).timestamp()
        summary_jpy = rq.get(
            "https://api.cryptowat.ch/markets/bitflyer/btcjpy/summary"
        ).json()["result"]
        btc_jpy_data = rq.get(
            f"https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods=1800&after={int(timestamp)}"
        ).json()["result"]
        btc_data = pd.DataFrame(btc_jpy_data["1800"])
        btc_data[0] = pd.to_datetime(btc_data[0].astype(int), unit="s")
        plt.figure(figsize=(15, 10), dpi=100)
        plt.plot(btc_data[0], btc_data[1], label="OpenPrice")
        plt.plot(btc_data[0], btc_data[2], label="HighPrice")
        plt.plot(btc_data[0], btc_data[3], label="LowPrice")
        plt.title("BTC_JPY Rate")
        plt.grid(axis="y", linestyle="dotted", color="b")
        plt.tight_layout()
        plt.legend()
        plt.savefig("btc_jpy.png")
        plt.close()
        BtcJpyPrice = rq.get(
            "https://api.cryptowat.ch/markets/bitflyer/btcjpy/price"
        ).json()["result"]["price"]
        file = discord.File("btc_jpy.png")
        embed = self.bot.create_base_embed(
            title="1 ビットコイン → 日本円",
            color=0xFFFF00,
            footer="Cryptowat Market REST APIを使用しております。取得日時"
        )
        embed.set_image(url="attachment://btc_jpy.png")
        embed.add_field(name="現在の金額", value="{:,}".format(BtcJpyPrice) + " 円")
        embed.add_field(
            name="0.2BTCあたりの金額",
            value="約 " + "{:,}".format(int(BtcJpyPrice * 0.2)) + " 円",
        )
        embed.add_field(
            name="最高値", value="{:,}".format(summary_jpy["price"]["high"]) + " 円"
        )
        embed.add_field(
            name="最安値", value="{:,}".format(summary_jpy["price"]["low"]) + " 円"
        )
        await self.bot.send_deletable_message(intrtaction, embed=embed, file=file)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
