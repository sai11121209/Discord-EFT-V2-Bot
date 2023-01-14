import os
import logging
import time
import datetime
from datetime import datetime as dt
import discord
from discord.ext import tasks, commands
from const import ChannelCode, AuthorCode, ServerStatusCode
import difflib
import random as rand

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # カレントディレクトリ変更

from util import (
    get_server_status,
    get_enrage_message,
    get_translate_text,
)

from loadData import (
    get_map_list,
    get_map_detail,
    get_trader_name,
    get_boss_name,
    get_ammo_data,
    get_weapons_data,
    get_task_data,
)


logging = logging.getLogger(__name__)

JST = datetime.timezone(datetime.timedelta(hours=9) , 'JST')

INITIAL_EXTENSIONS = [
    "cogs.test",
    "cogs.develop",
    "cogs.character",
    "cogs.chart",
    "cogs.other",
    "cogs.link",
    "cogs.rate",
    "cogs.random",
    "cogs.status",
    "cogs.map",
    "cogs.task",
    "cogs.reload",
]
TRADER_LIST = {
    "Prapor": {
        "stampid": 828552629248327690,
        "fullname": "Pavel Yegorovich Romanenko",
        "location": "Town",
        "origin": "ロシア連邦",
        "wares": [
            "武器",
            "弾薬",
            "手榴弾",
            "弾倉",
            "武器MOD",
        ],
        "services": [
            "保険",
            "修理",
        ],
        "currencies": ["Roubles (₽)"],
    },
    "Therapist": {
        "stampid": 828552629256192040,
        "fullname": "Elvira Khabibullina",
        "location": "Streets of Tarkov",
        "origin": "ロシア連邦",
        "wares": [
            "医療品",
            "地図",
            "食料品",
            "コンテナ",
        ],
        "services": [
            "保険",
        ],
        "currencies": [
            "Roubles (₽)",
            "Euros (€)",
        ],
    },
    "Fence": {
        "stampid": 828552627989512204,
        "fullname": "Real name unknown",
        "location": "A network of outlets all over Tarkov and its outskirts",
        "origin": "ロシア連邦",
        "wares": [
            "売られたもの全て",
        ],
        "services": [],
        "currencies": [
            "Roubles (₽)",
        ],
    },
    "Skier": {
        "stampid": 828552629436416010,
        "fullname": "Alexander Fyodorovich Kiselyov",
        "location": "Customs",
        "origin": "ロシア連邦",
        "wares": [
            "武器",
            "弾薬",
            "武器MOD",
            "コンテナ",
            "ユーロ",
        ],
        "services": [
            "修理",
        ],
        "currencies": [
            "Roubles (₽)",
            "Dollars ($)",
            "Euros (€)",
        ],
    },
    "Peacekeeper": {
        "stampid": 828552628682096710,
        "fullname": "Tadeusz Pilsudski",
        "location": "Terminal",
        "origin": "ポーランド共和国",
        "wares": [
            "欧米・NATOの武器",
            "弾薬",
            "手榴弾",
            "弾倉",
            "武器MOD",
            "USドル",
        ],
        "services": [],
        "currencies": [
            "Dollars ($)",
        ],
    },
    "Mechanic": {
        "stampid": 828552628887093328,
        "fullname": "Sergey Arsenyevich Samoylov",
        "location": "Factory",
        "origin": "不明",
        "wares": [
            "欧米・NATOの武器",
            "グロック17/18",
            "弾薬",
            "弾倉",
            "武器MOD",
        ],
        "services": [
            "修理",
        ],
        "currencies": [
            "Roubles (₽)",
            "Euros (€)",
            "Bitcoin (₿)",
        ],
    },
    "Ragman": {
        "stampid": 828552630120349716,
        "fullname": "Abramyan Arshavir Sarkisivich",
        "location": "Interchange",
        "origin": "不明",
        "wares": [
            "衣類",
            "アーマー",
            "バックパック",
            "タクティカリグ",
            "ギア",
        ],
        "services": [
            "戦闘服",
        ],
        "currencies": [
            "Roubles (₽)",
        ],
    },
    "Jaeger": {
        "stampid": 828552628396621855,
        "fullname": "Kharitonov Ivan Egorovich",
        "location": "Woods",
        "origin": "不明",
        "wares": [
            "ソビエト連邦の武器",
            "弾薬",
            "弾倉",
            "武器MOD",
            "隠れ家素材",
        ],
        "services": [],
        "currencies": [
            "Roubles (₽)",
        ],
    },
    "Lightkeeper": {
        "stampid": 828552629248327690,
        "fullname": "Farit Akhmadullovich Genatulin",
        "location": "不明",
        "origin": "不明",
        "wares": [
            "不明",
        ],
        "services": [
            "不明",
        ],
        "currencies": ["不明"],
    },
}
BOSS_LIST = {
    "Reshala": {
        "stampid": 834774060029706240,
        "location": ["Customs"],
        "pawnchance": {"Customs": 38},
        "drops": ["TT pistol 7.62x25 TT Gold"],
        "followers": "4",
    },
    "Killa": {
        "stampid": 834774059430313984,
        "location": ["Interchange"],
        "pawnchance": {"Interchange": 38},
        "drops": [
            "RPK-16 5.45x39 light machine gun",
            "Maska 1Sch helmet (Killa)",
            "Maska 1Sch face shield (Killa)",
            "6B13 M assault armor (tan)",
            "Blackhawk! Commando Chest Harness (black)",
        ],
        "followers": "0",
    },
    "Glukhar": {
        "stampid": 834774058724753418,
        "location": ["Reserve"],
        "pawnchance": {"Reserve": 43},
        "drops": [
            "ASh-12 12.7x55 assault rifle",
        ],
        "followers": "6",
    },
    "Shturman": {
        "stampid": 834774058612555777,
        "location": ["Woods"],
        "pawnchance": {"Woods": 41},
        "drops": [
            "AK-105 5.45x39 assault rifle",
            "SVDS 7.62x54 Sniper rifle",
            "Red Rebel Ice pick",
        ],
        "followers": "2",
    },
    "Sanitar": {
        "stampid": 834774059522588742,
        "location": ["Shoreline"],
        "pawnchance": {"Shoreline": 35},
        "drops": ["Sanitar bag"],
        "followers": "2",
    },
    "CultistPriest": {
        "stampid": 834774056091910195,
        "location": ["Woods", "Shoreline", "Customs"],
        "pawnchance": {"Woods": 28, "Shoreline": 28, "Customs": 20},
        "drops": ["Sanitar bag"],
        "followers": "3-5",
    },
}


