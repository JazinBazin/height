from django.db import models


class Description(models.Model):
    class Meta:
        verbose_name = 'описание'
        verbose_name_plural = 'О компании'
        ordering = ['order_number']

    headline = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Описание')

    order_number = models.SmallIntegerField(
        'Порядковый номер',
        default=1
    )

    def __str__(self):
        return self.headline
