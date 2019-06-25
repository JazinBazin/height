import xml.etree.ElementTree as ET

cian_feed_file_name = 'feed_cian.xml'


def cian_add_lot_offer(instance):
    try:
        if instance.transaction_type != 'p':
            return
        tree = ET.parse(cian_feed_file_name)
        feed = tree.getroot()
        cian_create_lot_offer(feed, instance)
        tree.write(cian_feed_file_name, encoding='UTF-8',
                   xml_declaration=False)
    except Exception as ex:
        with open('log.txt', 'a') as log_file:
            log_file.write('error in function cian_add_lot_offer. pk = ' +
                           str(instance.pk) + '\nwhat: ' + str(ex) + '\n')


def cian_remove_lot_offer(pk):
    try:
        pk = str(pk)
        tree = ET.parse(cian_feed_file_name)
        feed = tree.getroot()
        for ad_object in feed:
            if ad_object.tag != 'feed_version':
                ExternalId = ad_object.find('ExternalId')
                if ExternalId.text == pk:
                    feed.remove(ad_object)
                    break
        tree.write(cian_feed_file_name, encoding='UTF-8',
                   xml_declaration=False)
    except Exception as ex:
        with open('log.txt', 'a') as log_file:
            log_file.write('error in function cian_remove_lot_offer. pk = ' +
                           str(pk) + '\nwhat: ' + str(ex) + '\n')


def cian_update_lot_offer(instance):
    cian_remove_lot_offer(instance.pk)
    cian_add_lot_offer(instance)


def length_without_punctuation(string):
    return sum((1 for ch in string if ch.isdigit() or ch.isalpha()), 0)


def cian_create_lot_offer(feed, instance):
    ad_object = ET.Element('object')
    feed.append(ad_object)

    ExternalId = ET.SubElement(ad_object, 'ExternalId')
    ExternalId.text = str(instance.pk)

    Description = ET.SubElement(ad_object, 'Description')
    Description.text = str(instance.description)

    Address = ET.SubElement(ad_object, 'Address')
    Address.text = 'Россия, Республика Крым'
    if instance.district:
        Address.text += ', ' + str(instance.district)
        if 'район' not in str(instance.district).lower():
            Address.text += ' район'
    if instance.populated_area:
        Address.text += ', ' + str(instance.populated_area)

    if instance.cadastral_number:
        CadastralNumber = ET.SubElement(ad_object, 'CadastralNumber')
        CadastralNumber.text = str(instance.cadastral_number)

    Phones = ET.SubElement(ad_object, 'Phones')

    PhoneSchema = ET.SubElement(Phones, 'PhoneSchema')

    CountryCode = ET.SubElement(PhoneSchema, 'CountryCode')
    CountryCode.text = '+7'

    phone_number = ET.SubElement(PhoneSchema, 'CountryCode')
    phone_number.text = '9788343176'

    SubAgent = ET.SubElement(ad_object, 'SubAgent')

    agent_email = ET.SubElement(SubAgent, 'Email')
    agent_email.text = 'visota-agency@rambler.ru'

    agent_phone = ET.SubElement(SubAgent, 'Phone')
    agent_phone.text = '+7 (978) 834-31-76'

    agent_first_name = ET.SubElement(SubAgent, 'FirstName')
    agent_first_name.text = 'Светлана'

    agent_last_name = ET.SubElement(SubAgent, 'LastName')
    agent_last_name.text = 'Юденич'

    AvatarUrl = ET.SubElement(SubAgent, 'AvatarUrl')
    AvatarUrl.text = 'https://высота-крым.рф/static/agency/images/logo.png'

    LayoutPhoto = ET.SubElement(ad_object, 'LayoutPhoto')

    FullUrl = ET.SubElement(LayoutPhoto, 'FullUrl')
    FullUrl.text = 'https://высота-крым.рф' + str(instance.image.url)

    IsDefault = ET.SubElement(LayoutPhoto, 'IsDefault')
    IsDefault.text = 'true'

    if instance.images.count() != 0:
        Photos = ET.SubElement(ad_object, 'Photos')

        for photo in instance.images.all():
            PhotoSchema = ET.SubElement(Photos, 'PhotoSchema')

            FullUrl = ET.SubElement(PhotoSchema, 'FullUrl')
            FullUrl.text = 'https://высота-крым.рф' + str(photo.image.url)

            IsDefault = ET.SubElement(PhotoSchema, 'IsDefault')
            IsDefault.text = 'false'

    if (length_without_punctuation(instance.headline) >= 8
            and len(instance.headline) <= 33):
        Title = ET.SubElement(ad_object, 'Title')
        Title.text = str(instance.headline)

    Category = ET.SubElement(ad_object, 'Category')
    Category.text = 'landSale'

    Land = ET.SubElement(ad_object, 'Land')
    Area = ET.SubElement(Land, 'Area')
    AreaUnitType = ET.SubElement(Land, 'AreaUnitType')

    if instance.area_units == 'm':
        Area.text = str(instance.area / 100)
        AreaUnitType.text = 'sotka'
    elif instance.area_units == 'h':
        Area.text = str(instance.area)
        AreaUnitType.text = 'hectare'
    else:
        Area.text = str(instance.area)
        AreaUnitType.text = 'sotka'

    land_status = ET.SubElement(Land, 'Status')
    if instance.lot_type == 'i':
        land_status.text = 'individualHousingConstruction'
    elif instance.lot_type == 'a':
        land_status.text = 'farm'
    elif instance.lot_type == 'g':
        land_status.text = 'gardening'
    else:
        land_status.text = 'privateFarm'

    BargainTerms = ET.SubElement(ad_object, 'BargainTerms')

    Price = ET.SubElement(BargainTerms, 'Price')
    Price.text = str(instance.price)

    Currency = ET.SubElement(BargainTerms, 'Currency')
    if instance.currency == 'r':
        Currency.text = 'rur'
    elif instance.currency == 'd':
        Currency.text = 'usd'
    else:
        Currency.text = 'eur'
