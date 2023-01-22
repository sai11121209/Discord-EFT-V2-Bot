import discord
from discord import app_commands
from discord.ext import commands
from const import Url


class Link(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="top", description="EFT公式サイト表示")
    async def top(self, integration: discord.Integration) -> None:
        text = "www.escapefromtarkov.com"
        embed = self.bot.create_base_embed(
            title="Escape from Tarkov official page",
            url=Url.EFT_HP,
            description=text,
            color=0x2ECC69,
            thumbnail="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
        )
        await self.bot.send_deletable_message(integration, embed=embed)

    @app_commands.command(name="jawiki", description="日本EFTWikiサイト表示")
    async def ja_wiki(self, integration: discord.Integration) -> None:
        text = "wikiwiki.jp"
        embed = self.bot.create_base_embed(
            title="日本Escape from Tarkov WIKI",
            url=Url.JA_WIKI,
            description=text,
            color=0x2ECC69,
            thumbnail="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
        )
        await self.bot.send_deletable_message(integration, embed=embed)

    @app_commands.command(name="enwiki", description="海外EFTWikiサイト表示")
    async def en_wiki(self, integration: discord.Integration) -> None:
        text = "The Official Escape from Tarkov Wiki"
        embed = self.bot.create_base_embed(
            title="海外Escape from Tarkov WIKI",
            url=Url.EN_WIKI+"Escape_from_Tarkov_Wiki",
            description=text,
            color=0x2ECC69,
            thumbnail="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/b/bc/Wiki.png/revision/latest/scale-to-width-down/200?cb=20200612143203"
        )
        await self.bot.send_deletable_message(integration, embed=embed)

    @app_commands.command(name="market", description="フリーマーケット情報表示")
    async def market(self, integration: discord.Integration) -> None:
        text = "Actual prices, online monitoring, hideout, charts, price history"
        embed = self.bot.create_base_embed(
            title="Tarkov Market フリーマーケット情報",
            url=Url.MARKET,
            description=text,
            color=0x2ECC69,
        )
        await self.bot.send_deletable_message(integration, embed=embed)

    @app_commands.command(name="loadouts", description="ロードアウト作成")
    async def loadouts(self, integration: discord.Integration) -> None:
        text = "Actual prices, online monitoring, hideout, charts, price history"
        embed = self.bot.create_base_embed(
            title="Tarkov Market ロードアウト作成",
            url="https://tarkov-market.com/loadouts/weapon",
            description=text,
            color=0x2ECC69,
        )
        await self.bot.send_deletable_message(integration, embed=embed)

    @app_commands.command(name="tarkovtools", description="TarkovTools情報表示")
    async def tarkovtools(self, integration: discord.Integration) -> None:
        text = "Visualization of all ammo types in Escape from Tarkov, along with maps and other great tools"
        embed = self.bot.create_base_embed(
            title="Tarkov Tools",
            url=Url.EFT_TOOL,
            description=text,
            color=0x2ECC69,
        )
        embed.add_field(
            name="Tarkov-Tools",
            value="> [Tarkov-Tools携帯リモート操作リンク](https://tarkov-tools.com/control/)",
        )
        await self.bot.send_deletable_message(integration, embed=embed)

    @app_commands.command(name="source", description="ソースコード表示")
    async def source(self, integration: discord.Integration) -> None:
        text = "Contribute to sai11121209/Discord-EFT-V2-Bot development by creating an account on GitHub."

        embed = self.bot.create_base_embed(
            title="GitHub",
            url="https://github.com/sai11121209/Discord-EFT-V2-Bot",
            description=text,
            color=0x2ECC69,
            thumbnail="https://avatars.githubusercontent.com/u/55883274?s=400&v=4"
        )
        await self.bot.send_deletable_message(integration, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Link(bot))
