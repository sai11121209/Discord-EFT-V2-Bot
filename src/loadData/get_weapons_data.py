import re
from const import Url
from util import get_requests_response, get_beautiful_soup_object

def get_weapons_data():
    res = get_requests_response(Url.EN_WIKI, "Weapons")
    soup = get_beautiful_soup_object(res, class_name=None)
    EXCLUSION = [
        "Primaryweapons",
        "Secondaryweapons",
        "Stationaryweapons",
        "Throwableweapons",
        "Upcomingweapons",
        "Primaryweapons",
        "Secondaryweapons",
        "Launchers",
        "Throwableweapons",
        "Mines",
        "Stationaryweapons",
        "Mortar",
        "AntitankGun",
        "Unconfirmedweapons",
        "PrimaryWeapons",
        "SecondaryWeapons",
        "Launchers",
    ]
    PRIMARY_CATEGORY = [
        "Assault rifles",
        "Assault carbines",
        "Light machine guns",
        "Submachine guns",
        "Shotguns",
        "Designated marksman rifles",
        "Sniper rifles",
        "Grenade launchers",
    ]
    SECONDARY_CATEGORY = [
        "Pistols",
        "Signal pistols",
        "Revolvers",
        "Special weapons",
    ]
    STATIONARY_CATEGORY = [
        "Heavy machine guns",
        "Automatic Grenade launchers",
    ]
    MELEE_CATEGORY = ["Melee weapons"]
    THROWABLE_CATEGORY_ONE = [
        "Fragmentation grenades",
    ]
    THROWABLE_CATEGORY_TWO = [
        "Smoke grenades",
        "Stun grenades",
    ]
    weapon_category_list = [
        category.get_text()
        for category in soup.find_all("span", {"class": "toctext"})
        if category.get_text().replace(" ", "") not in EXCLUSION
    ]
    weapons_data = {}
    for weapons, category in zip(
        soup.find_all("table", class_="wikitable")[
            : len(weapon_category_list) - 1],
        weapon_category_list,
    ):
        weapons_data[category] = []
        if category in PRIMARY_CATEGORY or category in SECONDARY_CATEGORY:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
                    weapon_informations = GetWeaponInformations(weapon)
                    weapons_data[category].append(
                        {
                            "名前": weapon.find_all("td")[0].find("a")["title"],
                            "種類": weapon_informations["Type"].get_text(),
                            "typeUrl": weapon_informations["Type"]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "weaponUrl": weapon.find_all("td")[0]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "imageUrl": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                weapon.find("img").attrs["src"],
                            )
                            + "?format=original",
                            "重量": [
                                ""
                                if weapon_informations["Weight"] == ""
                                else weapon_informations["Weight"].get_text()
                            ][0],
                            "サイズ": [
                                ""
                                if weapon_informations["Grid size"] == ""
                                else weapon_informations["Grid size"].get_text()
                            ][0],
                            "販売元": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"].get_text()
                            ][0],
                            "soldByUrl": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"]
                                .find("a")["href"]
                                .replace("/wiki/", "", 1)
                            ][0],
                            "リコイル": {
                                "垂直反動": str(
                                    weapon_informations["Recoil"]
                                    .contents[0]
                                    .replace(" ", "")
                                    .split(":")[1]
                                ),
                                "水平反動": str(
                                    weapon_informations["Recoil"]
                                    .contents[2]
                                    .replace(" ", "")
                                    .split(":")[1]
                                ),
                            },
                            "有効射程": weapon_informations["Effective distance"].get_text(),
                            "口径": weapon.find_all("td")[1].find("a")["title"],
                            "cartridgeUrl": weapon.find_all("td")[1]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "発射機構": [
                                firingmode.replace(
                                    "\n", "").replace("\xa0", " ")
                                for firingmode in weapon.find_all("td")[2].contents
                                if firingmode != soup.hr and firingmode != soup.br
                            ],
                            "連射速度": weapon.find_all("td")[3]
                            .get_text()
                            .replace("\n", ""),
                            "使用可能弾薬": [
                                acceptedAmmunition
                                for acceptedAmmunition in weapon_informations[
                                    "Accepted ammunition"
                                ]
                                .get_text()
                                .split("\n")
                                if acceptedAmmunition != ""
                            ],
                            "詳細": weapon.find_all("td")[4].get_text(),
                        }
                    )
                except:
                    pass
        elif category in STATIONARY_CATEGORY:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
                    weapon_informations = GetWeaponInformations(weapon)
                    weapons_data[category].append(
                        {
                            "名前": weapon.find_all("td")[0].find("a")["title"],
                            "weaponUrl": weapon.find_all("td")[0]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "imageUrl": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                weapon.find("img").attrs["src"],
                            )
                            + "?format=original",
                            "重量": [
                                ""
                                if weapon_informations["Weight"] == ""
                                else weapon_informations["Weight"].get_text()
                            ][0],
                            "サイズ": [
                                ""
                                if weapon_informations["Grid size"] == ""
                                else weapon_informations["Grid size"].get_text()
                            ][0],
                            "販売元": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"].get_text()
                            ][0],
                            "soldByUrl": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"]
                                .find("a")["href"]
                                .replace("/wiki/", "", 1)
                            ][0],
                            "口径": weapon.find_all("td")[1].find("a")["title"],
                            "cartridgeUrl": weapon.find_all("td")[1]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "発射機構": [
                                firingmode.replace(
                                    "\n", "").replace("\xa0", " ")
                                for firingmode in weapon.find_all("td")[2].contents
                                if firingmode != soup.hr and firingmode != soup.br
                            ],
                            "使用可能弾薬": [
                                acceptedAmmunition
                                for acceptedAmmunition in weapon_informations[
                                    "Accepted ammunition"
                                ]
                                .get_text()
                                .split("\n")
                                if acceptedAmmunition != ""
                            ],
                        }
                    )
                except:
                    pass
        elif category in MELEE_CATEGORY:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
                    weapon_informations = GetWeaponInformations(weapon)
                    weapons_data[category].append(
                        {
                            "名前": weapon.find_all("td")[0].find("a")["title"],
                            "weaponUrl": weapon.find_all("td")[0]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "imageUrl": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                weapon.find("img").attrs["src"],
                            )
                            + "?format=original",
                            "重量": [
                                ""
                                if weapon_informations["Weight"] == ""
                                else weapon_informations["Weight"].get_text()
                            ][0],
                            "サイズ": [
                                ""
                                if weapon_informations["Grid size"] == ""
                                else weapon_informations["Grid size"].get_text()
                            ][0],
                            "販売元": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"].get_text()
                            ][0],
                            "soldByUrl": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"]
                                .find("a")["href"]
                                .replace("/wiki/", "", 1)
                            ][0],
                            "斬撃ダメージ": weapon.find_all("td")[1].get_text().replace("\n","",),
                            "斬撃距離": weapon.find_all("td")[2]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                            "刺突ダメージ": weapon.find_all("td")[3]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                            "刺突距離": weapon.find_all("td")[4]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                            "詳細": weapon.find_all("td")[5]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                        }
                    )
                except:
                    pass
        elif category in THROWABLE_CATEGORY_ONE:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
                    weapon_informations = GetWeaponInformations(weapon)
                    weapons_data[category].append(
                        {
                            "名前": weapon.find_all("td")[0].find("a")["title"],
                            "weaponUrl": weapon.find_all("td")[0]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "imageUrl": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                weapon.find("img").attrs["src"],
                            )
                            + "?format=original",
                            "重量": [
                                ""
                                if weapon_informations["Weight"] == ""
                                else weapon_informations["Weight"].get_text()
                            ][0],
                            "サイズ": [
                                ""
                                if weapon_informations["Grid size"] == ""
                                else weapon_informations["Grid size"].get_text()
                            ][0],
                            "販売元": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"].get_text()
                            ][0],
                            "soldByUrl": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"]
                                .find("a")["href"]
                                .replace("/wiki/", "", 1)
                            ][0],
                            "信管作動時間(s)": weapon.find_all("td")[1].get_text(),
                            "加害範囲": weapon.find_all("td")[2].get_text(),
                            "1破片当たりの最大ダメージ": weapon.find_all("td")[3].get_text(),
                            "破片数": weapon.find_all("td")[4].get_text(),
                            "詳細": weapon.find_all("td")[5].get_text(),
                        }
                    )
                except:
                    pass

        elif category in THROWABLE_CATEGORY_TWO:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
                    weapon_informations = GetWeaponInformations(weapon)
                    weapons_data[category].append(
                        {
                            "名前": weapon.find_all("td")[0].find("a")["title"],
                            "weaponUrl": weapon.find_all("td")[0]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1),
                            "imageUrl": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                weapon.find("img").attrs["src"],
                            )
                            + "?format=original",
                            "重量": [
                                ""
                                if weapon_informations["Weight"] == ""
                                else weapon_informations["Weight"].get_text()
                            ][0],
                            "サイズ": [
                                ""
                                if weapon_informations["Grid size"] == ""
                                else weapon_informations["Grid size"].get_text()
                            ][0],
                            "販売元": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"].get_text()
                            ][0],
                            "soldByUrl": [
                                ""
                                if weapon_informations["Sold by"] == ""
                                else weapon_informations["Sold by"]
                                .find("a")["href"]
                                .replace("/wiki/", "", 1)
                            ][0],
                            "信管作動時間(s)": weapon.find_all("td")[1].get_text(),
                            "詳細": weapon.find_all("td")[2].get_text(),
                        }
                    )
                except:
                    pass

    weapons_name = [
        weapon["名前"].upper()
        for weaponData in weapons_data.values()
        for weapon in weaponData
    ]

    return weapons_name, weapons_data

def GetWeaponInformations(weapon):
    res = get_requests_response(Url.EN_WIKI, weapon.find_all('td')[0].find('a')['href'].replace('/wiki/', '', 1))
    soup = get_beautiful_soup_object(res, class_name=None)
    weapon_informations = {}
    weapon_informations = {
        label.get_text().replace("\xa0", " "): contents
        for weaponInformation in soup.find_all("table", {"class": "va-infobox-group"})
        for label, contents in zip(
            weaponInformation.find_all("td", {"class": "va-infobox-label"}),
            weaponInformation.find_all("td", {"class": "va-infobox-content"}),
        )
    }
    if "Weight" not in weapon_informations:
        weapon_informations["Weight"] = ""
    if "Sold by" not in weapon_informations:
        weapon_informations["Sold by"] = ""
    if "Grid size" not in weapon_informations:
        weapon_informations["Grid size"] = ""

    return weapon_informations