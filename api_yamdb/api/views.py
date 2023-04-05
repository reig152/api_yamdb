from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from rest_framework import permissions, status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from . import serializers
from reviews.models import Genre, Category, Title, Review
from .mixins import MixinGenresCategories
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrAdminOrReadOnly)
from .filters import TitleFilter

User = get_user_model()


class GenreViewSet(MixinGenresCategories):
    """
    Получение списка жанров;
    Создание жанра;
    Удаление жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
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
    serializer_class = serializers.CategorySerializer
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
            return serializers.TitleReadOnlySerializer
        return serializers.TitleWriteSerializer


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


class UserAdminViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления пользователями с правом доступа для администратора.
    Разрешённые методы запроса:
    1. Получение списка пользователей,
    2. Добавление пользователя,
    3. Получение пользователя по username,
    4. Частичное обновление пользователя по username (PATCH)
    5. Удаление пользователя.
    Метод 'PUT' недоступен. Реализован поиск по username.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserAdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = View.http_method_names
    http_method_names.remove('put')


@api_view(['GET', 'PATCH'])
@permission_classes((permissions.IsAuthenticated,))
def users_me(request):
    """
    Функция для управления своей учётной записью.
    Доступ для авторизованных пользователей.
    Разрешённые методы запроса:
    1. GET - получение своих данных,
    2. PATCH - редактирование данных.
    Редактирование поля 'role' не доступно.
    """
    user = request.user
    if request.method == 'PATCH':
        serializer = serializers.UserMeSerializer(user,
                                                  data=request.data,
                                                  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = serializers.UserMeSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
