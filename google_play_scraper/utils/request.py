from typing import Union
# from urllib.error import HTTPError
# from urllib.request import Request, urlopen

from google_play_scraper.exceptions import ExtraHTTPError, NotFoundError
import requests


def _urlopen(obj):
    try:
        resp = urlopen(obj)
    except HTTPError as e:
        if e.code == 404:
            raise NotFoundError("App not found(404).")
        else:
            raise ExtraHTTPError(
                "App not found. Status code {} returned.".format(e.code)
            )

    return resp.read().decode("UTF-8")


def post(url: str, data: Union[str, bytes], headers: dict) -> str:
    return _urlopen(requests(url, data=data, headers=headers))


def get(url: str, proxy) -> str:
    if proxy:
        try:
            return requests.get(url, proxies={'https': proxy}, timeout=5).text
        except Exception as e:
            return None
    else:
        return requests.get(url).text
