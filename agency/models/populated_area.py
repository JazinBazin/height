from django.db import models


class PopulatedArea(models.Model):
    class Meta:
        verbose_name = 'населённый пункт'
        verbose_name_plural = 'Населённые пункты'
        ordering = ['name']

    name = models.CharField(
        'Название',
        max_length=100,
        db_index=True
    )

    is_city = models.BooleanField(
        'Это город?',
        choices=((True, 'Да'),
                 (False, 'Нет')),
        default=False,
    )

    def __str__(self):
        return self.name
