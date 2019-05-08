from django.db import models


class Service(models.Model):
    class Meta:
        verbose_name = 'услугу'
        verbose_name_plural = 'Услуги'
        ordering = ['order_number']

    headline = models.CharField('Заголовок', max_length=200)

    order_number = models.SmallIntegerField(
        'Порядковый номер',
        default=1
    )

    def __str__(self):
        return self.headline


class ServiceListItem(models.Model):
    class Meta:
        verbose_name = 'пункт списка'
        verbose_name_plural = 'Пункты списка'

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='list_items')
    text = models.TextField('Пункт списка')

    def __str__(self):
        return ''
