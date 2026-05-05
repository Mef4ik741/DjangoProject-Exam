from django.contrib import admin
from .models import Category, Article, Rating, Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'rating_avg', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    date_hierarchy = 'created_at'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'value', 'created_at']
    list_filter = ['value', 'created_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'created_at']
    list_filter = ['created_at']
