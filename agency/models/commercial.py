from django.db import models
from .real_estate import RealEstate


class Commercial(RealEstate):
    class Meta:
        verbose_name = 'коммерческую недвижимость'
        verbose_name_plural = 'Коммерческая недвижимость'

    description_page = 'commercial_description'

    commercial_type = models.CharField(
        'Тип коммерческой недвижимости',
        max_length=100
    )

    number_of_rooms = models.SmallIntegerField(
        'Количество комнат',
        blank=True,
        null=True
    )

    number_of_floors = models.SmallIntegerField(
        'Количество этажей',
        blank=True,
        null=True
    )

    decoration = models.CharField(
        'Отделка',
        max_length=100,
        blank=True
    )
