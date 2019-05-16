from django.db import models


class Certificate(models.Model):
    class Meta:
        verbose_name = 'сертификат'
        verbose_name_plural = 'Сертификаты'
        ordering = ['order_number']

    image = models.ImageField(
        'Изображение',
        upload_to='agency/images/certificates'
    )

    headline = models.CharField(
        'Заголовок',
        max_length=100
    )

    text = models.TextField(
        'Описание'
    )

    order_number = models.SmallIntegerField(
        'Порядковый номер',
        default=1
    )

    def __str__(self):
        return self.headline
