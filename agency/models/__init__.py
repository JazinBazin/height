from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
import agency.xml

from .district import District
from .populated_area import PopulatedArea
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
from .certificate import Certificate

models_with_image = (RealEstate, RealEstateType,
                     RealEstateImage, Advantage, Certificate)
real_estate_models = (Apartment, House, Garage, Land, Commercial)
models_with_default_image_height = (Advantage, RealEstateType)

real_estate_title_image_height = 480
real_estate_thumnail_image_height = 200
default_image_height = 256


def remove_from_xml(sender, instance, **kwargs):
    if instance.status == 'p':
        agency.xml.removeUrlFromSiteMap(instance.pk)
        # Here only RealEstate model
        # change to receiver_with_multiple_senders and add "if isinstance(instance, Land):"
        agency.xml.remove_from_all_feeds(instance.pk)


models.signals.post_delete.connect(remove_from_xml, sender=RealEstate)


def receiver_with_multiple_senders(signal, senders, **kwargs):
    def decorator(receiver_function):
        for sender in senders:
            signal.connect(receiver_function, sender=sender, **kwargs)
        return receiver_function
    return decorator


@receiver_with_multiple_senders(models.signals.post_delete, models_with_image)
def delete_image_post_object(sender, instance, **kwargs):
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


@receiver_with_multiple_senders(models.signals.pre_save, models_with_default_image_height)
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
        if isinstance(instance, Land):
            agency.xml.update_all_feeds(instance)
        if old_status == 'a':
            link = 'https://высота-крым.рф/' + \
                str(instance.pk) + instance.description_page + '/'
            agency.xml.addUrlToSiteMap(link, instance.pk)
    elif old_status == 'p':
        agency.xml.removeUrlFromSiteMap(instance.pk)
        if isinstance(instance, Land):
            agency.xml.remove_from_all_feeds(instance.pk)

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
        agency.xml.addUrlToSiteMap(link, instance.pk)
        if isinstance(instance, Land):
            agency.xml.add_to_all_feeds(instance)
