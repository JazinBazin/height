from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
import xml.etree.ElementTree as ET

from .advantage import Advantage
from .real_estate_type import RealEstateType
from .real_estate import RealEstate, RealEstateImage
from .apartment import Apartment
from .house import House
from .land import Land
from .garage import Garage
from .commercial import Commercial
from .contact import Contact, ContactPhone
from .service import Service, ServiceListItem
from .description import Description

auto_delete_images = (Advantage, RealEstateType, RealEstate, RealEstateImage)
real_estate_models = (Apartment, House, Garage, Land, Commercial)
models_with_image = (Advantage, RealEstateType)
real_estate_title_image_height = 480
real_estate_thumnail_image_height = 200
default_image_height = 256

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
tree = ET.parse('sitemap.xml')
urlset = tree.getroot()


def receiver_with_multiple_senders(signal, senders, **kwargs):
    def decorator(receiver_function):
        for sender in senders:
            signal.connect(receiver_function, sender=sender, **kwargs)
        return receiver_function
    return decorator


def addUrlToSiteMap(link, pk):
    url = ET.SubElement(urlset, 'url', attrib={
        'pk': str(pk),
    })
    loc = ET.SubElement(url, 'loc')
    loc.text = link
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)


def removeUrlFromSiteMap(pk):
    pk = str(pk)
    for url in urlset:
        if url.get('pk', -1) == pk:
            urlset.remove(url)
            break
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)


@receiver_with_multiple_senders(models.signals.post_delete, auto_delete_images)
def delete_image_post_object(sender, instance, **kwargs):
    if instance.status == 'p':
        removeUrlFromSiteMap(instance.pk)
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
    if hasattr(instance, 'thumbnail'):
        if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)


def create_thumbnail(image_height, source_image, dest_image):
    with Image.open(source_image) as thumbnail:
        thumbnail.thumbnail((thumbnail.width, image_height))
        output = BytesIO()
        thumbnail.save(output, thumbnail.format)
        dest_image.save(os.path.basename(source_image.path),
                        ContentFile(output.getvalue()), save=False)


def real_estate_image_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        create_thumbnail(real_estate_thumnail_image_height,
                         instance.image, instance.thumbnail)
        return
    old_image = sender.objects.get(pk=instance.pk).image
    if old_image != instance.image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
        old_thumbnail = sender.objects.get(pk=instance.pk).thumbnail
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)
        create_thumbnail(real_estate_thumnail_image_height,
                         instance.image, instance.thumbnail)


models.signals.pre_save.connect(
    real_estate_image_pre_save, sender=RealEstateImage)


@receiver_with_multiple_senders(models.signals.pre_save, models_with_image)
def models_with_image_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        create_thumbnail(default_image_height, instance.image, instance.image)
        return
    old_image = sender.objects.get(pk=instance.pk).image
    if old_image != instance.image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
        create_thumbnail(default_image_height, instance.image, instance.image)


@receiver_with_multiple_senders(models.signals.pre_save, real_estate_models)
def real_estate_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        create_thumbnail(real_estate_title_image_height,
                         instance.image, instance.image)
        create_thumbnail(real_estate_thumnail_image_height,
                         instance.image, instance.thumbnail)
        return

    old_object = sender.objects.get(pk=instance.pk)
    old_status = old_object.status
    old_image = old_object.image

    if instance.status == 'p':
        if old_status == 'a':
            link = 'https://высота-крым.рф/' + \
                str(instance.pk) + instance.description_page + '/'
            addUrlToSiteMap(link, instance.pk)
    elif old_status == 'p':
        removeUrlFromSiteMap(instance.pk)

    if old_image != instance.image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
        old_thumbnail = sender.objects.get(pk=instance.pk).thumbnail
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)
        create_thumbnail(real_estate_title_image_height,
                         instance.image, instance.image)
        create_thumbnail(real_estate_thumnail_image_height,
                         instance.image, instance.thumbnail)


@receiver_with_multiple_senders(models.signals.post_save, real_estate_models)
def real_estate_post_save(sender, instance, created, **kwargs):
    if created == True and instance.status == 'p':
        link = 'https://высота-крым.рф/' + \
            str(instance.pk) + instance.description_page + '/'
        addUrlToSiteMap(link, instance.pk)
