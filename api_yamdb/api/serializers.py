from rest_framework import serializers
from reviews.models import Genre, Category, Title


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
    """Сериализатор для записи произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
