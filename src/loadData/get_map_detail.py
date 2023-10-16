import re
from const import Url
from util import get_requests_response, get_beautiful_soup_object

def get_map_detail(map_lists):
    map_data = {}
    for key, value in map_lists.items():
        map_data[key] = value
        res = get_requests_response(Url.EN_WIKI, value['MapUrl'])
        soup = get_beautiful_soup_object(res, class_name="mw-parser-output")
        for s in soup.find_all("table"):
            s.decompose()

        try:
            soup.find("center").decompose()
            soup.find("div", {"class": "thumb"}).decompose()
        except:
            pass
        # Map情報の全imgタグを取得
        images = soup.find_all("img")
        map_data[key]["Images"] = {}
        for image in images:
            if (
                # customs: "FullScreenMapIcon.png"
                image["alt"] != "FullScreenMapIcon.png"
                # interchange: "The Power Switch"
                and image["alt"] != "The Power Switch"
                # laboratory: "TheLab-Insurance-Messages-01.PNG"
                and image["alt"] != "TheLab-Insurance-Messages-01.PNG"
                and image["alt"] != ""
                and image.get("data-src")
            ):
                # 参照画像サイズを800px -> オリジナル画像サイズに変換
                map_data[key]["Images"].update(
                    {
                        image["alt"]: re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            image.get("data-src"),
                        )
                        + "?format=original"
                    }
                )
    return map_data