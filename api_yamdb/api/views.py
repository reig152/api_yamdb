from rest_framework import viewsets

from reviews.models import Genre, Category
from .serializers import GenreSerializer, CategorySerializer
from .mixins import MixinGenresCategories


class GenreViewSet(MixinGenresCategories):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class CategoryViewSet(MixinGenresCategories):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
