from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Супер Админ'),
        ('admin', 'Админ'),
        ('user', 'Пользователь'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_banned = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def is_super_admin(self):
        return self.role == 'superadmin'

    def is_admin(self):
        return self.role in ('superadmin', 'admin')

    def can_moderate_articles(self):
        return self.role in ('superadmin', 'admin')

    def can_ban_users(self):
        return self.role in ('superadmin', 'admin')

    def can_assign_admins(self):
        return self.role == 'superadmin'

    def __str__(self):
        return self.username