try:
    from local_settings import *
    LOCAL_HOST = False
except ImportError:
    APPLICATION_ID = os.getenv("APPLICATION_ID")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

class EscapeFromTarkovV2Bot(commands.Bot):
    def __init__(self, LOCAL_HOST, TRADER_LIST, BOSS_LIST):
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.all(),
            application_id=APPLICATION_ID
        )
        self.LOCAL_HOST = LOCAL_HOST
        self.TRADER_LIST = TRADER_LIST
        self.BOSS_LIST = BOSS_LIST
        self.develop_mode = False
        self.enrage_counter = 0
        self.help_embed = None
        self.safe_mode = False
        self.disability = False
        self.server_status = ServerStatusCode.SUCCESS
        self.executable_command = {
            name: False for name in ["map", "character", "task", "weapon", "ammo", ]
        }
        self.executable_command["reload"] = True

    async def send_deletable_message(self, intrtaction: discord.Integration, message: str=None, embed: discord.Embed=None, file: discord.File=None) -> None:
        """削除リアクションを付加したメッセージを送る関数

        Args:
            intrtaction (discord.Integration): discord.Integration
            message (str): 送信するメッセージ
        """
        if file:
            send_message = await intrtaction.channel.send(message, embed=embed, file=file)
        else:
            send_message = await intrtaction.channel.send(message, embed=embed)
        await send_message.add_reaction("❌")

    async def setup_hook(self) -> None:
        """スラッシュコマンド読み込み反映処理"""
        [await self.load_extension(cog) for cog in INITIAL_EXTENSIONS]
        await bot.tree.sync()

    async def on_ready(self) -> None:
        load_start_time = time.time()
        await self.data_reload(category="map")
        logging.info("Bot Application Start")
        if self.LOCAL_HOST: return
        channel = self.get_channel(ChannelCode.EXCEPTION_LOG)
        elapsed_time = time.time() - load_start_time
        start_time = dt.now(JST)
        embed = discord.Embed(
            title=f" DataLoadLog ({start_time.strftime('%Y%m%d%H%M%S')})",
            color=0xFF0000,
            timestamp=datetime.datetime.fromtimestamp(dt.now(JST).timestamp()),
        )
        embed.add_field(
            name="DataLoadTime",
            value=f"```{start_time.strftime('%Y/%m/%d %H:%M:%S')}```",
            inline=False,
        )
        embed.add_field(
            name="TimeRequired", value=f"```{elapsed_time}```", inline=False
        )
        embed.set_footer(text=f"{self.user.name}")
        await channel.send(embed=embed)
        self.change_status.start()
        self.server_status_checker.start()

    async def data_reload(self, category: str="all"):
        await self.set_status(
            status=discord.Status.idle,
            activity_name="最新データ読み込み中...",
        )
        if category=="all" or category=="map":
            try:
                self.map_list = get_map_list()
                self.maps_detail =  get_map_detail(self.map_list)
                self.executable_command["map"] = True
            except: pass
        if category=="all" or category=="character":
            try:
                self.boss_name = get_boss_name()
                self.trader_name = get_trader_name()
                self.executable_command["character"] = True
            except: pass
        if category=="all" or category=="task":
            try:
                self.get_tasks_name, self.get_tasks_detail = get_task_data()
                self.executable_command["task"] = True
            except: pass
        if category=="all" or category=="weapon":
            try:
                self.get_weapons_name, self.get_weapons_detail = get_weapons_data()
                self.executable_command["weapon"] = False
            except: pass
        if category=="all" or category=="ammo":
            try:
                self.ammo_list = get_ammo_data()
                self.executable_command["ammo"] = True
            except: pass
        self.update_timestamp = datetime.datetime.fromtimestamp(dt.now(JST).timestamp())
        await self.set_status()

    async def close(self):
        await super().close()
        await self.session.close()

    async def set_status(self, status: discord.Status=discord.Status.online, activity_name: str="Escape from Tarkov", activity_type: discord.ActivityType=discord.ActivityType.streaming) -> None:
        await self.change_presence(
            status=status,
            activity=discord.Activity(name=activity_name, type=activity_type),
        )

    @tasks.loop(minutes=1)
    async def change_status(self) -> None:
        if self.disability: return
        if self.LOCAL_HOST or self.develop_mode: return
        map = rand.choice(
            [
                key
                for key, val in self.maps_detail.items()
                if val["Duration"] != ""
            ]
        ).upper()
        await self.set_status(activity_name=f"マップ{map}")

    @tasks.loop(minutes=10)
    async def server_status_checker(self):
        (self.server_status, context) = get_server_status(previous_status=self.server_status)
        if context is None: return
        channel = self.get_channel(ChannelCode.EFT_ANNOUNCEMENTS)
        embed = discord.Embed(
            title="EscapeTarkovServerStatus",
            description=context.get("description"),
            color=context.get("color"),
            url="https://status.escapefromtarkov.com/",
            timestamp=datetime.datetime.fromtimestamp(dt.now(JST).timestamp())
        )
        await channel.send("@everyone", embed=embed)
        # await self.slash.commands["status"].invoke(channel)
        self.disability = context.get("code")
        await self.set_status(
            status=context.get("status"),
            activity_name=context.get("activity_name"),
        )

    async def on_interaction(self, interaction):
        if self.executable_command.get(interaction.command.binding.qualified_name.lower(), True): await interaction.response.defer()
        else:
            embed = discord.Embed(
                title="Wikiデータ読み込みエラー",
                color=0x808080,
                timestamp=self.update_timestamp,
            )
            embed.add_field(
                name=f"{interaction.command.binding.qualified_name}カテゴリのデータが読み込まれておりません。",
                value=f"{interaction.command.binding.qualified_name}カテゴリのデータが読み込まれておりません。",
            )
        await self.send_deletable_message(interaction, embed=embed)

    async def on_app_command_completion(self, interaction, command):
        if command.name!="help" and self.help_embed:
            await self.help_embed.delete()
            self.help_embed = None
        else:
            pass

    # 登録されているスラッシュコマンド以外の例外発生時発火
    async def on_error(self, event, *args, **kwargs):
        print(event)
        pass

    # 登録されているスラッシュコマンド以外の例外発生時発火
    async def on_command_error(self, ctx, error):
        print(ctx)
        pass

    # TODO リアクション反応時発火
    # async def on_reaction_add(self, reaction, user):
    #     if user.bot and self.develop_mode and reaction.message.channel.id==ChannelCode.README: return
    #     try:
    #         if len(self.hints[reaction.emoji].split(" ")) == 1:
    #             await self.slash.commands[self.hints[reaction.emoji]](
    #                 reaction.message.channel
    #             )
    #         else:
    #             if self.hintsEmbed:
    #                 await self.hintsEmbed.delete()
    #                 self.hintsEmbed = None
    #             await self.slash.commands[
    #                 self.hints[reaction.emoji].split(" ")[0]
    #             ].invoke(
    #                 reaction.message.channel,
    #                 self.hints[reaction.emoji].split(" ")[1:],
    #             )
    #     except:
    #         pass

    async def on_raw_reaction_add(self, payload):
        user = await self.fetch_user(payload.user_id)
        if self.develop_mode: return
        if user.bot: return
        try:
            channel = await self.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.emoji.name == "❌" and message.author.bot and message.channel.id != ChannelCode.README: await message.delete()
        except:
            pass

    # TODO on_slash_command_error
    async def on_slash_command_error(self, ctx, ex):
        if isinstance(ex, commands.CommandNotFound):
            hitCommands = []
            if ctx.command == "map":
                hitCommands += [map.lower() for map in self.mapData]
            elif ctx.command == "weapon":
                hitCommands += [weaponName.lower()
                                for weaponName in self.weaponsName]
            elif ctx.command == "ammo":
                hitCommands += [ammoData for ammoData in self.ammoData.keys()]
                hitCommands += [
                    ammo["Name"]
                    for ammoData in self.ammoData.values()
                    for ammo in ammoData
                ]
            elif ctx.command == "task":
                hitCommands += [taskName.lower() for taskName in self.taskName]
            # コマンドの予測変換
            self.hints = {
                self.emojiList[n]: hint
                for n, hint in enumerate(
                    [
                        command
                        for command in hitCommands
                        if difflib.SequenceMatcher(
                            None,
                            ctx.args[0].lower(),
                            self.command_prefix + command,
                        ).ratio()
                        >= 0.59
                    ][:10]
                )
            }
            if ctx.args[0].lower() in self.hints.values():
                self.hints = {"1️⃣": ctx.args[0].lower()}
            if len(self.hints) > 0:
                text = ""
                embed = discord.Embed(
                    title="Hint", description="もしかして以下のコマンドじゃね?", color=0xFF0000
                )
                fixHints = self.hints
                for emoji, hint in self.hints.items():
                    if hint in [map.lower() for map in self.mapData]:
                        fixHints[emoji] = f"map {hint}"
                    elif hint in [
                        weaponName.lower() for weaponName in self.weaponsName
                    ]:
                        fixHints[emoji] = f"weapon {hint}"
                    elif hint in [ammoData for ammoData in self.ammoData.keys()]:
                        fixHints[emoji] = f"ammo {hint}"
                    elif hint in [
                        ammo["Name"]
                        for ammoData in self.ammoData.values()
                        for ammo in ammoData
                    ]:
                        fixHints[emoji] = f"ammo {hint}"
                    elif hint in [task.lower() for task in self.taskName]:
                        fixHints[emoji] = f"task {hint}"
                    embed.add_field(
                        name=emoji, value=f"__`{prefix}{fixHints[emoji]}`__"
                    )
                self.hints = fixHints
                if len(self.hints) == 1:
                    if len(self.hints["1️⃣"].split(" ")) != 1:
                        await self.slash.commands[
                            self.hints["1️⃣"].split(" ")[0]
                        ].invoke(
                            ctx,
                            self.hints["1️⃣"].split(" ")[1:],
                        )
                    else:
                        await self.slash.commands[self.hints["1️⃣"]].invoke(
                            ctx,
                        )
                else:
                    embed.set_footer(text="これ以外に使えるコマンドは /help で確認できるよ!")
                    self.hintsEmbed = await ctx.send(embed=embed)
                    try:
                        for emoji in self.hints.keys():
                            await self.hintsEmbed.add_reaction(emoji)
                        await self.hintsEmbed.add_reaction("❌")
                    except:
                        pass
            else:
                text = f"入力されたコマンド {ctx.command} {ctx.args[0]} は見つからなかったよ...ごめんね。\n"
                text += f"これ以外に使えるコマンドは {self.command_prefix}help で確認できるよ!"
                await ctx.send(text)
        elif isinstance(ex, commands.ExtensionError):
            pass
        elif isinstance(ex, commands.MissingRole):
            pass
        else:
            # exception-log チャンネル
            channel = self.get_channel(846977129211101206)
            errorTime = dt.now(pytz.timezone("Asia/Tokyo"))
            embed = discord.Embed(
                title=f"ErrorLog ({errorTime.strftime('%Y%m%d%H%M%S')})",
                description=f"ご迷惑をおかけしております。コマンド実行中において例外処理が発生しました。\nこのエラーログは sai11121209 に送信されています。 {ctx.author.mention} バグを発見してくれてありがとう!",
                color=0xFF0000,
                timestamp=datetime.datetime.fromtimestamp(dt.now(JST).timestamp()),
            )
            embed.add_field(
                name="Time",
                value=f"```{errorTime.strftime('%Y/%m/%d %H:%M:%S')}```",
                inline=False,
            )
            embed.add_field(
                name="ServerId", value=f"```{ctx.guild.id}```", inline=False
            )
            embed.add_field(
                name="ServerName", value=f"```{ctx.guild.name}```", inline=False
            )
            embed.add_field(
                name="ChannelId", value=f"```{ctx.channel.id}```", inline=False
            )
            embed.add_field(
                name="ChannelName", value=f"```{ctx.channel.name}```", inline=False
            )
            embed.add_field(
                name="UserId", value=f"```{ctx.author.id}```", inline=False)
            embed.add_field(
                name="UserName", value=f"```{ctx.author.name}```", inline=False
            )
            embed.add_field(
                name="ErrorCommand", value=f"```{ctx.command}```", inline=False
            )
            embed.add_field(name="ErrorDetails",
                            value=f"```{ex}```", inline=False)
            embed.set_footer(text=f"{ctx.me.name}")
            await channel.send(embed=embed)
            if self.LOCAL_HOST == False:
                sendMessage = await ctx.send(embed=embed)
                await sendMessage.add_reaction("❌")

    async def on_message(self, message):
        if self.LOCAL_HOST: return
        # メッセージ送信者がBotだった場合は無視する
        if not message.content: return
        if message.author.bot:
            if message.channel.id!=ChannelCode.EFT_ANNOUNCEMENTS and message.author.id==self.application.id: return
            res = get_translate_text(message.content)
            if res["code"] == 200:
                text = "@everyone 多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n"
                text += res["text"]
                await message.channel.send(text)
            if "MSK" in message.content:
                channel = self.get_channel(ChannelCode.NOTIFICATION_GNERAL)
                text = "@everyone 重要なお知らせかもしれないからこっちにも貼っとくで\n"
                text += f"{message.content}\n\n"
                text += f"多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n{res['text']}"
                await channel.send(f"{text}{message.content}")

        if (
            self.develop_mode
            and message.author.id != AuthorCode.SAI11121209
            and not message.author.bot
            and self.command_prefix == message.content[0]
        ):
            await message.channel.send(get_enrage_message(self))

        elif "@everyone BOTの更新をしました!" == message.content:
            await self.slash.commands["patch"].invoke(message.channel)
        if self.command_prefix == message.content[0]:
            if self.safe_mode:
                await message.delete()
                embed = discord.Embed(
                    title="現在セーフモードで動作しているためコマンドを呼び出すことはできません。",
                    color=0xFF0000,
                )
                await message.channel.send(embed=embed)
            else:
                if not self.develop_mode:
                    await message.delete()
                elif message.content == f"{self.command_prefix}develop":
                    await message.delete()

bot = EscapeFromTarkovV2Bot(
    LOCAL_HOST=LOCAL_HOST,
    TRADER_LIST=TRADER_LIST,
    BOSS_LIST=BOSS_LIST,
)
bot.run(BOT_TOKEN)

print("END")