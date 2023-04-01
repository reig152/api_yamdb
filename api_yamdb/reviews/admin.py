from django.contrib import admin
from .models import Genre, Category, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'year',
        'description',
    ]
