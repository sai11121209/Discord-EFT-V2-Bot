import discord
from discord import app_commands
from discord.ext import commands


class Chart(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="recovery",
        description="回復早見表",
    )
    async def chart_recovery(self, intrtaction: discord.Integration) -> None:
        recovery_images = [
            "abnormal_state.jpg",
            "recovery.jpg",
        ]
        author_list = [
            {
                "author": {
                    "name": "Twitter: Rushy_ve_",
                    "url": "https://twitter.com/Rushy_ve_",
                },
                "link": "https://twitter.com/Rushy_ve_/status/1231153891808440321?s=20",
            },
            {
                "author": {
                    "name": "Twitter: Rushy_ve_",
                    "url": "https://twitter.com/Rushy_ve_",
                },
                "link": "https://twitter.com/Rushy_ve_/status/1231153891808440321?s=20",
            },
        ]
        for n, (url, author) in enumerate(zip(recovery_images, author_list)):
            file = discord.File(f"../imgs/chart/health/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(recovery_images)})回復早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            await self.bot.send_deletable_message(intrtaction, embed=embed, file=file)

    @app_commands.command(
        name="itemvalue",
        description="アイテム価格早見表",
    )
    async def chart_itemvalue(self, intrtaction: discord.Integration) -> None:
        item_value_images = [
            "pyramid.jpg",
            "chart.jpg",
        ]
        author_list = [
            {
                "author": {
                    "name": "Reddit: CALLSIGN-ASTRO",
                    "url": "https://www.reddit.com/user/CALLSIGN-ASTRO/",
                },
                "link": "https://www.reddit.com/r/EscapefromTarkov/comments/eu0pmi/i_tried_to_make_quick_barter_items_price_list_but/?utm_source=share&utm_medium=web2x",
            },
            {
                "author": {
                    "name": "Tarkov Tools",
                    "url": "https://tarkov-tools.com/",
                },
                "link": "https://tarkov-tools.com/loot-tier/",
            },
        ]
        for n, (url, author) in enumerate(zip(item_value_images, author_list)):
            file = discord.File(f"../imgs/chart/item/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(item_value_images)})アイテム価格早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            await self.bot.send_deletable_message(intrtaction, embed=embed, file=file)

    @app_commands.command(
        name="taskitem",
        description="タスク使用アイテム早見表",
    )
    async def chart_taskitem(self, intrtaction: discord.Integration) -> None:
        task_item_images = [
            "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/1/19/QuestItemRequirements.png/revision/latest?cb=20210212192637&format=original",
            "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/f/f8/QuestItemsInRaid.png/revision/latest?cb=20210212192627&format=original",
        ]
        author_list = [
            {
                "author": {
                    "name": "Official Escape from Tarkov Wiki",
                    "url": "https://escapefromtarkov.fandom.com/wiki/Quests",
                },
                "link": "https://escapefromtarkov.fandom.com/wiki/Quests",
            },
            {
                "author": {
                    "name": "Official Escape from Tarkov Wiki",
                    "url": "https://escapefromtarkov.fandom.com/wiki/Quests",
                },
                "link": "https://escapefromtarkov.fandom.com/wiki/Quests",
            },
        ]
        for n, (url, author) in enumerate(zip(task_item_images, author_list)):
            embed = discord.Embed(
                title=f"({n+1}/{len(task_item_images)})タスク使用アイテム早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=url)
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            await self.send_deletable_message(intrtaction, embed=embed)

    @app_commands.command(
        name="tasktree",
        description="タスクツリー早見表",
    )
    async def chart_tasktree(self, intrtaction: discord.Integration) -> None:
        task_item_images = [
            "tree.jpg",
        ]
        author_list = [
            {
                "author": {
                    "name": "Twitter: @morimoukorigori",
                    "url": "https://twitter.com/morimoukorigori",
                },
                "link": "https://twitter.com/morimoukorigori/status/1357008341940064256",
            },
        ]
        for n, (url, author) in enumerate(zip(task_item_images, author_list)):
            file = discord.File(f"../imgs/chart/task/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(task_item_images)})タスクツリー早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            await self.send_deletable_message(intrtaction, embed=embed, file=file)

    @app_commands.command(
        name="armor",
        description="アーマー早見表",
    )
    async def chart_armor(self, intrtaction: discord.Integration) -> None:
        armor_images = [
            "class4.jpg",
            "class5.jpg",
            "class6.jpg",
            "graph.jpg",
        ]
        for n, url in enumerate(armor_images):
            file = discord.File(f"../imgs/chart/armor/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(armor_images)})アーマー早見表",
                color=0x808080,
                url=f"{self.bot.enWikiUrl}Armor_vests",
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name="Twitter: @N7th_WF",
                url="https://twitter.com/N7th_WF",
            )
            embed.set_footer(
                text="提供元: https://twitter.com/N7th_WF/status/1376825476598013957?s=20"
            )
            await self.send_deletable_message(intrtaction, embed=embed, file=file)

    @app_commands.command(
        name="headset",
        description="ヘッドセット早見表",
    )
    async def chart_headset(self, intrtaction: discord.Integration) -> None:
        headset_images = [
            "chart.PNG",
            "gssh_comtac2.PNG",
            "sordin_tactical.PNG",
            "razor_xcel.PNG",
            "m32_rac.PNG",
        ]
        for n, url in enumerate(headset_images):
            file = discord.File(f"../imgs/chart/headset/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(headset_images)})ヘッドセット早見表",
                color=0x808080,
                url=f"{self.bot.enWikiUrl}Headsets",
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name="セヴンスGaming",
                url="https://www.youtube.com/channel/UCZpSzN3ozBUnJrXLmx50qVA",
            )
            embed.set_footer(
                text="提供元: [ EFT 解説 ] ヘッドセットの選び方ガイド②考察編【タルコフ】 https://www.youtube.com/watch?v=LyVGpyBZ0EU"
            )
            await self.send_deletable_message(intrtaction, embed=embed, file=file)

    @app_commands.command(
        name="lighthousetask",
        description="Lighthouseタスク早見表",
    )
    async def chart_lighthousetask(self, intrtaction: discord.Integration) -> None:
        lighthouse_task_images = [
            "lighthouse_1.jpg",
            "lighthouse_2.jpg",
            "lighthouse_3.jpg",
            "lighthouse_4.jpg",
        ]
        for n, url in enumerate(lighthouse_task_images):
            file = discord.File(f"../imgs/chart/task/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(lighthouse_task_images)})ヘッドセット早見表",
                color=0x808080,
            )
            embed.set_image(url=f"attachment://{url}")
            await self.send_deletable_message(intrtaction, embed=embed, file=file)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chart(bot))
