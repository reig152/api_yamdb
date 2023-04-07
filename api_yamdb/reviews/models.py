from django.db import models
from core.models import NameAndSlug
from users.models import CustomUser
from .validators import max_value_current_year
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(NameAndSlug):
    """Модель категории."""
    pass


class Genre(NameAndSlug):
    """Модель жанра."""
    pass


class TitleGenre(models.Model):
    """Модель взаимосвязи произведения и жанров."""
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True
    )


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[max_value_current_year],
        db_index=True
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through=TitleGenre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )


class Review(models.Model):
    """Модель отзывов"""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)]
    )

    class Meta:
        default_related_name = 'reviews'
        unique_together = ('author', 'title',)


class Comment(models.Model):
    """Модель комментариев"""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'
