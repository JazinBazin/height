import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

yrl_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}


def escape_yrl(text):
    return escape(text, yrl_escape_table)


ET._escape_cdata = escape_yrl

from .sitemap import addUrlToSiteMap, removeUrlFromSiteMap
from .feed import add_lot_offer, remove_lot_offer, update_lot_offer
