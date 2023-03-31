from rest_framework import viewsets

from reviews.models import Genre, Category, Title
from .serializers import (GenreSerializer, CategorySerializer,
                          TitleReadOnlySerializer, TitleWriteSerializer)
from .mixins import MixinGenresCategories


class GenreViewSet(MixinGenresCategories):
    """
    Получение списка жанров;
    Создание жанра;
    Удаление жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class CategoryViewSet(MixinGenresCategories):
    """
    Получение списка категорий;
    Создание категории;
    Удаление категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка и одного произведения;
    Создание произведения;
    Обновление произведения;
    Удаление произведения.
    """
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if 'retrieve' == self.action == 'list':
            return TitleReadOnlySerializer
        return TitleWriteSerializer
