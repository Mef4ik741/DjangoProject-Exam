from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('popular/', views.popular, name='popular'),
    path('category/<slug:slug>/', views.category_articles, name='category_articles'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('article/<int:pk>/rate/', views.rate_article, name='rate_article'),
    path('article/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('moderate/', views.moderate_articles, name='moderate_articles'),
    path('article/<int:pk>/approve/', views.approve_article, name='approve_article'),
    path('article/<int:pk>/reject/', views.reject_article, name='reject_article'),
]
