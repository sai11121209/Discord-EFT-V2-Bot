import os
import logging
import time
import datetime
from datetime import datetime as dt
import discord
from discord.ext import tasks, commands
from const import Url, ChannelCode, AuthorCode, ServerStatusCode, CommandCategory, CommandCategory
from cogs.button import Button, DeleteButton
from cogs.select_menu import SelectMenu
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
NOTIFICATION_INFORMATION = {
    "6.0": [
        "OpenAIのサードパーティーライブラリを使用したAIチャットボットコマンド _`AICHAT`_ を追加予定。",
        "OpenAIのサードパーティーライブラリを使用したAI画像生成コマンド _`AIIMG`_ を追加予定。",
    ]
}
# 上に追記していくこと
PATCH_NOTES = {
    "5.0:2023/01/20 00:00": [
        "コードのリプレイス、リファクタリングを行いました。",
        "ランタイムをPython3.8からPython3.11に移行、これによりプログラム全体の処理速度が向上いたします。",
        "discord.py v2.xに対応。これにより柔軟に新機能を追加することが可能になります。",
        "プログラム再起動を行わず最新のwikiデータを取得するコマンド _`RELOAD`_ を追加しました。",
        "ヘルプコマンド _`HELP`_ において試験的に埋め込みメッセージのページングを行うようにしました。",
        "一部コマンドの埋め込みメッセージを一括で送信することでレスポンスの速度の改善を行いました。",
        "一部弾薬(5.56x45mm NATO、 9x18mm Makarov)などにおいて弾薬表が表示出来ないバグの修正。",
        "EFTゲームサーバの死活監視機能が動作してしていなかったバグの修正。",
        "「アプリケーションが応答しませんでした」と表示されるコマンド実行時間オーバーエラーの解消。",
        "ネットワークトラフィックの最適化を行いました。",
        "埋め込みメッセージのUI改善。",
        "全体的な処理の安定化、処理の高速化、その他細かいバグの修正。",
    ],
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
    LOCAL_HOST = True
except ImportError:
    APPLICATION_ID = os.getenv("APPLICATION_ID")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    LOCAL_HOST = False

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
        self.COMMAND_LIST=COMMAND_LIST
        self.NOTIFICATION_INFORMATION=NOTIFICATION_INFORMATION
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

    async def send_deletable_message(self, integration: discord.Integration, message: str=None, embed: discord.Embed=None, embeds: list=None, file: discord.File=None, view:discord.ui.View=None) -> None:
        """削除リアクションを付加したメッセージを送る関数

        Args:
            integration (discord.Integration): discord.Integration
            message (str): 送信するメッセージ
        """
        # 空の場合送信しない
        if message is None and embed is None and embeds is None and file is None and view is None: return
        view = view if view else discord.ui.View()
        view.add_item(DeleteButton())
        if embeds:
            N = 4
            send_messages = []
            for i in range(0, len(embeds), N):
                send_message = await integration.followup.send(message, embeds=embeds[i:i+N], file=file, view=view) if file and bool([embed.image.url.split("//")[-1] for embed in embeds[i:i+N] if embed.image.url.split("//")[-1]==file.filename]) else await integration.followup.send(message, embeds=embeds[i:i+N], view=view)
                send_messages.append(send_message)
            return send_messages
        else:
            if file:
                send_message = await integration.followup.send(message, embed=embed, file=file, view=view)
            else:
                send_message = await integration.followup.send(message, embed=embed, view=view)
            return send_message

    def create_base_embed(self, title:str="Escape from Tarkov Bot", description:str="", url:str=None, color:int=0x2ECC69, timestamp:datetime=None, thumbnail:str="", author_name:str="Escape from Tarkov Bot", author_url:str="https://github.com/sai11121209/Discord-EFT-V2-Bot", author_icon:str=None, footer:str="Source: The Official Escape from Tarkov Wiki 最終更新")->discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            url=url if url else Url.EN_WIKI,
            timestamp= timestamp if timestamp else self.update_timestamp
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_author(
            name=author_name,
            url=author_url,
            icon_url=author_icon if author_icon else self.user.avatar.url,
        )
        embed.set_footer(text=footer)
        return embed

    async def setup_hook(self) -> None:
        """スラッシュコマンド読み込み反映処理"""
        [await self.load_extension(cog) for cog in INITIAL_EXTENSIONS]
        # await bot.tree.sync()

    async def on_ready(self) -> None:
        load_start_time = time.time()
        await self.data_reload(category="all")
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
        logging.info("Bot Application Start")

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
                self.tasks_name, self.tasks_detail = get_task_data()
                self.executable_command["task"] = True
            except: pass
        if category=="all" or category=="weapon":
            try:
                self.weapons_name, self.weapons_detail = get_weapons_data()
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
        embed = self.create_base_embed(
            title="EscapeTarkovServerStatus",
            description=context.get("description"),
            color=context.get("color"),
            url="https://status.escapefromtarkov.com/",
        )
        await channel.send("@everyone", embed=embed)
        # await self.slash.commands["status"].invoke(channel)
        self.disability = context.get("code")
        await self.set_status(
            status=context.get("status"),
            activity_name=context.get("activity_name"),
        )

    async def on_interaction(self, interaction):
        # 過去に生成したのボタンが押された場合
        if not interaction.command: return await interaction.message.delete()
        await interaction.response.defer(thinking=True)
        if self.executable_command.get(interaction.command.binding.qualified_name.lower(), True): return
        else:
            embed = self.create_base_embed(
                title="Wikiデータ読み込みエラー",
                color=discord.Color.red(),
                footer=""
            )
            embed.add_field(
                name=f"{interaction.command.binding.qualified_name}コマンド呼び出し失敗",
                value=f"{CommandCategory.COMMAND_CATEGORY_MAP.get(interaction.command.binding.qualified_name.lower())}カテゴリのデータが読み込まれておりません。",
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
        pass

    # 登録されているスラッシュコマンド以外の例外発生時発火
    # async def on_command_error(self, integration, error):
    #     print(integration)
    #     pass

    # TODO リアクション反応時発火
    async def on_reaction_add(self, reaction, user):
        if user.bot or self.develop_mode or reaction.message.channel.id==ChannelCode.README: return
        try:
            if len(self.hints[reaction.emoji].split(" ")) == 1:
                await self.slash.commands[self.hints[reaction.emoji]](
                    reaction.message.channel
                )
            else:
                if self.hints_embed:
                    await self.hints_embed.delete()
                    self.hints_embed = None
                await self.slash.commands[
                    self.hints[reaction.emoji].split(" ")[0]
                ].invoke(
                    reaction.message.channel,
                    self.hints[reaction.emoji].split(" ")[1:],
                )
        except:
            pass

    async def on_command_error(self, integration, error):
        if isinstance(error, commands.CommandNotFound):
            hit_commands = []
            if integration.command.name == "map":
                hit_commands += [map.lower() for map in self.maps_detail]
            elif integration.command.name == "weapon":
                hit_commands += [weapon_name.lower()
                                for weapon_name in self.weapons_name]
            elif integration.command.name == "ammo":
                hit_commands += [ammo for ammo in self.ammo_list.keys()]
                hit_commands += [
                    a["Name"]
                    for ammo in self.ammo_list.values()
                    for a in ammo
                ]
            elif integration.command.name == "task":
                hit_commands += [task_name.lower() for task_name in self.tasks_name]
            # コマンドの予測変換
            self.hints = [
                hint
                for hint in [
                    command
                    for command in hit_commands
                    if difflib.SequenceMatcher(
                        None,
                        integration.namespace.name.lower(),
                        self.command_prefix + command,
                    ).ratio()
                    >= 0.59
                ]
            ]
            if integration.namespace.name.lower() in self.hints:
                self.hints = [integration.namespace.name.lower()]
            if len(self.hints) > 0:
                embed = self.create_base_embed(
                    title="Hint",
                    description="もしかして以下のコマンドじゃね?",
                    color=0xFF0000,
                    footer="これ以外に使えるコマンドは /help で確認できるよ!",
                )
                fix_hints = self.hints
                view = discord.ui.View()
                select_menu = []
                for hint in self.hints:
                    embed.add_field(
                        name=hint, value=f"__`{self.command_prefix}{integration.command.name} {hint}`__"
                    )
                self.hints = fix_hints
                if len(self.hints) == 1:
                    command = self.tree.get_command(integration.command.name)
                    cogs = self.cogs.get(integration.command.name.capitalize())
                    await integration.response.defer(thinking=True)
                    await command.callback(cogs, integration,  self.hints[0])
                else:
                    try:
                        for command in self.hints:
                            select_menu.append(command)
                    except:
                        pass
                    view.add_item(SelectMenu(integration.command.name, select_menu, "実行したいコマンド選んでください"))
                    self.hints_embed = await self.send_deletable_message(integration, embed=embed, view=view)
            else:
                message = f"入力されたコマンド {integration.command.name} {integration.namespace.name.lower()} は見つからなかったよ...ごめんね。\n"
                message += f"これ以外に使えるコマンドは {self.command_prefix}help で確認できるよ!"
                await self.send_deletable_message(integration, message)
        elif isinstance(error, commands.ExtensionError):
            pass
        elif isinstance(error, commands.MissingRole):
            pass
        else:
            # exception-log チャンネル
            channel = self.get_channel(ChannelCode.EXCEPTION_LOG)
            error_time = dt.now(JST)
            embed = self.create_base_embed(
                title=f"ErrorLog ({error_time.strftime('%Y%m%d%H%M%S')})",
                description=f"ご迷惑をおかけしております。コマンド実行中において例外処理が発生しました。\nこのエラーログは {self.application.owner.mention} に送信されています。 {integration.user.mention} バグを発見してくれてありがとう!",
                color=0xFF0000,
                footer="",
            )
            embed.add_field(
                name="Time",
                value=f"```{error_time.strftime('%Y/%m/%d %H:%M:%S')}```",
                inline=False,
            )
            embed.add_field(
                name="ServerId", value=f"```{integration.guild.id}```", inline=False
            )
            embed.add_field(
                name="ServerName", value=f"```{integration.guild.name}```", inline=False
            )
            embed.add_field(
                name="ChannelId", value=f"```{integration.channel.id}```", inline=False
            )
            embed.add_field(
                name="ChannelName", value=f"```{integration.channel.name}```", inline=False
            )
            embed.add_field(
                name="UserId", value=f"```{integration.user.id}```", inline=False)
            embed.add_field(
                name="UserName", value=f"```{integration.user.name}```", inline=False
            )
            embed.add_field(
                name="ErrorCommand", value=f"```{integration.command.name}```", inline=False
            )
            embed.add_field(name="ErrorCommandOption",
                            value=f"```{error}```" if error.args else "```None```", inline=False)
            await channel.send(embed=embed)
            if self.LOCAL_HOST == False:
                await self.send_deletable_message(integration, embed=embed)

    async def on_message(self, message):
        if self.LOCAL_HOST or not message.content: return
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            if message.channel.id != ChannelCode.EFT_ANNOUNCEMENTS or message.author.id == self.application.id: return
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
    PATCH_NOTES=PATCH_NOTES,
)
bot.run(BOT_TOKEN)