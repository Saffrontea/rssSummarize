import os
import xml.etree.ElementTree
import xml.etree.ElementTree as ET
from dataclasses import dataclass as dataclass


@dataclass
class Rss:
    title: str
    url: str
    xml_url: str


def parse_opml(file: os.path, logger):
    url_list = []

    # import XML
    try:
        tree = ET.parse(file)
        xml_root = tree.getroot()
    except xml.etree.ElementTree.ParseError:
        logger.fatal("OPML file is broken!")
        exit(-10)

    elms = xml_root.findall(".//outline[@type='rss']")
    for e in elms:
        data = e.attrib
        item = Rss("", "", "")
        for k, v in data.items():
            if k == 'title':
                item.title = v
            elif k == "htmlUrl":
                item.url = v
            elif k == "xmlUrl":
                item.xml_url = v
        url_list.append(item)
    return url_list
