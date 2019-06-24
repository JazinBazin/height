from django.db import models
from .real_estate import RealEstate


class Land(RealEstate):
    class Meta:
        verbose_name = 'земельный участок'
        verbose_name_plural = 'Земельные участки'

    description_page = 'land_description'

    lot_type = models.CharField(
        'Тип участка',
        max_length=1,
        choices=(('i', 'ИЖС'),
                 ('a', 'Сельхозназначения'),
                 ('g', 'Садоводство'),
                 ('l', 'ЛПХ')),
        default='i',
        db_index=True
    )
