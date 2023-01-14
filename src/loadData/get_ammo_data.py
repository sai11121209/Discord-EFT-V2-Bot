import re
from const import Url
from util import get_requests_response, get_beautiful_soup_object

def get_ammo_data():
    ammo_caliber_url_list = []
    ammo_header = []
    ammo_list = {}
    res = get_requests_response(Url.EN_WIKI, "Ammunition")
    soup = get_beautiful_soup_object(res, class_name="mw-parser-output")
    soup.find("div", {"class": "toc"}).decompose()
    for table in soup.find_all("table", {"class": "wikitable"}):
        for ammo_caliber in table.find("tbody").find_all("tr")[1:]:
            ammo_caliber_url_list.append(
                ammo_caliber.find("a").get("href").replace("/wiki/", "")
            )
    for ammo_caliber_url in ammo_caliber_url_list:
        res = get_requests_response(Url.EN_WIKI, ammo_caliber_url)
        soup = get_beautiful_soup_object(res, class_name="mw-parser-output")
        ammo_list[ammo_caliber_url.replace("_", " ")] = []
        for table in soup.find_all("table", {"class": "wikitable"}):
            for n, ammo_caliber in enumerate(table.find("tbody").find_all("tr")):
                if n == 0:
                    for theader in ammo_caliber.find_all("th")[1:]:
                        ammo_header.append(
                            theader.get_text(strip=True).replace("\xa0%", "")
                        )
                else:
                    ammo_data = {}
                    ammo_data["Caliber"] = ammo_caliber_url.replace("_", " ")
                    try:
                        ammo_data["Icon"] = (
                            re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                ammo_caliber.find(["th", "td"]).find(
                                    "img")["data-src"],
                            )
                            + "?format=original"
                        )
                    except:
                        ammo_data["Icon"] = (
                            re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                ammo_caliber.find(["th", "td"]).find(
                                    "img")["src"],
                            )
                            + "?format=original"
                        )
                    for theader, ammo in zip(
                        ammo_header, ammo_caliber.find_all(["th", "td"])[1:]
                    ):
                        ammo_data[theader] = ammo.get_text(strip=True)
                    ammo_list[ammo_caliber_url.replace(
                        "_", " ")].append(ammo_data)
    return ammo_list