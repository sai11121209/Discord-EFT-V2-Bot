import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import numpy as np
from matplotlib import pyplot as plt
from const import Url
from util import get_url, get_translate_text


class Weapon(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def ammunition_figure_generation(self, ammo_data, caliber):
        try:
            x, y, name = [], [], []
            for ammunition in ammo_data[caliber]:
                name.append(ammunition["Name"])
                x.append(int(ammunition["Damage"]))
                y.append(int(ammunition["Penetration Power"]))
            xmin, xmax = 0, max(x) + 10
            hlines_list = np.arange(10, 61, 10)
            for x_, y_, name in zip(x, y, name):
                plt.plot(x_, y_, "o")
                plt.annotate(name.split(" ", 1)[1], xy=(x_, y_), color="white")
            plt.hlines(hlines_list, xmin, xmax, linestyle="dashed")
            for n, hline in enumerate(hlines_list):
                if hline < max(y) + 10:
                    plt.text(
                        max(x) + 10,
                        hline + 0.5,
                        f"ARMOR CLASS {n+1}",
                        size=10,
                        horizontalalignment="right",
                        color="green",
                    )
            plt.xlim(min(x) - 10, max(x) + 10)
            plt.ylim(0, max(y) + 10)
            plt.xlabel("DAMAGE")
            plt.ylabel("PENETRATION")
            plt.title(f"{caliber} Ammo Chart")
            plt.grid()
            ax = plt.gca()
            ax.set_facecolor("black")
            plt.savefig("ammo.png", bbox_inches="tight", pad_inches=0.05)
            plt.close()
            self.ammo_chart_check = True
            self.file = discord.File("ammo.png")
        except:
            pass

    @app_commands.command(name="weapon", description="武器一覧表示")
    @app_commands.describe(name="武器名を指定します。")
    async def weapon(self, intrtaction: discord.Integration, name: str=None) -> None:
        self.ammo_chart_check = False
        try:
            if name:
                if type(name) == list:
                    name = name[0]
                info_str = ""
                fix_text = name.upper().replace(" ", "")
                weapon_data = [
                    value
                    for values in self.bot.get_weapons_detail.values()
                    for value in values
                    if value["名前"].upper().replace(" ", "") == fix_text
                ][0]
                for col_name, value in weapon_data.items():
                    if col_name in [
                        "名前",
                        "weaponUrl",
                        "typeUrl",
                        "imageUrl",
                        "cartridgeUrl",
                        "soldByUrl",
                    ]:
                        pass
                    elif weapon_data[col_name] == "":
                        pass
                    elif col_name == "種類":
                        info_str += f"\n**{col_name.capitalize()}**: __[{weapon_data[col_name]}]({Url.EN_WIKI}{weapon_data['typeUrl']})__"
                    elif col_name == "口径":
                        info_str += f"\n**{col_name.capitalize()}**: __[{weapon_data[col_name]}]({Url.EN_WIKI}{weapon_data['cartridgeUrl']})__"
                    elif col_name == "発射機構":
                        info_str += f"\n**{col_name.capitalize()}**:"
                        for firingMode in weapon_data[col_name]:
                            info_str += f"\n・__{firingMode}__"
                    elif col_name == "販売元":
                        info_str += f"\n**{col_name.capitalize()}**: __[{weapon_data[col_name]}]({Url.EN_WIKI}{weapon_data['soldByUrl']})__"
                    elif col_name == "詳細":
                        res = get_translate_text(weapon_data[col_name]).json()
                        if res["code"] == 200:
                            text = res["text"]
                        info_str += f"\n**{col_name}**:"
                        info_str += f"\n> {weapon_data[col_name]}"
                        info_str += f"\n> {text}"
                        info_str += "> Google翻訳"
                    elif col_name == "使用可能弾薬":
                        info_str += f"\n**{col_name.capitalize()}**:"
                        for ammunition in weapon_data[col_name]:
                            info_str += f"\n・__[{ammunition}]({Url.EN_WIKI}{ammunition.replace(' ','_')})__"
                        self.ammunition_figure_generation(
                            self.bot.ammo_list, weapon_data["口径"]
                        )
                    elif col_name == "リコイル":
                        info_str += f"\n**{col_name.capitalize()}**:"
                        for key, value in weapon_data[col_name].items():
                            info_str += f"\n・**{key}**: __{value}__"
                    else:
                        info_str += (
                            f"\n**{col_name.capitalize()}**: __{weapon_data[col_name]}__"
                        )
                embed = discord.Embed(
                    title=weapon_data["名前"],
                    url=get_url(Url.EN_WIKI, weapon_data['weaponUrl']),
                    description=info_str,
                    timestamp=self.bot.update_timestamp,
                )
                embed.set_footer(
                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                )
                embed.set_thumbnail(url=weapon_data["imageUrl"])
                if self.ammo_chart_check:
                    embed.set_image(url="attachment://ammo.png")
                    await self.bot.send_deletable_message(intrtaction, embed=embed, file=self.file)
                    os.remove("ammo.png")

            else:
                embeds = []
                for n, (index, values) in enumerate(self.bot.get_weapons_detail.items()):
                    embed = discord.Embed(
                        title=f"武器一覧({n+1}/{len(self.bot.get_weapons_detail)})",
                        url=get_url(Url.EN_WIKI, "Weapons"),
                        timestamp=self.bot.update_timestamp,
                    )
                    embed.add_field(
                        name=f"{index}",
                        value=f"[{index} Wikiリンク]({Url.EN_WIKI}Weapons#{index.replace(' ', '_')})",
                        inline=False,
                    )
                    for value in values:
                        embed.add_field(
                            name=value["名前"],
                            value=f"[海外Wikiリンク]({Url.EN_WIKI}{value['weaponUrl']})",
                            inline=False,
                        )
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    embeds.append(embed)
                for embed in embeds:
                    await self.bot.send_deletable_message(intrtaction, embed=embed)
        except:
            # TODO　エラー処理
            pass
            # await self.bot.on_slash_command_error(
            #     ctx, commands.CommandNotFound("weapon")
            # )

    @app_commands.command(name="ammo", description="弾薬性能表示")
    @app_commands.describe(name="弾薬名を指定します。")
    @app_commands.choices(
        name = [
            Choice(name="7.62x25mm Tokarev", value="7.62x25mm Tokarev"),
            Choice(name="9x18mm Makarov", value="9x18mm Makarov"),
            Choice(name="9x19mm Parabellum", value="9x19mm Parabellum"),
            Choice(name="9x21mm Gyurza", value="9x21mm Gyurza"),
            Choice(name=".357 Magnum", value=".357 Magnum"),
            Choice(name=".45 ACP", value=".45 ACP"),
            Choice(name="4.6x30mm HK", value="4.6x30mm HK"),
            Choice(name="5.7x28mm FN", value="5.7x28mm FN"),
            Choice(name="5.45x39mm", value="5.45x39mm"),
            Choice(name="5.56x45mm NATO", value="5.56x45mm NATO"),
            Choice(name=".300 Blackout", value=".300 Blackout"),
            Choice(name="7.62x39mm", value="7.62x39mm"),
            Choice(name="7.62x51mm NATO", value="7.62x51mm NATO"),
            Choice(name="7.62x54mmR", value="7.62x54mmR"),
            Choice(name=".338 Lapua Magnum", value=".338 Lapua Magnum"),
            Choice(name="9x39mm", value="9x39mm"),
            Choice(name=".366 TKM", value=".366 TKM"),
            Choice(name="12.7x55mm STs-130", value="12.7x55mm STs-130"),
            Choice(name="12x70mm", value="12x70mm"),
            Choice(name="20x70mm", value="20x70mm"),
            Choice(name="23x75mm", value="23x75mm"),
            Choice(name="40x46mm", value="40x46mm"),
            Choice(name="40x53mm", value="40x53mm"),
            Choice(name="26x75mm", value="26x75mm"),
        ]
    )
    async def ammo(self, intrtaction: discord.Integration, name: str=None) -> None:
        self.ammo_chart_check = False
        if name:
            if type(name) == list:
                name = name[0]
            if name in self.bot.ammo_list.keys():
                info_str = ""
                info_str += f"\n**弾薬一覧**:"
                for ammunition in self.bot.ammo_list[name]:
                    info_str += f"\n・__[{ammunition['Name']}]({Url.EN_WIKI}{ammunition['Name'].replace(' ','_')})__"
                embed = discord.Embed(
                    title=name,
                    url=get_url(Url.EN_WIKI, name.replace(' ', '_')),
                    description=info_str,
                    timestamp=self.bot.update_timestamp,
                )
                embed.set_footer(
                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                )
                self.ammunition_figure_generation(self.bot.ammo_list, name)
                embed.set_image(url="attachment://ammo.png")
                await self.bot.send_deletable_message(intrtaction, embed=embed, file=self.file)
                os.remove("ammo.png")
            elif name in [
                ammo["Name"]
                for ammoData in self.bot.ammo_list.values()
                for ammo in ammoData
            ]:
                ammunition = [
                    ammo
                    for ammoData in self.bot.ammo_list.values()
                    for ammo in ammoData
                    if name == ammo["Name"]
                ][0]
                info_str = ""
                for key, value in ammunition.items():
                    if value != "":
                        if key == "Caliber":
                            info_str += f"\n**口径**: __[{value}]({Url.EN_WIKI}{value.replace('_', ' ')})__"
                        elif key == "Damage":
                            info_str += f"\n**ダメージ**: {value}"
                        elif key == "Penetration Power":
                            info_str += f"\n**貫通力**: {value}"
                        elif key == "Armor Damage":
                            info_str += f"\n**アーマーダメージ**: {value}"
                        elif key == "Accuracy":
                            info_str += f"\n**精度**: {value}"
                        elif key == "Recoil":
                            info_str += f"\n**リコイル**: {value}"
                        elif key == "Fragmentationchance":
                            info_str += f"\n**破裂確率**: {value}"
                        elif key == "Projectile Speed (m/s)":
                            info_str += f"\n**跳弾確率**: {value}"
                        elif key == "Light bleedingchance":
                            info_str += f"\n**軽度出血確率**: {value}%"
                        elif key == "Heavy bleedingchance":
                            info_str += f"\n**重度出血確率**: {value}%"
                        elif key == "Ricochetchance":
                            info_str += f"\n**弾速**: {value}"
                        elif key == "Special effects":
                            info_str += f"\n**特殊効果**: {value}"
                        elif key == "Sold by":
                            info_str += f"\n**販売元**: {value}"

                embed = discord.Embed(
                    title=name,
                    url=get_url(Url.EN_WIKI, name.replace(' ', '_')),
                    description=info_str,
                    timestamp=self.bot.update_timestamp,
                )
                embed.set_thumbnail(url=ammunition["Icon"])
                embed.set_footer(
                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                )
                try:
                    await self.bot.send_deletable_message(intrtaction, embed=embed)
                except:
                    import traceback

                    traceback.print_exc()
            else:
                pass
                # TODO エラー処理
                # await self.bot.on_slash_command_error(
                #     ctx, commands.CommandNotFound("ammo")
                # )
        else:
            text = "弾薬性能表示"
            ammoImages = [
                "Ammunition_List_1.jpg",
                "Ammunition_List_2.jpg",
            ]
            for n, url in enumerate(ammoImages):
                file = discord.File(f"../imgs/chart/ammo/{url}")
                embed = discord.Embed(
                    title=f"({n+1}/{len(ammoImages)}){text}",
                    color=0x808080,
                    url=f"https://eft.monster/",
                )
                embed.set_image(url=f"attachment://{url}")
                embed.set_author(
                    name="Twitter: bojotaro_tarkov",
                    url="https://twitter.com/bojotaro_tarkov",
                )
                embed.set_footer(
                    text="提供元: https://twitter.com/bojotaro_tarkov/status/1476871141709213702"
                )
                await self.bot.send_deletable_message(intrtaction, embed=embed, file=file)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Weapon(bot))