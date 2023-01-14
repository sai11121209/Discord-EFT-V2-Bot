import discord
from discord import app_commands
from discord.ext import commands
import datetime
from datetime import datetime as dt
from const import Url
from util import get_requests_response, get_beautiful_soup_object


JST = datetime.timezone(datetime.timedelta(hours=9) , 'JST')

class Rate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def get_rate(self, name):
        res = get_requests_response(Url.MARKET, name)
        soup = get_beautiful_soup_object(res, class_name=None)
        return soup.find("div", {"class": "bold alt"}).get_text().replace("₽", "")

    @app_commands.command(name="rate", description="EFT為替レートを表示")
    async def rate(self, intrtaction: discord.Integration) -> None:
        euro = self.get_rate("euros")
        dollar = self.get_rate("dollars")
        embed = discord.Embed(
            title=f"EFT為替レート",
            color=0x808080,
        )
        embed.add_field(
            name="ユーロ値段",
            value=f"{euro}₽",
        )
        embed.add_field(
            name="ドル値段",
            value=f"{dollar}₽",
        )
        embed.set_footer(text=f"提供元: {Url.MARKET}")
        await self.bot.send_deletable_message(intrtaction, embed=embed)

    @app_commands.command(name="euro", description="EUR → RUB 為替レート計算")
    @app_commands.describe(price="ユーロの値段を入力。")
    async def rate_euro(self, intrtaction: discord.Integration, price: int) -> None:
        euro = self.get_rate("euros")
        embed = discord.Embed(
            title=f"RUB → EUR 為替レート計算",
            color=0x808080,
        )
        embed.add_field(
            name="ユーロ値段",
            value=f"{price}€",
        )
        embed.add_field(
            name="換算ルーブル値段",
            value=f"{int(euro)*price}₽",
        )
        embed.set_footer(text=f"提供元: {Url.MARKET}")
        await self.bot.send_deletable_message(intrtaction, embed=embed)

    @app_commands.command(name="dollar", description="USD → RUB 為替レート計算")
    @app_commands.describe(price="ドルの値段を入力。")
    async def rate_dollar(self, intrtaction: discord.Integration, price: int) -> None:
        dollar = self.get_rate("dollars")
        embed = discord.Embed(
            title=f"EFT為替レート",
            color=0x808080,
        )
        embed.add_field(
            name="ドル値段",
            value=f"{price}$",
        )
        embed.add_field(
            name="換算ルーブル値段",
            value=f"{int(dollar)*price}₽",
        )
        embed.set_footer(text=f"提供元: {Url.MARKET}")
        await self.bot.send_deletable_message(intrtaction, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Rate(bot))
