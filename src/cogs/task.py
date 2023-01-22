import discord
from discord import app_commands
from discord.ext import commands
from const import Url
from util import get_url


class Task(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="task", description="タスク一覧表示コマンド")
    @app_commands.describe(name="名前")
    async def task(self, intrtaction:discord.Integration, name:str=None) -> None:
        if name:
            if type(name) == list:
                name = name[0]
            try:
                task_data = [
                    value
                    for values in self.bot.tasks_detail.values()
                    for value in values["tasks"]
                    if value["questName"].lower().replace(" ", "") == name
                ][0]
            except:
                return await self.bot.on_command_error(intrtaction, commands.CommandNotFound("task"))
            info_str = ""
            embeds = []
            for col_name, values in task_data.items():
                if col_name == "dealerName":
                    info_str += f"**ディーラー**: __[{task_data[col_name]}]({Url.EN_WIKI}{task_data['dealerUrl']})__"
                elif col_name == "type":
                    info_str += f"\n*タイプ**: __{task_data[col_name]}__"
                elif col_name == "objectives":
                    info_str += f"\n**目的**:"
                    for objective in values:
                        hyper_text = objective["text"]
                        for text, link in objective["linkText"].items():
                            hyper_text = hyper_text.replace(
                                f"{text}",
                                f"[{text}]({Url.EN_WIKI}{link})",
                            )
                        info_str += f"\n・__{hyper_text}__"
                elif col_name == "rewards":
                    info_str += f"\n**報酬**:"
                    for reward in values:
                        hyper_text = reward["text"]
                        for text, link in reward["linkText"].items():
                            hyper_text = hyper_text.replace(
                                f"{text}",
                                f"[{text}]({Url.EN_WIKI}{link})",
                            )
                        info_str += f"\n・__{hyper_text}__"
                elif col_name == "location":
                    info_str += f"\n**場所**:"
                    if len(task_data[col_name]) == 0:
                        info_str += f" __-__"
                    elif len(task_data[col_name]) == 1:
                        hyper_text = task_data[col_name][0]["text"]
                        hyper_text = hyper_text.replace(
                            f"{task_data[col_name][0]['text']}",
                            f"[{task_data[col_name][0]['text']}]({Url.EN_WIKI}{task_data[col_name][0]['linkText']})",
                        )
                        info_str += f" __{hyper_text}__"
                    else:
                        for location in task_data[col_name]:
                            hyper_text = location["text"]
                            hyper_text = hyper_text.replace(
                                f"{location['text']}",
                                f"[{location['text']}]({Url.EN_WIKI}{location['linkText']})",
                            )
                            info_str += f"\n・__{hyper_text}__"
                elif col_name == "previous_quest":
                    info_str += f"\n**事前タスク**:"
                    if len(task_data[col_name]) == 0:
                        info_str += f" __-__"
                    elif len(task_data[col_name]) == 1:
                        hyper_text = task_data[col_name][0]["text"]
                        hyper_text = hyper_text.replace(
                            f"{task_data[col_name][0]['text']}",
                            f"[{task_data[col_name][0]['text']}]({Url.EN_WIKI}{task_data[col_name][0]['linkText']})",
                        )
                        info_str += f" __{hyper_text}__"
                    else:
                        for previous_quest in task_data[col_name]:
                            hyper_text = previous_quest["text"]
                            hyper_text = hyper_text.replace(
                                f"{previous_quest['text']}",
                                f"[{previous_quest['text']}]({Url.EN_WIKI}{previous_quest['linkText']})",
                            )
                            info_str += f"\n・__{hyper_text}__"
                elif col_name == "next_quest":
                    info_str += f"\n**事後タスク**:"
                    if len(task_data[col_name]) == 0:
                        info_str += f" __-__"
                    elif len(task_data[col_name]) == 1:
                        hyper_text = task_data[col_name][0]["text"]
                        hyper_text = hyper_text.replace(
                            f"{task_data[col_name][0]['text']}",
                            f"[{task_data[col_name][0]['text']}]({Url.EN_WIKI}{task_data[col_name][0]['linkText']})",
                        )
                        info_str += f" __{hyper_text}__"
                    else:
                        for next_quest in task_data[col_name]:
                            hyper_text = next_quest["text"]
                            hyper_text = hyper_text.replace(
                                f"{next_quest['text']}",
                                f"[{next_quest['text']}]({Url.EN_WIKI}{next_quest['linkText']})",
                            )
                            info_str += f"\n・__{hyper_text}__"
                elif col_name == "taskImage":
                    for image_url in values.values():
                        embed = self.bot.create_base_embed(
                            title=f"{task_data['questName']} Image",
                            url=get_url(Url.EN_WIKI, task_data['questUrl']),
                            thumbnail=task_data["dealerThumbnail"]
                        )
                        embed.set_image(url=image_url)
                        embeds.append(embed)
            embed = self.bot.create_base_embed(
                title=task_data["questName"],
                url=get_url(Url.EN_WIKI, task_data['questUrl']),
                description=info_str,
                thumbnail=task_data["dealerThumbnail"]
            )
            embed.set_image(url=task_data["taskThumbnail"])
            await self.bot.send_deletable_message(intrtaction, embed=embed)
            await self.bot.send_deletable_message(intrtaction, embeds=embeds)
        else:
            for n, (index, values) in enumerate(self.bot.tasks_detail.items()):
                embed = self.bot.create_base_embed(
                    title=f"タスク一覧({n+1}/{len(self.bot.tasks_detail)})",
                    url=get_url(Url.EN_WIKI, "Quests"),
                )
                embed.add_field(
                    name=f"{index}",
                    value=f"[海外Wiki]({Url.EN_WIKI}{values['dealerUrl']})",
                    inline=False,
                )
                for value in values["tasks"]:
                    embed.add_field(
                        name=value["questName"],
                        value=f"[海外Wiki]({Url.EN_WIKI}{value['questUrl']})",
                        inline=True,
                    )
                    embed.set_thumbnail(url=value["dealerThumbnail"])
                await self.bot.send_deletable_message(intrtaction, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Task(bot))
