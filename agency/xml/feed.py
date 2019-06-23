import xml.etree.ElementTree as ET
from datetime import datetime

def add_lot_offer(instance):
    if instance.transaction_type == 'e':
        return
    try:
        ET.register_namespace(
            '', 'http://webmaster.yandex.ru/schemas/feed/realty/2010-06')
        tree = ET.parse('feed.xml')
        feed = tree.getroot()
        change_feed_generation_date(feed)
        create_lot_offer(feed, instance)
        tree.write('feed.xml', encoding='UTF-8', xml_declaration=True)
    except:
        log_file = open('log.txt', 'a')
        log_file.write('error in function add_lot_offer. pk = ' + str(instance.pk))
        log_file.close()


def remove_lot_offer(pk):
    pk = str(pk)
    try:
        ET.register_namespace(
            '', 'http://webmaster.yandex.ru/schemas/feed/realty/2010-06')
        tree = ET.parse('feed.xml')
        feed = tree.getroot()
        change_feed_generation_date(feed)
        for offer in feed:
            if offer.tag != '{http://webmaster.yandex.ru/schemas/feed/realty/2010-06}generation-date' and offer.get('internal-id', -1) == pk:
                feed.remove(offer)
                break
        tree.write('feed.xml', encoding='UTF-8', xml_declaration=True)
    except:
        log_file = open('log.txt', 'a')
        log_file.write('error in function remove_lot_offer. pk = ' + str(pk))
        log_file.close()


def change_feed_generation_date(feed):
    generation_date = feed.find(
        '{http://webmaster.yandex.ru/schemas/feed/realty/2010-06}generation-date')
    if generation_date is not None:
        generation_date.text = datetime.now().replace(
            microsecond=0).isoformat(sep='T') + '+03:00'
    else:
        generation_date = ET.Element('generation-date')
        generation_date.text = datetime.now().replace(
            microsecond=0).isoformat(sep='T') + '+03:00'
        feed.insert(0, generation_date)


def create_lot_offer(feed, instance):
    offer = ET.Element('offer', attrib={
        'internal-id': str(instance.pk),
    })
    feed.append(offer)
    transaction_type = ET.SubElement(offer, 'type')
    transaction_type.text = 'продажа' if instance.transaction_type == 'p' else 'аренда'
    property_type = ET.SubElement(offer, 'property-type')
    property_type.text = 'участок'
    lot_url = ET.SubElement(offer, 'url')
    lot_url.text = 'https://высота-крым.рф/' + str(instance.pk) + 'land_description/'
    creation_date = ET.SubElement(offer, 'creation-date')
    creation_date.text = datetime.now().replace(
        microsecond=0).isoformat(sep='T') + '+03:00'
    location = ET.SubElement(offer, 'location')
    country = ET.SubElement(location, 'country')
    country.text = 'Россия'
    region = ET.SubElement(location, 'region')
    region.text = 'Республика Крым'
    if instance.district:
        district = ET.SubElement(location, 'district')
        district.text = str(instance.district)
    if instance.populated_area:
        locality_name = ET.SubElement(location, 'locality-name')
        locality_name.text = str(instance.populated_area)
    sales_agent = ET.SubElement(offer, 'sales-agent')
    agent_name = ET.SubElement(sales_agent, 'name')
    agent_name.text = 'Юденич Светлана Станиславовна'
    agent_phone = ET.SubElement(sales_agent, 'phone')
    agent_phone.text = '+79788343176'
    agent_category = ET.SubElement(sales_agent, 'category')
    agent_category.text = 'агентство'
    agent_organization = ET.SubElement(sales_agent, 'organization')
    agent_organization.text = 'Высота'
    agent_url = ET.SubElement(sales_agent, 'url')
    agent_url.text = 'https://высота-крым.рф'
    agent_email = ET.SubElement(sales_agent, 'email')
    agent_email.text = 'visota-agency@rambler.ru'
    agent_photo = ET.SubElement(sales_agent, 'photo')
    agent_photo.text = 'https://высота-крым.рф/static/agency/images/favicon32x32.ico'
    price = ET.SubElement(offer, 'price')
    price_value = ET.SubElement(price, 'value')
    price_value.text = str(instance.price)
    price_currency = ET.SubElement(price, 'currency')
    if instance.currency == 'r':
        price_currency.text = 'RUR'
    elif instance.currency == 'd':
        price_currency.text = 'USD'
    else:
        price_currency.text = 'EUR'
    deal_status = ET.SubElement(offer, 'deal-status')
    deal_status.text = 'прямая продажа'
    lot_area = ET.SubElement(offer, 'lot-area')
    lot_area_value = ET.SubElement(lot_area, 'value')
    lot_area_value.text = str(instance.area.normalize())
    lot_area_unit = ET.SubElement(lot_area, 'unit')
    if instance.area_units == 'm':
        lot_area_unit.text = 'кв. м'
    elif instance.area_units == 'h':
        lot_area_unit.text = 'гектар'
    else:
        lot_area_unit.text = 'cотка'
    # lot_type = ET.SubElement(offer, 'lot-type')
    # lot_type.text = 'ИЖС'
    lot_image = ET.SubElement(offer, 'lot-image')
    lot_image.text = 'https://высота-крым.рф/media/agency/images/real_estate_titles/IMG-35a6fa6b68e32d3575a20a18f37ae24b-V.jpg'
    description = ET.SubElement(offer, 'description')
    description.text = instance.description