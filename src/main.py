import os
import logging
import time
import datetime
from datetime import datetime as dt
import discord
from discord.ext import tasks, commands
from const import ChannelCode, AuthorCode, ServerStatusCode, CommandCategory
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

COMMAND_PREFIX = "/"

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
    "cogs.weapon",
    "cogs.help",
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
# 新規コマンド追加時は必ずcommandListに追加
COMMAND_LIST = {
    "EFT公式サイト表示": ["TOP"],
    "日本EFTWiki表示": ["JAWIKI"],
    "海外EFTWiki表示": ["ENWIKI"],
    "マップ一覧表示": ["MAP"],
    # "各マップ情報表示": mapList,
    "武器一覧表示": ["WEAPON"],
    "各武器詳細表示": [],
    "弾薬性能表示": ["AMMO"],
    "フリーマーケット情報表示": ["MARKET"],
    "TarkovTools情報表示": ["TARKOVTOOLS"],
    "各アイテムフリーマーケット価格表示": [],
    "ディーラー一覧表示": ["DEALER"],
    "ボス一覧表示": ["BOSS"],
    "マップ抽選": ["RANDOMMAP"],
    "武器抽選": ["RANDOMWEAPON"],
    "早見表表示": ["CHART"],
    "アーマ早見表表示": ["ARMOR"],
    "ヘッドセット早見表": ["HEADSET"],
    "更新履歴表示": ["PATCH"],
    "現在時刻表示": ["NOW"],
    "ビットコイン価格表示": ["BTC"],
    "ソースコード表示": ["SOURCE"],
}
NOTIFICATION_INFORMATION = {}
# 上に追記していくこと
PATCH_NOTES = {
    "4.2:2022/01/28 16:00": [
        "マップ情報表示コマンド __`MAP`__ のReserveにおいて日本語翻訳マップを追加しました。",
    ],
    "4.1:2022/01/20 16:00": [
        "現在のユーロ、ドルのEFT為替レート表示コマンド _`RATE`_ を追加しました。",
        "ユーロからルーブルの値段を計算するコマンド _`RATE EURO`_ を追加しました。",
        "ドルからルーブルの値段を計算するコマンド _`RATE DOLLAR`_ を追加しました。",
        "弾薬性能表示コマンド __`AMMO`__ を呼び出した際に表示される弾薬の性能比較画像を12.12版に更新しました。",
    ],
    "4.0:2022/01/14 02:00": [
        "Discord SlashCommand の実装に伴う大幅仕様変更",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ において表示されるEmbedの表示方式を変更しました。",
        "__`ARMOR`__ __`HEADSET`__ __`ITEMVALUE`__ __`RECOVERY`__ __`TASKITEM`__ __`TASKTREE`__ __`LIGHTHOUSETASK`__ の7コマンドが早見表表示コマンド __`CHART`__ のサブコマンドとして組み込まれました。以降は __`CHART ARMOR`__ のように呼び出せるようになります。",
        "サーバステータス確認コマンド __`STATUS`__ の動作を安定化しました。",
        "武器抽選コマンド __`RANDOMWEAPON`__ マップ抽選コマンド __`RANDOMMAP`__ において発生していたバグの修正。",
        "一部処理の並列化による起動時間、応答時間の短縮。",
        "その他細かい修正",
    ],
    "3.7:2022/01/02 06:00": [
        "サーバステータス確認コマンドを __`STATUS`__ を実装しました。",
        "本BOTが5分置きににEscape from Tarkovサーバの状態を監視し、異常があった場合に通知してくれる機能を実装しました。",
        "その他細かい修正",
    ],
    "3.6:2021/11/25 20:00": [
        "弾薬性能表示コマンドにおいて __`AMMO 口径名`__ __`AMMO 弾薬名`__ を入力することで特定口径の弾薬や、弾薬の性能を見ることできるようになりました。",
        "その他細かい修正",
    ],
    "3.5:2021/11/09 13:00": [
        "海外Wikiのサイト仕様変更に伴う内部処理の修正",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ において表示されるAmmoChartのUIを変更しました。",
        "その他細かい修正",
    ],
    "3.4:2021/10/25 18:00": [
        "コマンド実行時呼び出しに使用したメッセージを消去するようになりました",
        "海外Wikiのサイト仕様変更に伴う内部処理の修正",
        "その他細かい修正",
    ],
    "3.3:2021/09/30 00:00": [
        "Among Us Botとの連携アップデート",
        "その他細かい修正",
    ],
    "3.2.1:2021/09/14 00:00": [
        "武器抽選コマンド __`RANDOMWEAPON`__ においてすべての処理が正常に実行されず複数回同様のコマンドが実行されてしまう問題の修正。WOLTERFEN#6329ありがとうございます。",
        "マップ抽選コマンド __`RANDOMMAP`__ においてすべての処理が正常に実行されず複数回同様のコマンドが実行されてしまう問題に加え、未実装マップも結果として出力されてしまっていた問題を修正。",
    ],
    "3.2:2021/08/19 13:00": [
        "ヘッドセット早見表コマンド __`HEADSET`__ を追加しました。",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ において投擲武器名を入力した際正常にレスポンスが行われなかった問題の修正。",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ にArmorクラス7が表示されてしまっていた問題の修正。",
    ],
    "3.1:2021/08/07 16:00": [
        "各武器詳細表示コマンド __`WEAPON 武器名`__ を入力した際に弾薬表も同時に表示されるようになりました。",
    ],
    "3.0.1:2021/07/24 01:00": [
        "各武器詳細表示コマンド __`WEAPON 武器名`__ を入力した際に発生していたエラー20210654072607を修正しました。WOLTERFEN#6329ありがとうございます。",
        "海外公式wikiのサイト更新に伴う仕様変更によりマップ、タスク、武器情報にアクセスできなかった問題を修正しました。",
        "各武器詳細表示コマンド __`WEAPON 武器名`__  、タスク詳細表示コマンド __`TASK {タスク名}`__ コマンドの補完処理における不具合を修正しました。",
        "ボイスチャット参加中(ボイスチャンネル参加者ロール付与中)に特定メッセージに対して返信を行なった際に返信先のユーザを自動的にメンションする様になりました。",
        "各種細かい不具合、動作改善。",
    ],
    "3.0:2021/07/12 23:30": [
        "コマンド呼び出し時の不具合を修正しました。",
        "タスク詳細表示コマンド __`TASK {タスク名}`__ の動作を一部変更しました。",
        "タスクツリー早見表コマンド __`TASKTREE`__ を追加しました。",
        "武器のロードアウトを組むことができるURLを呼び出すロードアウト作成コマンド __`LOADOUTS`__ を追加しました。",
        "タスク詳細表示コマンド __`TASK {タスク名}`__ を正式実装しました。",
        "タスク一覧コマンド __`TASK`__ とタスク詳細表示コマンド __`TASK {タスク名}`__ の2コマンドが仮追加されました。",
        "本サーバに送信されたメッセージに対して __`❌`__ リアクションが付与すると誰でもメッセージを消去できてしまう脆弱性の修正を行いました。",
        "__`notification-general`__ において発言した際の全体メンションの処理が変更されました。",
        "ボイスチャンネル使用中のユーザがテキストを書き込んだ際の処理が変更されました。",
        "各マップ情報表示コマンド __`MAP マップ名`__ 各武器詳細表示コマンド __`WEAPON 武器名`__ を入力した際に発生していたエラー20210617212538を修正しました。",
        "Discord Botフレームワーク環境への移行準に伴い各マップ情報表示コマンド ~~__`マップ名`__~~ から __`MAP マップ名`__ に変更されました。",
        "Discord Botフレームワーク環境への移行準に伴い各武器詳細表示コマンド ~~__`武器名`__~~ から __`WEAPON 武器名`__ に変更されました。",
        "ヘルプコマンド __`HELP`__ が呼び出された際にヘルプコマンドが消去されてしまう不具合を修正しました。",
        "全コマンドにおいて __`❌`__ リアクションが付与されクリックすることで表示されている実行結果が消去できるようになりました。",
    ],
    "3.0:2021/06/08 20:35": [
        "タスク使用アイテム早見表コマンド __`TASKITEM`__ で表示される画像が0.12.9.10532時点のものに更新されました。",
        "ヘルプコマンド __`HELP`__ を呼び出した後コマンドを入力し正常に呼び出された場合HELPコマンドの出力が消去されるようになりました。",
        "ボイスチャット入退室通知が入室時のみ通知されるように変更されました。",
        "マップ関連情報をBot起動時に動的取得するようになりました。",
        "未実装マップもマップ一覧表示コマンド __`MAP`__ で表示されるようになりました",
        "Discord Botフレームワーク環境への移行準備完了。現在試験的に新環境でプログラムを実行中です。",
        "例外処理発生時エラーログを出力するようになりました。",
        "コマンド補完性能向上。",
        "各種不具合の修正。",
    ],
    "2.3:2021/05/20 19:00": ["コマンド不一致時に表示されるヒントコマンドをリアクション選択から実行できるようになりました。"],
    "2.2.1:2021/05/20 14:00": ["各武器詳細表示コマンド __`武器名`__ の仕様を変更しました。"],
    "2.2:2021/05/15 18:00": [
        "出会いを目的としたフレンド募集を含む投稿を行った場合警告が送られる様になりました。",
    ],
    "2.1:2021/05/08 17:00": [
        "自動全体メンションに本文を含む様に変更されました。",
        "TarkovTools情報表示コマンド __`TARKOVTOOLS`__ を追加しました。",
        "以前から仕様変更予定にあった早見表表示、アーマ早見表表示コマンド __`CHART`__ __`ARMOR`__ の正式実装を行いました。",
        "早見表表示、アーマ早見表表示コマンド __`CHART`__ __`ARMOR`__ の正式実装、又TarkovTools情報表示コマンド __`TARKOVTOOLS`__ 追加に伴い弾薬性能表示コマンド __`AMMO`__の仕様が一部変更されました。",
    ],
    "2.0.1:2021/05/07 17:00": [
        "__`notification-general`__ において発言を行うと自動全体メンションをする様になりました。",
        "機能改善会議(メンテナンス)中にbotに話しかけると怒る様になりました。",
    ],
    "2.0:2021/05/06 18:00": [
        "武器一覧表示、各武器詳細表示コマンド __`WEAPON`__ __`武器名`__ の各種データを海外Wikiから取得する様に変更されました。",
        "武器一覧表示、各武器詳細表示、マップ一覧表示、ボス一覧表示コマンドのレスポンス最適化。",
        "ボイスチャンネル使用中のユーザがテキストチャンネルに書き込むとボイスチャンネル参加ユーザを自動メンションする様になりました。",
    ],
    "1.11:2021/04/22 22:10": [
        "武器抽選コマンド __`RANDOMWEAPON`__ 追加に伴いマップ抽選コマンド ~~__`RANDOM`__~~ から __`RANDOMMAP`__ に変更されました。",
        "ボス一覧表示コマンド __`BOSS`__ を追加しました。",
    ],
    "1.10.3:2021/04/20 18:35": [
        "マップ抽選コマンド __`RANDOM`__ で発生していたデータ型キャスト不具合の修正を行いました。",
        "タイムゾーン未指定による更新日時が正常に表示されていなかった問題の修正。",
    ],
    "1.10.2:2021/04/06 19:13": ["弾薬性能表示コマンド __`AMMO`__ の挙動が変更されました。"],
    "1.10.1:2021/04/06 03:20": [
        "機能改善に伴いタスク一覧表示コマンドが ~~__`TASK`__~~  から ディーラー一覧表示コマンドの __`DEALER`__ に統合されました。"
    ],
    "1.10:2021/04/02 12:00": ["アーマの早見表表示コマンド __`ARMOR`__ が仮実装されました。"],
    "1.9.1:2021/03/30 01:35": [
        "マップ一覧表示コマンド __`MAP`__ の挙動を大幅に改良しました。",
        "類似コマンドが存在し、かつ類似コマンドが1つの場合該当コマンドを実行するようになるようになりました。",
        "使用可能コマンド一覧表示コマンド __`HELP`__ を見やすいように表示方法改善しました。",
    ],
    "1.9:2021/03/23 18:00": [
        "各マップ情報表示コマンドの挙動を大幅に改良しました。",
        "海外公式wiki表示コマンド __`ENWIKI`__ 追加に伴い日本EFTWiki表示コマンドの呼び出しコマンドが 　~~__`WIKITOP`__~~ から __`JAWIKI`__ に変更されました。",
    ],
    "1.8.1:2021/03/22 23:00": ["内部処理エラーによる __`WEAPON`__ コマンドの修正"],
    "1.8:2021/03/19": [
        "ビットコイン価格表示コマンド __`BTC`__ を追加しました。",
        "メンテナンス関連のアナウンスがあった場合、テキストチャンネル __`escape-from-tarkov`__ に通知を送るようにしました。",
    ],
    "1.7:2021/03/17": ["現在時刻表示コマンド __`NOW`__ を追加しました。"],
    "1.6:2021/03/15": ["フリーマーケット情報表示コマンド __`MARKET`__ を追加しました。"],
    "1.5.2:2021/03/14": ["ボイスチャンネル開始、終了時の通知挙動の修正をしました。 ※最終修正"],
    "1.5.1:2021/03/11": ["ボイスチャンネル開始、終了時の通知挙動の修正をしました。"],
    "1.5:2021/03/09": ["BOTがボイスチャンネル開始時に通知をしてくれるようになりました。"],
    "1.4:2021/03/06": ["BOTが公式アナウンスを自動的に翻訳してくれるようになりました。"],
    "1.3.2.1:2021/03/04": ["BOTがよりフレンドリーな返答をするようになりました。"],
    "1.3.2:2021/02/25": ["早見表表示コマンドに2件早見表を追加しました。"],
    "1.3.1:2021/02/23": [f"最初の文字が __`{COMMAND_PREFIX}`__ 以外の文字の場合コマンドとして認識しないように修正。"],
    "1.3:2021/02/10": [
        "タスク一覧表示コマンド __`TASK`__ を追加しました。",
        "弾薬性能表示コマンド __`AMMO`__ を追加しました。",
    ],
    "1.2.2:2021/02/08": ["一部コマンドのレスポンス内容の変更を行いました。"],
    "1.2.1:2021/02/05": ["一部コマンドを除いたレスポンスの向上"],
    "1.2:2021/02/04": [
        "入力されたコマンドに近いコマンドを表示するヒント機能を追加しました。",
        "各武器名を入力することで入力された武器の詳細情報のみにアクセスできるようになりました。",
        "BOTのソースコードにアクセスできるコマンド __`SOURCE`__ を追加しました。",
    ],
    "1.1:2021/02/02": [
        "更新履歴表示コマンド __`PATCH`__ を追加しました。",
        "武器一覧表示コマンドの挙動を大幅に変更しました。",
        "早見表表示コマンドに料金表を追加しました。",
    ],
    "1.0:2021/01/30": ["早見表表示コマンド __`CHART`__ を追加しました。", "早見表コマンドにアイテム早見表を追加しました。"],
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
    def __init__(self, COMMAND_PREFIX, LOCAL_HOST, TRADER_LIST, BOSS_LIST, COMMAND_LIST, NOTIFICATION_INFORMATION, PATCH_NOTES):
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=discord.Intents.all(),
            application_id=APPLICATION_ID
        )
        self.LOCAL_HOST = LOCAL_HOST
        self.TRADER_LIST = TRADER_LIST
        self.BOSS_LIST = BOSS_LIST
        self.COMMAND_LIST=COMMAND_LIST,
        self.NOTIFICATION_INFORMATION=NOTIFICATION_INFORMATION,
        self.PATCH_NOTES=PATCH_NOTES
        self.develop_mode = False
        self.enrage_counter = 0
        self.help_embed = None
        self.safe_mode = False
        self.disability = False
        self.server_status = ServerStatusCode.SUCCESS
        self.executable_command = {
            name: False for name in CommandCategory.COMMAND_CATEGORY_MAP.keys()
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
                self.ammo_list = get_ammo_data()
                self.executable_command["weapon"] = True
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

    @tasks.loop(minutes=10)
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

    @tasks.loop(minutes=1)
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
    COMMAND_PREFIX=COMMAND_PREFIX,
    LOCAL_HOST=LOCAL_HOST,
    TRADER_LIST=TRADER_LIST,
    BOSS_LIST=BOSS_LIST,
    COMMAND_LIST=COMMAND_LIST,
    NOTIFICATION_INFORMATION=NOTIFICATION_INFORMATION,
    PATCH_NOTES=PATCH_NOTES
)
bot.run(BOT_TOKEN)