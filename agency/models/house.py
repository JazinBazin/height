from django.db import models
from .real_estate import RealEstate


class House(RealEstate):
    class Meta:
        verbose_name = 'дом/дачу'
        verbose_name_plural = 'Дома и дачи'

    description_page = 'house_description'

    number_of_rooms = models.SmallIntegerField(
        'Количество комнат'
    )

    number_of_floors = models.SmallIntegerField(
        'Количество этажей'
    )

    house_type = models.CharField(
        'Тип жилья',
        max_length=1,
        choices=(
            ('h', 'Дом'),
            ('c', 'Дача')),
        default='h'
    )

    decoration = models.CharField(
        'Отделка',
        max_length=100,
        blank=True
    )
