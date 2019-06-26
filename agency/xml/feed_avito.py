import xml.etree.ElementTree as ET

avito_feed_file_name = 'feed_avito.xml'


def avito_add_lot_offer(instance):
    try:
        if instance.transaction_type != 'p':
            return
        tree = ET.parse(avito_feed_file_name)
        feed = tree.getroot()
        avito_create_lot_offer(feed, instance)
        tree.write(avito_feed_file_name, encoding='UTF-8',
                   xml_declaration=False)
    except Exception as ex:
        with open('log.txt', 'a') as log_file:
            log_file.write('error in function avito_add_lot_offer. pk = ' +
                           str(instance.pk) + '\nwhat: ' + str(ex) + '\n')


def avito_remove_lot_offer(pk):
    try:
        pk = str(pk)
        tree = ET.parse(avito_feed_file_name)
        feed = tree.getroot()
        for ad in feed:
            ad_id = ad.find('Id')
            if ad_id.text == pk:
                feed.remove(ad)
                break
        tree.write(avito_feed_file_name, encoding='UTF-8',
                   xml_declaration=False)
    except Exception as ex:
        with open('log.txt', 'a') as log_file:
            log_file.write('error in function avito_remove_lot_offer. pk = ' +
                           str(pk) + '\nwhat: ' + str(ex) + '\n')


def avito_update_lot_offer(instance):
    avito_remove_lot_offer(instance.pk)
    avito_add_lot_offer(instance)


def avito_create_lot_offer(feed, instance):
    Ad = ET.Element('Ad')
    feed.append(Ad)

    ad_id = ET.SubElement(Ad, 'Id')
    ad_id.text = str(instance.pk)

    AllowEmail = ET.SubElement(Ad, 'AllowEmail')
    AllowEmail.text = 'Да'

    ManagerName = ET.SubElement(Ad, 'ManagerName')
    ManagerName.text = 'Юденич Светлана Станиславовна'

    ContactPhone = ET.SubElement(Ad, 'ContactPhone')
    ContactPhone.text = '+7 (978) 834-31-76'

    Address = ET.SubElement(Ad, 'Address')
    Address.text = 'Россия, Крым'
    if instance.district:
        Address.text += ', ' + str(instance.district)
        if 'район' not in str(instance.district).lower():
            Address.text += ' район'
    if instance.populated_area:
        Address.text += ', ' + str(instance.populated_area)

    DistanceToCity = ET.SubElement(Ad, 'DistanceToCity')
    DistanceToCity.text = '0'

    Description = ET.SubElement(Ad, 'Description')
    Description.text = str(instance.description)

    Category = ET.SubElement(Ad, 'Category')
    Category.text = 'Земельные участки'

    OperationType = ET.SubElement(Ad, 'OperationType')
    OperationType.text = 'Продам'

    Price = ET.SubElement(Ad, 'Price')
    if instance.currency == 'r':
        Price.text = str(int(instance.price))
    elif instance.currency == 'd':
        Price.text = str(int(instance.price * 60))
    else:
        Price.text = str(int(instance.price * 70))

    LandArea = ET.SubElement(Ad, 'LandArea')

    if instance.area_units == 'm':
        LandArea.text = str(int(instance.area / 100))
    elif instance.area_units == 'h':
        LandArea.text = str(int(instance.area / 10000))
    else:
        LandArea.text = str(int(instance.area))

    PropertyRights = ET.SubElement(Ad, 'PropertyRights')
    if instance.cadastral_number:
        PropertyRights.text = 'Собственник'
        CadastralNumber = ET.SubElement(Ad, 'CadastralNumber')
        CadastralNumber.text = str(instance.cadastral_number)
    else:
        PropertyRights.text = 'Посредник'

    ObjectType = ET.SubElement(Ad, 'ObjectType')
    if instance.lot_type == 'i':
        ObjectType.text = 'Поселений (ИЖС)'
    else:
        ObjectType.text = 'Сельхозназначения (СНТ, ДНП)'

    Images = ET.SubElement(Ad, 'Images')

    Image = ET.SubElement(Images, 'Image')
    Image.set('url', 'https://высота-крым.рф' + str(instance.image.url))

    for photo in instance.images.all():
        Image = ET.SubElement(Images, 'Image')
        Image.set('url', 'https://высота-крым.рф' + str(photo.image.url))
