import re
import discord
import datetime
from datetime import datetime as dt
from const import Url, ChannelCode
from util import get_requests_response, get_beautiful_soup_object

async def get_task_data(bot):
    res = get_requests_response(Url.EN_WIKI, "Quests")
    soup = get_beautiful_soup_object(res, class_name=None)
    task_data = {}
    length = len(soup.find_all("table", {"class": "wikitable"}))
    for n, tasks in enumerate(soup.find_all("table", {"class": "wikitable"})):
        await bot.set_status(
            status=discord.Status.idle,
            activity_name=f"タスクデータ({n+1}/{length})読み込み中...",
        )
        channel = bot.get_channel(ChannelCode.EXCEPTION_LOG)
        JST = datetime.timezone(datetime.timedelta(hours=9) , 'JST')
        embed = bot.create_base_embed(
            title=f"タスクデータ({n+1}/{length})ロード完了",
            color=0xFF0000,
            timestamp=dt.fromtimestamp(dt.now(JST).timestamp()),
        )
        await channel.send(embed=embed)
        dealerName = tasks.find_all("a")[0].text.replace("\n", "")
        try:
            task_data[dealerName] = {
                "dealerName": tasks.find_all("a")[0].text.replace("\n", ""),
                "dealerUrl": tasks.find_all("th")[0]
                .find("a")["href"]
                .replace("/wiki/", "", 1),
                "tasks": [],
            }
            res = get_requests_response(Url.EN_WIKI, task_data[dealerName]['dealerUrl'])
            soup = get_beautiful_soup_object(res, class_name="mw-parser-output")
        except:
            pass
        try:
            dealer_thumbnail = (
                re.sub(
                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                    "",
                    soup.find("td", {"class": "va-infobox-mainimage-image"}).find(
                        "img"
                    )["data-src"],
                )
                + "?format=original"
            )
        except:
            dealer_thumbnail = (
                re.sub(
                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                    "",
                    soup.find("td", {"class": "va-infobox-mainimage-image"}).find(
                        "img"
                    )["src"],
                )
                + "?format=original"
            )
        for task in tasks.find_all("tr")[2:]:
            try:
                task_dict = {
                    "questName": task.find_all("th")[0].text.replace("\n", ""),
                    "questUrl": task.find_all("th")[0]
                    .find("a")["href"]
                    .replace("/wiki/", "", 1),
                    "dealerName": dealerName,
                    "dealerUrl": tasks.find_all("th")[0]
                    .find("a")["href"]
                    .replace("/wiki/", "", 1),
                    "dealerThumbnail": dealer_thumbnail,
                    "type": task.find_all("th")[1].text.replace("\n", ""),
                    "objectives": [
                        {
                            "text": objective.text.replace("\n", ""),
                            "linkText": {
                                linkText.text.replace("\n", ""): linkText[
                                    "href"
                                ].replace("/wiki/", "", 1)
                                for linkText in objective.find_all("a")
                            },
                        }
                        for objective in task.find_all("td")[0].find_all("li")
                    ],
                    "rewards": [
                        {
                            "text": reward.text.replace("\n", ""),
                            "linkText": {
                                linkText.text.replace("\n", ""): linkText[
                                    "href"
                                ].replace("/wiki/", "", 1)
                                for linkText in reward.find_all("a")
                            },
                        }
                        for reward in task.find_all("td")[1].find_all("li")
                    ],
                }
                res = get_requests_response(Url.EN_WIKI, task_dict['questUrl'])
                soup = get_beautiful_soup_object(res, class_name="mw-parser-output")
                task_images = {}
                for n, image in enumerate(soup.find_all("li", {"class": "gallerybox"})):
                    try:
                        task_images.update(
                            {
                                image.find(
                                    "div", {"class": "gallerytext"}
                                ).p.text.replace("\n", ""): re.sub(
                                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                    "",
                                    image.find("img")["data-src"],
                                )
                                + "?format=original"
                            }
                        )
                    except:
                        try:
                            task_images.update(
                                {
                                    f"No Name Image {n}": re.sub(
                                        "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                        "",
                                        image.find("img")["data-src"],
                                    )
                                    + "?format=original"
                                }
                            )
                        except:
                            task_images.update(
                                {
                                    f"None{n}": re.sub(
                                        "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                        "",
                                        image.find("img")["src"],
                                    )
                                    + "?format=original"
                                }
                            )
                try:
                    task_dict.update(
                        {
                            "taskThumbnail": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                soup.find(
                                    "td", {
                                        "class": "va-infobox-mainimage-image"}
                                ).find("img")["data-src"],
                            )
                            + "?format=original",
                        }
                    )
                except:
                    task_dict.update(
                        {
                            "taskThumbnail": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                soup.find(
                                    "td", {
                                        "class": "va-infobox-mainimage-image"}
                                ).find("img")["src"],
                            )
                            + "?format=original",
                        }
                    )
                task_dict.update(
                    {
                        "taskImage": task_images,
                        "location": [
                            {
                                "text": location.text,
                                "linkText": location["href"].replace("/wiki/", "", 1),
                            }
                            for location in soup.find_all(
                                "td", {"class": "va-infobox-content"}
                            )[1].find_all("a")
                        ],
                        "reqKappa": soup.find_all(
                            "table", {"class": "va-infobox-group"}
                        )[1]
                        .find_all("td", {"class": "va-infobox-content"})[-1]
                        .text,
                    }
                )
                try:
                    task_dict.update(
                        {
                            "previousQuest": [
                                {
                                    "text": PreviousQuest.text,
                                    "linkText": PreviousQuest["href"].replace(
                                        "/wiki/", "", 1
                                    ),
                                }
                                for PreviousQuest in soup.find_all(
                                    "table", {"class": "va-infobox-group"}
                                )[2]
                                .find_all("td", {"class": "va-infobox-content"})[0]
                                .find_all("a")
                            ],
                            "nextQuest": [
                                {
                                    "text": nextQuest.text,
                                    "linkText": nextQuest["href"].replace(
                                        "/wiki/", "", 1
                                    ),
                                }
                                for nextQuest in soup.find_all(
                                    "table", {"class": "va-infobox-group"}
                                )[2]
                                .find_all("td", {"class": "va-infobox-content"})[1]
                                .find_all("a")
                            ],
                        }
                    )
                except:
                    task_dict.update(
                        {
                            "previousQuest": [],
                            "nextQuest": [],
                        }
                    )
                task_data[dealerName]["tasks"].append(task_dict)
            except:
                pass
        task_name = [
            task["questName"].replace(" ", "").upper()
            for tasks in task_data.values()
            for task in tasks["tasks"]
        ]
    return task_name, task_data