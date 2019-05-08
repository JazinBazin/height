from django.db import models


class Advantage(models.Model):
    class Meta:
        verbose_name = 'вид приеимущества'
        verbose_name_plural = 'Преимущества'
        ordering = ['order_number']

    image = models.ImageField(
        'Изображение',
        upload_to='agency/images/advantages'
    )

    headline = models.CharField(
        'Заголовок',
        max_length=100
    )

    order_number = models.SmallIntegerField(
        'Порядковый номер',
        default=1
    )

    def __str__(self):
        return self.headline
