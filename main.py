import json
import logging
from logging import config
import sys
import dotenv

import requests

import time
from datetime import datetime, timedelta

import pprint

import xml_parse
from article_fetch import article_fetch
from rss_fetch import rss_fetch

# TODO: Flags

if __name__ == '__main__':
    with open("./log_config.json") as f:
        c = json.load(f)

    config.dictConfig(c)
    logger = logging.getLogger(__name__)
    # 2023-08-03 00:00:00,000 - [DEBUG]: msg

    logger.debug("launch App")
    dotenv.load_dotenv()
    logger.info("⚡RSS Summarizer⚡ rev 2023-08-03 running on Python %s" % sys.version)  # TODO: How to insert build date?

    # Load OPML file(RSS feeds)
    logger.debug("start import opml...")
    rss_list = xml_parse.parse_opml("feeds.opml", logger)
    logger.debug("import opml done")
    logger.debug(rss_list)

    # Fetch each RSS
    logger.debug("fetching RSS...")
    feed_list = rss_fetch(rss_list, logger)
    logger.debug("fetch RSS done!")
    # pprint.pprint(feed_list)

    # Fetch RSS Articles
    logger.debug("fetching and summarizing Articles...")
    article_list = article_fetch(feed_list, logger)
    logger.debug("summarizing Articles finish")

    # Make Output
    logger.debug("making output...")
    url = "https://weather.tsukumijima.net/api/forecast/city/"
    header = {"content-type": "application/json"}
    r = requests.get(url + "130010", headers=header)
    weather = r.json()
    article_list = list(map(lambda x: ' '.join(x.splitlines()), article_list))
    data_list = ["今日は{month}月{day}日です。".format(month=datetime.now().month, day=datetime.now().day),
                 "{loc}の天気は{weather}、最高気温は{maxtemp}で最低気温は{mintemp}です。".format(
                     loc=weather["location"]["city"],
                     weather=weather["forecasts"][0]["telop"],

                     maxtemp=weather["forecasts"][0]["temperature"]["max"]["celsius"] + "度"
                     if weather["forecasts"][0]["temperature"]["max"]["celsius"] is not None else "情報なし",

                     mintemp=weather["forecasts"][0]["temperature"]["min"]["celsius"] + "度"
                     if weather["forecasts"][0]["temperature"]["min"]["celsius"] is not None else "情報なし"),
                 "本日の技術ニュースは次のとおりです。",
                 article_list]
    text = "".join(map(lambda x: "".join(x), data_list))
    print(text)

