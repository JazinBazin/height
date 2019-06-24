from django.db import models
from . import District, PopulatedArea


class RealEstate(models.Model):

    class Meta:
        ordering = ['-creation_date']

    status = models.CharField(
        'Статус',
        max_length=1,
        choices=(('p', 'Опубликовано'),
                 ('a', 'В архиве')),
        default='p',
        db_index=True
    )

    is_best_offer = models.BooleanField(
        'Лучшее предложение',
        choices=((True, 'Да'),
                 (False, 'Нет')),
        default=False,
        db_index=True
    )

    headline = models.CharField(
        'Заголовок',
        max_length=100,
    )

    description = models.TextField(
        'Описание'
    )

    image = models.ImageField(
        'Титульное изображение',
        upload_to='agency/images/real_estate_titles'
    )

    thumbnail = models.ImageField(
        'Миниатюра',
        upload_to='agency/images/real_estate_thumbnail_titles',
    )

    vendor_code = models.CharField(
        'Артикул',
        max_length=100,
        unique=True
    )

    transaction_type = models.CharField(
        'Тип сделки',
        max_length=1,
        choices=(
            ('p', 'Продажа'),
            ('r', 'Аренда'),
            ('e', 'Обмен')),
        default='p'
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Район',
    )

    populated_area = models.ForeignKey(
        PopulatedArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Населённый пункт',
    )

    address = models.CharField(
        'Адрес',
        max_length=200
    )

    phone = models.CharField(
        'Номер телефона владельца',
        max_length=100
    )

    price = models.PositiveIntegerField(
        'Цена',
    )

    currency = models.CharField(
        'Валюта',
        max_length=1,
        choices=(
            ('r', '₽'),
            ('d', '$'),
            ('e', '€')),
        default='r'
    )

    area = models.DecimalField(
        'Общая площадь',
        max_digits=10,
        decimal_places=6
    )

    area_units = models.CharField(
        'Единицы измерения площади',
        max_length=1,
        choices=(
            ('m', 'м²'),
            ('h', 'га'),
            ('a', 'сотки')),
        default='m'
    )

    documents = models.CharField(
        'Документы',
        max_length=100,
        blank=True
    )

    last_edit_date = models.DateTimeField(
        'Дата последнего редактирования',
        auto_now=True
    )

    creation_date = models.DateTimeField(
        'Дата создания объявления',
        auto_now_add=True
    )

    cadastral_number = models.CharField(
        'Кадастровый номер',
        max_length=100,
        blank=True
    )

    haggle = models.BooleanField(
        'Торг',
        choices=((True, 'Да'),
                 (False, 'Нет')),
        default=True,
    )

    mortgage = models.BooleanField(
        'Ипотека',
        choices=((True, 'Есть'),
                 (False, 'Нет')),
        default=True,
    )

    def __str__(self):
        return self.headline


class RealEstateImage(models.Model):
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    real_estate = models.ForeignKey(
        RealEstate,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        'Файл',
        upload_to='agency/images/real_estate_images'
    )

    thumbnail = models.ImageField(
        'Миниатюра',
        upload_to='agency/images/real_estate_thumbnail_images',
    )

    def __str__(self):
        return ''
