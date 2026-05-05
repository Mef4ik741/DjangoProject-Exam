from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/', views.profile, name='profile_detail'),
    path('authors/', views.authors, name='authors'),
    path('ban/<int:pk>/', views.ban_user, name='ban_user'),
    path('unban/<int:pk>/', views.unban_user, name='unban_user'),
    path('promote/<int:pk>/', views.promote_user, name='promote_user'),
]
