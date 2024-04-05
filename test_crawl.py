#!./venv/bin/python3

from google_play_scraper.features.app import parse_dom
import requests
from pprint import pprint


def get_raw(url):

    try:
        result = requests.get(url)
        if result.status_code != 200:
            return 0, 1
        else:
            return 1, result
    except Exception as e:
        print(e)
        return 0, 2


def crawlapage(appid):



    url = f"https://play.google.com/store/apps/details?id={appid}"
    result = get_raw(url)

    if result[0]:
        return parse_dom(result[1].text, appid, url)
    elif result[1] == 2:
        return None
    else:
        return None


pprint(crawlapage("io.supercent.pizzaidle"))
