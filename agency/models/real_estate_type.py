from django.db import models


class RealEstateType(models.Model):
    class Meta:
        verbose_name = 'вид недвижимого имущества'
        verbose_name_plural = 'Виды недвижимого имущества'
        ordering = ['order_number']

    image = models.ImageField(
        'Изображение',
        upload_to='agency/images/real_estate_types'
    )

    headline = models.CharField(
        'Заголовок',
        max_length=100
    )

    link = models.CharField(
        'Ссылка',
        max_length=100
    )

    order_number = models.SmallIntegerField(
        'Порядковый номер',
        default=1
    )

    def __str__(self):
        return self.headline
