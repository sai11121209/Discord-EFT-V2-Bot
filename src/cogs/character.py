import discord
from discord import app_commands
from discord.ext import commands
from const import Url
from util import get_url


class Character(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="dealers", description="ディーラー一覧表示")
    async def dealers(self, intrtaction: discord.Integration) -> None:
        embed = discord.Embed(
            title="ディーラー",
            url=get_url(Url.EN_WIKI, "Characters#Dealers"),
            color=0x808080,
            timestamp=self.bot.update_timestamp,
        )
        for trader_name in self.bot.trader_name:
            trader = self.bot.TRADER_LIST[trader_name]
            text = f"**本名**: __{trader['fullname']}__\n"
            if (
                "A network of outlets all over Tarkov and its outskirts"
                != trader["location"]
            ):
                text += f"**場所**: __[{trader['location']}]({Url.EN_WIKI}{trader['location'].replace(' ', '_')})__\n"
            else:
                text += f"**場所**: __{trader['location']}__\n"
            text += f"**出身地**: __{trader['origin']}__\n"
            text += "**取り扱い品**:\n"
            for ware in trader["wares"]:
                text += f"・__{ware}__\n"
            if trader["services"]:
                text += "**サービス**:\n"
                for service in trader["services"]:
                    text += f"・__{service}__\n"
            else:
                text += "**サービス**: 無し\n"
            text += f"**通貨**:\n"
            for currencie in trader["currencies"]:
                text += f"・__{currencie}__\n"
                # trader_name.capitalize()
            text += f"**タスク情報**: [JA]({Url.JA_WIKI}{trader_name}タスク) / [EN]({Url.EN_WIKI}Quests)\n"
            text += f"**詳細情報**: [EN]({Url.EN_WIKI}{trader_name})"
            embed.add_field(
                name=f"<:{trader_name}:{trader['stampid']}> {trader_name}",
                value=text,
            )
        embed.set_author(
            name="EFT(Escape from Tarkov) Wiki Bot",
            url="https://github.com/sai11121209",
            # icon_url=client.get_user(279995095124803595).avatar_url,
        )
        embed.set_footer(
            text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできるよー。",
        )
        await self.bot.send_deletable_message(intrtaction, embed=embed)

    @app_commands.command(name="boss", description="ボス一覧表示")
    async def boss(self, intrtaction: discord.Integration) -> None:
        embed = discord.Embed(
            title="ボス",
            url=f"{Url.EN_WIKI}Characters#Bosses",
            color=0x808080,
            timestamp=self.bot.update_timestamp,
        )
        for boss_name in self.bot.boss_name:
            try:
                boss = self.bot.BOSS_LIST[boss_name]
                text = ""
                text += "**場所**:"
                if len(boss["location"]) == 1:
                    text += f"__[{boss['location'][0]}]({Url.EN_WIKI}{boss['location'][0]})__\n"
                    text += (
                        f"**出現確率**: __{boss['pawnchance'][boss['location'][0]]}%__\n"
                    )
                else:
                    text += "\n"
                    for location in boss["location"]:
                        text += f"・__[{location}]({Url.EN_WIKI}{location})__\n"
                    text += f"**出現確率**:\n"
                    for location in boss["location"]:
                        text += (
                            f"・__{location}__: __{boss['pawnchance'][location]}%__\n"
                        )
                text += "**レアドロップ**:\n"
                for drop in boss["drops"]:
                    text += (
                        f"・__[{drop}]({Url.EN_WIKI}{drop.replace(' ', '_')})__\n"
                    )
                text += f"**護衛**: {boss['followers']}人\n"
                if boss_name != "CultistPriest":
                    text += f"**詳細情報**: [EN]({Url.EN_WIKI}{boss_name})"
                else:
                    text += f"**詳細情報**: [EN]({Url.EN_WIKI}Cultists)"
                embed.add_field(
                    name=f"<:{boss_name}:{boss['stampid']}> {boss_name}",
                    value=text,
                )
            except:
                pass
        embed.set_author(
            name="EFT(Escape from Tarkov) Wiki Bot",
            url="https://github.com/sai11121209",
            # icon_url=client.get_user(279995095124803595).avatar_url,
        )
        embed.set_footer(
            text="ボス名をクリックすることで各ボスの詳細情報にアクセスできるよー。",
        )
        await self.bot.send_deletable_message(intrtaction, embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Character(bot))
