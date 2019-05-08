from django.db import models
from .real_estate import RealEstate


class Apartment(RealEstate):
    class Meta:
        verbose_name = 'квартиру'
        verbose_name_plural = 'Квартиры'

    description_page = 'apartment_description'

    floor_number = models.SmallIntegerField(
        'Номер этажа'
    )

    number_of_floors = models.SmallIntegerField(
        'Этажность'
    )

    number_of_rooms = models.SmallIntegerField(
        'Количество комнат'
    )

    balcony = models.BooleanField(
        'Балкон',
        choices=(
            (True, 'Есть'),
            (False, 'Нет')),
        default=True
    )

    bathroom = models.CharField(
        'Санузел',
        max_length=1,
        choices=(
            ('c', 'Совмещённый'),
            ('s', 'Раздельный')),
        default='c'
    )

    decoration = models.CharField(
        'Отделка',
        max_length=100,
        blank=True
    )

    building_type = models.CharField(
        'Тип дома',
        max_length=100,
        blank=True
    )
