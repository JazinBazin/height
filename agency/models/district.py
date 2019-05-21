from django.db import models


class District(models.Model):
    class Meta:
        verbose_name = 'район'
        verbose_name_plural = 'Районы'
        ordering = ['name']

    name = models.CharField(
        'Название',
        max_length=100,
        db_index=True
    )

    def __str__(self):
        return self.name
