class Url:
    EFT_HP = "https://www.escapefromtarkov.com/"
    JA_WIKI = "https://wikiwiki.jp/eft/"
    EN_WIKI = "https://escapefromtarkov.fandom.com/wiki/"
    MARKET = "https://tarkov-market.com/item/"
    EFT_TOOL = "https://tarkov-tools.com/"
    TRANSLATE_URL = "https://script.google.com/macros/s/AKfycbxvCS-29LVgrm9-cSynGl19QUIB7jTpzuvFqflus_P0BJtXX80ahLazltfm2rbMGVVs/exec"
    SERVER_STATUS_STATUS = "https://status.escapefromtarkov.com/api/global/status",
    SERVER_STATUS_SERVICE = "https://status.escapefromtarkov.com/api/services",
    SERVER_STATUS_DATA_CENTER = "https://status.escapefromtarkov.com/api/datacenter/list",
    SERVER_STATUS_INFORMATION = "https://status.escapefromtarkov.com/api/message/list",

    SERVER_STATUS_MAP = {
        "status": "https://status.escapefromtarkov.com/api/global/status",
        "service": "https://status.escapefromtarkov.com/api/services",
        "datacenter": "https://status.escapefromtarkov.com/api/datacenter/list",
        "information": "https://status.escapefromtarkov.com/api/message/list",
    }

# チャンネルコード
class ChannelCode:
    # 開発用 exception-log チャンネル
    EXCEPTION_LOG = 1063454659748044863
    # 本番用 exception-log チャンネル
    # EXCEPTION_LOG = 848999028658405406

    # 開発用 announcements-log チャンネル
    EFT_ANNOUNCEMENTS = 1063454659748044863
    # 本番用 eft-announcements チャンネル
    # EFT_ANNOUNCEMENTS = 811566006132408340

    # 開発用 readme チャンネル
    README = 1063454659748044863
    # 本番用 readme チャンネル
    # README =  890461420330819586

    # 開発用 notification-general チャンネル
    NOTIFICATION_GNERAL = 1063454659748044863
    # 本番用 notification-general チャンネル
    # NOTIFICATION_GNERAL =  839769626585333761

    # 開発用 eft-announcements チャンネル
    EFT_ANNOUNCEMENTS = 1063454659748044863
    # 本番用 eft-announcements チャンネル
    # EFT_ANNOUNCEMENTS = 811566006132408340

class AuthorCode:
    SAI11121209 = 279995095124803595

class CommandCategory:
    MAP = "map"
    CHARACTER = "character"
    TASK = "task"
    WEAPON = "weapon"
    AMMO = "ammo"
    ALL = "all"

    COMMAND_CATEGORY_MAP = {
        "map": "マップ",
        "character": "キャラクター(トレーダー・ボス)",
        "task": "タスク",
        "weapon": "武器",
        "ammo": "弾薬",
        "all": "全て",
    }

class ServerStatusCode:
    SUCCESS = 0
    UPDATE = 1
    WARNING = 2
    ERROR = 3
    SERVER_STATUS_CODE_MAP = {"0": "正常", "1": "更新", "2": "接続不安定", "3": "障害"}

class ServerStatusColorCode:
    SUCCESS = 0x70B035
    UPDATE = 0x90C1EB
    WARNING = 0xCA8A00
    ERROR = 0xD42929

    SERVER_STATUS_COLOR_CODE_MAP = {"0": 0x70B035, "1": 0x90C1EB, "2": 0xCA8A00, "3": 0xD42929}