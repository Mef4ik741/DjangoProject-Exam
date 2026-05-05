from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_articles', kwargs={'slug': self.slug})


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('pending', 'На модерации'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating_avg = models.FloatField(default=0.0)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    def update_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.rating_avg = round(ratings.aggregate(models.Avg('value'))['value__avg'], 2)
        else:
            self.rating_avg = 0.0
        self.save(update_fields=['rating_avg'])


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.user.username} -> {self.article.title}: {self.value}'


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'

    def __str__(self):
        return f'{self.user.username} -> {self.article.title}'
