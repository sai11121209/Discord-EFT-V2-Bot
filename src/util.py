import json
from typing import Tuple
import requests as rq
from bs4 import BeautifulSoup
import discord
from const import ServerStatusCode, ServerStatusColorCode
from const import Url


def get_server_status(previous_status: int) -> Tuple[int, dict]:
    """現在のEscape from Tarkovサーバステータスを取得し、ステータス変化に応じたデータを返す。

    Args:
        previous_status (int): これまでのサーバステータス

    Returns:
        int: 現在のステータスコード
        dict: 現在のステータスに応じたデータ
    """
    response = get_requests_response("https://status.escapefromtarkov.com/api/global/status")
    now_status = json.loads(response.text)["status"]
    status_context = {
        # 正常
        ServerStatusCode.SUCCESS: {
            # 正常 → 正常
            ServerStatusCode.SUCCESS: None,
            # 正常 → 更新
            ServerStatusCode.UPDATE: {
                "code": 1,
                "status": discord.Status.dnd,
                "activity_name": "アップデート中",
                "color": ServerStatusColorCode.UPDATE,
                "description": "現在EscapeTarkovServerはアップデートのため停止しています。",
            },
            # 正常 → 接続不安定
            ServerStatusCode.WARNING: {
                "code": 2,
                "status": discord.Status.idle,
                "activity_name": "接続不安定",
                "color": ServerStatusColorCode.WARNING,
                "description": "現在EscapeTarkovServerへの接続が不安定な状態になっています。",
            },
            # 正常 → 障害
            ServerStatusCode.ERROR: {
                "code": 3,
                "status": discord.Status.idle,
                "activity_name": "障害発生中",
                "color": ServerStatusColorCode.ERROR,
                "description": "現在EscapeTarkovServerにおいて障害が発生しています。",
            },
        },
        # 更新
        ServerStatusCode.UPDATE: {
            # 更新 → 正常
            ServerStatusCode.SUCCESS: {
                "code": 0,
                "status": discord.Status.online,
                "activity_name": "Escape from Tarkov",
                "color": ServerStatusColorCode.SUCCESS,
                "description": "EscapeTarkovServerのアップデートが終了しサービスが再開しました。",
            },
            # 更新 → 更新
            ServerStatusCode.UPDATE: {
                "code": 1,
                "status": discord.Status.dnd,
                "activity_name": "アップデート中",
                "color": ServerStatusColorCode.UPDATE,
                "description": "現在EscapeTarkovServerはアップデートのため停止しています。",
            },
            # 更新 → 接続不安定
            ServerStatusCode.WARNING: {
                "code": 2,
                "status": discord.Status.idle,
                "activity_name": "接続不安定",
                "color": ServerStatusColorCode.WARNING,
                "description": "現在EscapeTarkovServerへの接続が不安定な状態になっています。",
            },
            # 更新 → 障害
            ServerStatusCode.ERROR: {
                "code": 3,
                "status": discord.Status.dnd,
                "activity_name": "障害発生中",
                "color": ServerStatusColorCode.ERROR,
                "description": "現在EscapeTarkovServerにおいて障害が発生しています。",
            },
        },
        # 接続不安定
        ServerStatusCode.WARNING: {
            # 接続不安定 → 正常
            ServerStatusCode.SUCCESS: {
                "code": 0,
                "status": discord.Status.online,
                "activity_name": "Escape from Tarkov",
                "color": ServerStatusColorCode.SUCCESS,
                "description": "EscapeTarkovServerにおいて発生していた障害は現在解消されました。",
            },
            # 接続不安定 → 更新
            ServerStatusCode.UPDATE: {
                "code": 1,
                "status": discord.Status.dnd,
                "activity_name": "アップデート中",
                "color": ServerStatusColorCode.UPDATE,
                "description": "現在EscapeTarkovServerにおいて発生していた障害は現在解消し、アップデートのため停止しています。",
            },
            # 接続不安定 → 接続不安定
            ServerStatusCode.WARNING: {
                "code": 2,
                "status": discord.Status.idle,
                "activity_name": "接続不安定",
                "color": ServerStatusColorCode.WARNING,
                "description": "現在EscapeTarkovServerへの接続が不安定な状態になっています。",
            },
            # 接続不安定 → 障害
            ServerStatusCode.ERROR: {
                "code": 3,
                "status": discord.Status.dnd,
                "activity_name": "障害発生中",
                "color": ServerStatusColorCode.ERROR,
                "description": "現在EscapeTarkovServerにおいて障害が発生しています。",
            },
        },
        # 障害
        ServerStatusCode.ERROR: {
            # 障害 → 正常
            ServerStatusCode.SUCCESS: {
                "code": 0,
                "status": discord.Status.online,
                "activity_name": "Escape from Tarkov",
                "color": ServerStatusColorCode.SUCCESS,
                "description": "EscapeTarkovServerにおいて発生していた障害は現在解消されました。",
            },
            # 障害 → 更新
            ServerStatusCode.UPDATE: {
                "code": 1,
                "status": discord.Status.dnd,
                "activity_name": "アップデート中",
                "color": ServerStatusColorCode.UPDATE,
                "description": "現在EscapeTarkovServerにおいて発生していた障害は現在解消し、アップデートのため停止しています。",
            },
            # 障害 → 接続不安定
            ServerStatusCode.WARNING: {
                "code": 2,
                "status": discord.Status.idle,
                "activity_name": "接続不安定",
                "color": ServerStatusColorCode.WARNING,
                "description": "現在EscapeTarkovServerにおいて発生していた障害は現在解消されましたが、接続が不安定な状態になっています。",
            },
            # 障害 → 障害
            ServerStatusCode.ERROR: {
                "code": 3,
                "status": discord.Status.dnd,
                "activity_name": "障害発生中",
                "color": ServerStatusColorCode.ERROR,
                "description": "現在EscapeTarkovServerにおいて障害が発生しています。",
            },
        }
    }
    return now_status, status_context[previous_status][now_status]

def get_enrage_message(bot: object) -> str:
    """開発モード中にコマンドを呼びだした際の処理
    怒りメッセージと怒りカウンターのインクリメントを同時に行います。

    Args:
        bot (object): EscapeFromTarkovV2Bot

    Returns:
        str: 怒りメッセージ
    """
    if bot.enrage_counter < 5: message = "機能改善会議しとるねん。話しかけんといて。"
    elif bot.enrage_counter < 10: message = "やめて。ください。"
    elif bot.enrage_counter < 15: message = "......"
    else: message = "嫌い"
    bot.enrage_counter += 1
    return message

def get_url(base_url: str, url: str) -> str:
    return base_url+url

def get_requests_response(base_url: str, url: str="") -> rq:
    return rq.get(get_url(base_url, url))

def get_beautiful_soup_object(response: rq, purse :str="lxml", class_name :str="wikitable") -> BeautifulSoup:
    soup = BeautifulSoup(response.text, purse)
    return soup.find(class_=class_name) if class_name else soup

def get_translate_text(text: str, source_language: str="en", target_language: str="ja") -> rq:
    return get_requests_response(Url.TRANSLATE_URL, f"?text={text}&source={source_language}&target={target_language}")