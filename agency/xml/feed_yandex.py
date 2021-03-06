import xml.etree.ElementTree as ET
from datetime import datetime
from xml.sax.saxutils import escape

yrl_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}

yandex_feed_file_name = 'feed_yandex.xml'


def escape_yrl(text):
    return escape(text, yrl_escape_table)


def yandex_add_lot_offer(instance):
    if instance.transaction_type == 'e':
        return

    ET_escape_cdata = ET._escape_cdata
    ET._escape_cdata = escape_yrl

    try:
        ET.register_namespace(
            '', 'http://webmaster.yandex.ru/schemas/feed/realty/2010-06')
        tree = ET.parse(yandex_feed_file_name)
        feed = tree.getroot()
        yandex_change_feed_generation_date(feed)
        yandex_create_lot_offer(feed, instance)
        tree.write(yandex_feed_file_name,
                   encoding='UTF-8', xml_declaration=True)
    except Exception as ex:
        with open('log.txt', 'a') as log_file:
            log_file.write('error in function yandex_add_lot_offer. pk = ' +
                           str(instance.pk) + '\nwhat: ' + str(ex) + '\n')
    finally:
        ET._escape_cdata = ET_escape_cdata


def yandex_remove_lot_offer(pk):
    try:
        pk = str(pk)
        ET.register_namespace(
            '', 'http://webmaster.yandex.ru/schemas/feed/realty/2010-06')
        tree = ET.parse(yandex_feed_file_name)
        feed = tree.getroot()
        yandex_change_feed_generation_date(feed)
        for offer in feed:
            if offer.tag != '{http://webmaster.yandex.ru/schemas/feed/realty/2010-06}generation-date' and offer.get('internal-id', -1) == pk:
                feed.remove(offer)
                break
        tree.write(yandex_feed_file_name, encoding='UTF-8', xml_declaration=True)
    except Exception as ex:
        with open('log.txt', 'a') as log_file:
            log_file.write('error in function yandex_remove_lot_offer. pk = ' +
                           str(pk) + '\nwhat: ' + str(ex) + '\n')


def yandex_update_lot_offer(instance):
    yandex_remove_lot_offer(instance.pk)
    yandex_add_lot_offer(instance)


def yandex_change_feed_generation_date(feed):
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


def yandex_create_lot_offer(feed, instance):
    offer = ET.Element('offer', attrib={
        'internal-id': str(instance.pk),
    })
    feed.append(offer)

    transaction_type = ET.SubElement(offer, 'type')
    if instance.transaction_type == 'p':
        transaction_type.text = 'продажа'
    else:
        transaction_type.text = 'аренда'
        rent_period = ET.SubElement(offer, 'period')
        rent_period.text = 'месяц'

    property_type = ET.SubElement(offer, 'property-type')
    property_type.text = 'жилая'

    category = ET.SubElement(offer, 'category')
    category.text = 'участок'

    lot_url = ET.SubElement(offer, 'url')
    lot_url.text = 'https://высота-крым.рф/' + \
        str(instance.pk) + 'land_description/'

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
    agent_photo.text = 'https://высота-крым.рф/static/agency/images/logo.png'

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
    lot_area_value.text = str(instance.area)

    lot_area_unit = ET.SubElement(lot_area, 'unit')
    if instance.area_units == 'm':
        lot_area_unit.text = 'кв. м'
    elif instance.area_units == 'h':
        lot_area_unit.text = 'гектар'
    else:
        lot_area_unit.text = 'cотка'

    lot_type = ET.SubElement(offer, 'lot-type')
    if instance.lot_type == 'i':
        lot_type.text = 'ИЖС'
    else:
        lot_type.text = 'садоводство'

    if instance.cadastral_number:
        cadastral_number = ET.SubElement(offer, 'cadastral-number')
        cadastral_number.text = str(instance.cadastral_number)

    haggle = ET.SubElement(offer, 'haggle')
    haggle.text = 'да' if instance.mortgage == True else 'нет'

    mortgage = ET.SubElement(offer, 'mortgage')
    mortgage.text = 'да' if instance.mortgage == True else 'нет'

    not_for_agents = ET.SubElement(offer, 'not-for-agents')
    not_for_agents.text = 'да'

    lot_image = ET.SubElement(offer, 'image')
    lot_image.text = 'https://высота-крым.рф' + str(instance.image.url)

    for photo in instance.images.all():
        lot_image = ET.SubElement(offer, 'image')
        lot_image.text = 'https://высота-крым.рф' + str(photo.image.url)

    description = ET.SubElement(offer, 'description')
    description.text = str(instance.description)
