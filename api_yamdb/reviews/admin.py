from django.contrib import admin
from .models import Genre, Category


@admin.register(Genre)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]


@admin.register(Category)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
