from django.db import models


class Contact(models.Model):
    class Meta:
        verbose_name = 'контактные данные'
        verbose_name_plural = 'Контактные данные'

    address = models.CharField('Адрес', max_length=200)
    email = models.EmailField('Почта')
    working_days_and_time = models.CharField(
        'Рабочие дни и время', max_length=100)
    working_break = models.CharField('Перерыв', max_length=100)

    def __str__(self):
        return 'Контактные данные агенства недвижимости "Высота"'


class ContactPhone(models.Model):
    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'

    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='phones')
    phone = models.CharField('Номер телефона', max_length=100)

    def __str__(self):
        return ''
