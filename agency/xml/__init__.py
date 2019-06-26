from .sitemap import addUrlToSiteMap, removeUrlFromSiteMap
from .feed_yandex import yandex_add_lot_offer, yandex_update_lot_offer, yandex_remove_lot_offer
from .feed_cian import cian_add_lot_offer, cian_update_lot_offer, cian_remove_lot_offer
from .feed_avito import avito_add_lot_offer, avito_update_lot_offer, avito_remove_lot_offer


def add_to_all_feeds(instance):
    yandex_add_lot_offer(instance)
    cian_add_lot_offer(instance)
    avito_add_lot_offer(instance)


def remove_from_all_feeds(pk):
    yandex_remove_lot_offer(pk)
    cian_remove_lot_offer(pk)
    avito_remove_lot_offer(pk)


def update_all_feeds(instance):
    yandex_update_lot_offer(instance)
    cian_update_lot_offer(instance)
    avito_update_lot_offer(instance)
