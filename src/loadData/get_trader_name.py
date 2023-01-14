from const import Url
from util import get_requests_response, get_beautiful_soup_object

def get_trader_name():
    res = get_requests_response(Url.EN_WIKI, "Trading")
    soup = get_beautiful_soup_object(res)
    return [
        s.find_all("a")[0].get_text().replace(" ", "")
        for s in soup.find_all("tr")
        if s.find_all("a")
    ]
