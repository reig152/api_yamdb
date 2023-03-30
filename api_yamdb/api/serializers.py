from rest_framework import serializers
from reviews.models import Genre, Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id', )
