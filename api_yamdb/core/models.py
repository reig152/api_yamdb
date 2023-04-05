from django.db import models


class NameAndSlug(models.Model):
    """Абстрактная модель для создания имени и слага"""
    name = models.CharField(
        max_length=256,
        verbose_name='Полное имя'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Сокращенное имя'
    )

    class Meta:
        # указываем абстрактную модель
        abstract = True
