from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Genre, Category, Title, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id', )


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True,
                            read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи произведений.
    Добавление поля -rating для получения средней оценки"""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return round(rating)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = (
            'id',
            'author',
            'title',
            'pub_date'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
        read_only_fields = (
            'id',
            'author',
            'review',
            'pub_date'
        )
