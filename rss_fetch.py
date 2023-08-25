import logging
import urllib
from datetime import datetime, timedelta
from xml.sax import SAXException

import feedparser


def rss_fetch(rss_list, logger: logging.Logger):
    feed_list = []
    for i, rss in enumerate(rss_list):
        logger.info("[{index}/{length}] fetching {title}".format(index=i+1, length=len(rss_list), title=rss.title))
        try:
            f = feedparser.parse(rss.xml_url)
        except urllib.error.URLError:
            logger.error("fetching {title} failed!!".format(title=rss.title))
        except SAXException:
            logger.fatal("RSS Feed XML Parse ERROR! it may be something went wrong.")
            exit(-5)
        feed_list.append(
            list(filter(
                lambda x: datetime(*x["updated_parsed"][:6]).date() >= (datetime.now() - timedelta(days=2)).date(),
                f['entries'])
            ))

    return feed_list
    # for e in f['entries']:
    #     feed_time = datetime(*e['updated_parsed'][:6])
    #     if feed_time.date() == (datetime.now() - timedelta(days=1)).date():
    #         pprint.pprint(e)
