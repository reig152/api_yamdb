from django.contrib import admin
from .models import Genre, Category, Title, Review, Comment


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'title',
        'text',
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'review',
        'text',
    ]
