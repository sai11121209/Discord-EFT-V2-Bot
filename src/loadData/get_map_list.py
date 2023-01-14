import re
from const import Url
from util import get_requests_response, get_beautiful_soup_object

def get_map_list():
    res = get_requests_response(Url.EN_WIKI, "Map_of_Tarkov")
    soup = get_beautiful_soup_object(res)
    map_list = {}
    column_data = []
    for i, maps_data in enumerate(soup.find("tbody").find_all("tr")):
        if i != 0:
            map_name = maps_data.find_all("th")[1].find("a")["title"].upper().replace(" ", "")
            map_list[map_name] = {}
        for j, map_data in enumerate(maps_data.find_all(["th", "td"])):
            if i == 0:
                # 列名取得
                column_data.append(map_data.get_text().replace("\n", ""))
            else:
                if column_data[j] == "Banner":
                    try:
                        map_list[map_name].update(
                            {
                                column_data[j]: re.sub(
                                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                    "",
                                    map_data.find("img")["data-src"],
                                )
                                + "?format=original"
                            }
                        )
                    except:
                        map_list[map_name].update(
                            {
                                column_data[j]: re.sub(
                                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                    "",
                                    map_data.find("img")["src"],
                                )
                                + "?format=original"
                            }
                        )

                elif column_data[j] == "Name":
                    map_list[map_name].update(
                        {
                            column_data[j]: map_data.get_text().replace("\n", ""),
                            "MapUrl": map_data.find("a")["href"].replace(
                                "/wiki/", "", 1
                            ),
                        }
                    )
                else:
                    if map_data.find("hr"):
                        map_data.contents = [
                            map
                            for map in map_data
                            if map != map_data.find("hr") and map != "\n"
                        ]
                        if column_data[j] == "Duration" or column_data[j] == "Players":
                            tempData = {}
                            for map in map_data.contents:
                                key, value = (
                                    map.replace(" ", "")
                                    .replace("minutes", "")
                                    .split(":")
                                )
                                tempData.update({key: value.replace("\n", "")})
                            map_list[map_name].update({column_data[j]: tempData})

                        elif column_data[j] == "Enemy types":
                            tempData = []
                            for map in map_data.contents:
                                try:
                                    tempData.append(
                                        map.get_text().replace(" ", ""))
                                except:
                                    pass
                            map_list[map_name].update(
                                {column_data[j]: list(set(tempData))}
                            )
                    else:
                        if column_data[j] == "Enemy types":
                            map_list[map_name].update(
                                {
                                    column_data[j]: [
                                        map_data.get_text()
                                        .replace(" ", "")
                                        .replace("\n", "")
                                    ]
                                }
                            )
                        else:
                            map_list[map_name].update(
                                {
                                    column_data[j]: map_data.get_text()
                                    .replace("\n", "")
                                    .replace("minutes", "")
                                }
                            )
    return map_list
