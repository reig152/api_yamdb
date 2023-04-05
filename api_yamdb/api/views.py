from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Category, Title, Review
from .serializers import (GenreSerializer, CategorySerializer,
                          TitleReadOnlySerializer, TitleWriteSerializer,
                          ReviewSerializer, CommentSerializer)
from .mixins import MixinGenresCategories
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrAdminOrReadOnly)
from .filters import TitleFilter


class GenreViewSet(MixinGenresCategories):
    """
    Получение списка жанров;
    Создание жанра;
    Удаление жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    search_fields = ['=name']
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]


class CategoryViewSet(MixinGenresCategories):
    """
    Получение списка категорий;
    Создание категории;
    Удаление категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    search_fields = ['=name']
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка и одного произведения;
    Создание произведения;
    Обновление произведения;
    Удаление произведения.
    """
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if 'retrieve' == self.action == 'list':
            return TitleReadOnlySerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получение списка и одного отзыва;
    Создание отзыва;
    Обновление отзыва;
    Удаление отзыва.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_queryset(self):
        pk = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        return title.reviews.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получение списка и одного комментария;
    Создание  комментария к отзыву;
    Обновление  комментария;
    Удаление  комментария.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_queryset(self):
        pk = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=pk)
        return review.comments.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=pk)
        serializer.save(author=self.request.user, review=review)
