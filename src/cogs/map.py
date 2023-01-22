import discord
from discord import app_commands, ButtonStyle
from discord.ext import commands
from discord.app_commands import Choice
from util import get_requests_response, get_beautiful_soup_object, get_translate_text
from const import Url
from cogs.button import Button
from cogs.select_menu import SelectMenu


class Map(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="map", description="マップ一覧表示")
    @app_commands.describe(name="マップ名を指定します。")
    @app_commands.choices(
        name = [
            Choice(name="CUSTOMS", value="CUSTOMS"),
            Choice(name="FACTORY", value="FACTORY"),
            Choice(name="INTERCHANGE", value="INTERCHANGE"),
            Choice(name="LIGHTHOUSE", value="LIGHTHOUSE"),
            Choice(name="RESERVE", value="RESERVE"),
            Choice(name="SHORELINE", value="SHORELINE"),
            Choice(name="THELAB", value="THELAB"),
            Choice(name="WOODS", value="WOODS"),
            Choice(name="ARENA", value="ARENA"),
            Choice(name="PRIVATESECTOR", value="PRIVATESECTOR"),
            Choice(name="STREETSOFTARKOV", value="STREETSOFTARKOV"),
            Choice(name="SUBURBS", value="SUBURBS"),
            Choice(name="TERMINAL", value="TERMINAL"),
            Choice(name="TOWN", value="TOWN"),
        ]
    )
    async def map(self, integration:discord.Integration, name:str=None) -> None:
        release_text = ""
        released_color = 0x2ECC69
        unreleased_color = 0xFF0000
        if name:
            text = f"{name} MAP INFORMATION\n"
            # LABORATORYのみ海外公式wikiのURLがThe_Labとなるため例外
            message = ""
            name = name.upper()
            features_text = ""
            for key, value in self.bot.maps_detail[name.upper()].items():
                if key == "Banner":
                    pass
                elif key == "Name":
                    pass
                elif key == "MapUrl":
                    pass
                elif key == "Description":
                    res = get_translate_text(value).json()
                    if res["code"] == 200:
                        tranceText = res["text"]
                        features_text = f"\n**特徴**:"
                        features_text += f"\n> {value}"
                        features_text += f"\n\n> {tranceText}"
                        features_text += "\n> Google翻訳"
                elif key == "Duration":
                    message += f"**時間制限**: "
                    try:
                        message += f"__昼間:{value['Day']}分__ __夜間:{value['Night']}分__"
                    except:
                        message += f"__{value}分__"
                    message += "\n"
                elif key == "Players":
                    message += f"**人数**: "
                    try:
                        message += f"__昼間:{value['Day']}人__ __夜間:{value['Night']}人__"
                    except:
                        message += f"__{value}人__"
                    message += "\n"
                elif key == "Enemy types":
                    message += f"**出現敵兵**: "
                    for v in value:
                        if v == "ScavRaiders":
                            message += f"__[{v}]({Url.EN_WIKI}Scav_Raiders)__ "
                        else:
                            message += f"__[{v}]({Url.EN_WIKI}{v})__ "
                    message += "\n"
                elif key == "Release state":
                    if value == "Released":
                        color = released_color
                    else:
                        release_text = "**未実装マップ**\n\n"
                        color = unreleased_color

            embed = self.bot.create_base_embed(
                title=text,
                description=release_text + message + features_text,
                color=color,
                url=f"{Url.EN_WIKI}{self.bot.maps_detail[name]['MapUrl']}",
            )
            embed.set_image(url=self.bot.maps_detail[name]["Banner"])
            await self.bot.send_deletable_message(integration, embed=embed)
            map_data = self.bot.maps_detail[name]["Images"]
            n = 1
            embeds = []
            file = None
            if name == "RESERVE":
                file = discord.File(f"../imgs/map/reserve/1.jpg")
                embed = self.bot.create_base_embed(
                    title=f"{name} MAP",
                    color=color,
                    url=f"{Url.EN_WIKI}{self.bot.maps_detail[name]['MapUrl']}",
                )
                embed.set_image(url=f"attachment://1.jpg")
                embeds.append(embed)
            for key, value in map_data.items():
                embed = self.bot.create_base_embed(
                    title=f"{name} MAP",
                    color=color,
                    url=f"{Url.EN_WIKI}{self.bot.maps_detail[name]['MapUrl']}",
                )
                embed.set_image(url=value)
                embeds.append(embed)
                n += 1
            await self.bot.send_deletable_message(integration, embeds=embeds, file=file)
        else:
            embed = self.bot.create_base_embed(
                title="MAP LIST",
                url=f"{Url.EN_WIKI}Map",
                color=0x2ECC69,
                thumbnail="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/4/43/Map.png/revision/latest?cb=20200619104902&format=original",
                footer=f"{self.bot.command_prefix}マップ名で各マップの地形情報を表示できるよー。 例: {self.bot.command_prefix}reserve \n Source: The Official Escape from Tarkov Wiki 最終更新"
            )
            view = discord.ui.View()
            select_menu = []
            for map, values in self.bot.maps_detail.items():
                text = ""
                for key, value in values.items():
                    if key == "Duration":
                        text += f"**時間制限**: "
                        try:
                            text += f"__昼間:{value['Day']}分__ __夜間:{value['Night']}分__"
                        except:
                            text += f"__{value}分__"
                        text += "\n"
                    elif key == "difficulty":
                        text += f"**難易度**: __{value}__"
                        text += "\n"
                    elif key == "Players":
                        text += f"**人数**: "
                        try:
                            text += f"__昼間:{value['Day']}人__ __夜間:{value['Night']}人__"
                        except:
                            text += f"__{value}人__"
                        text += "\n"
                    elif key == "Enemies":
                        text += f"**出現敵兵**: "
                        for v in value:
                            if v == "ScavRaiders":
                                text += f"__[{v}]({Url.EN_WIKI}Scav_Raiders)__ "
                            else:
                                text += f"__[{v}]({Url.EN_WIKI}{v})__ "
                        text += "\n"
                text += f"**詳細情報**: __[JA]({Url.JA_WIKI}{map})__ / __[EN]({Url.EN_WIKI}{self.bot.maps_detail[map]['MapUrl']})__\n"
                select_menu.append(values["Name"].upper())
                if values.get("Release state", "Released") == "Released":
                    embed.add_field(name=values["Name"].upper(), value=text)
                else:
                    embed.add_field(name=map, value=f"~~{text}~~")
            view.add_item(SelectMenu(integration.command.name, select_menu, "地図を出力したいマップを選んでください"))
            await self.bot.send_deletable_message(integration, embed=embed, view=view)

# マップ画像取得
def GetMapImage(map_name):
    map_images = {}
    res = get_requests_response(Url.EN_WIKI, map_name)
    soup = get_beautiful_soup_object(res, class_="mw-parser-output")
    # Map情報以外のimgタグを除去
    for s in soup.find_all("table"):
        s.decompose()
    soup.find("center").decompose()
    try:
        soup.find("div", {"class": "thumb"}).decompose()
    except:
        pass
    # Map情報の全imgタグを取得
    images = soup.find_all("img")
    for image in images:
        if (
            # customs: "FullScreenMapIcon.png"
            image["alt"] != "FullScreenMapIcon.png"
            # interchange: "The Power Switch"
            and image["alt"] != "The Power Switch"
            # laboratory: "TheLab-Insurance-Messages-01.PNG"
            and image["alt"] != "TheLab-Insurance-Messages-01.PNG"
            and image["alt"] != ""
        ):
            # 参照画像サイズを800px -> オリジナル画像サイズに変換
            map_images[image["alt"]] = (
                image["src"].replace("/scale-to-width-down/800", "")
                + "&format=original"
            )
    return map_images

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Map(bot))
