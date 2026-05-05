from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import Category, Article, Rating, Bookmark
from .forms import ArticleForm
from users.models import User


def _paginate(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def home(request):
    articles_list = Article.objects.filter(status='published').select_related('author', 'category')
    articles = _paginate(request, articles_list)
    context = {
        'articles': articles,
        'title': 'Все статьи',
    }
    return render(request, 'articles/home.html', context)


def popular(request):
    articles_list = Article.objects.filter(status='published', rating_avg__gte=4).select_related('author', 'category')
    articles = _paginate(request, articles_list)
    context = {
        'articles': articles,
        'title': 'Популярное',
    }
    return render(request, 'articles/home.html', context)


def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles_list = Article.objects.filter(status='published', category=category).select_related('author', 'category')
    articles = _paginate(request, articles_list)
    context = {
        'articles': articles,
        'title': f'Категория: {category.name}',
        'category': category,
    }
    return render(request, 'articles/home.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.status != 'published' and not request.user.is_authenticated:
        messages.error(request, 'Статья не найдена')
        return redirect('home')
    if article.status != 'published' and not request.user.can_moderate_articles() and request.user != article.author:
        messages.error(request, 'Статья не найдена')
        return redirect('home')
    article.views_count += 1
    article.save(update_fields=['views_count'])
    user_rating = None
    is_bookmarked = False
    if request.user.is_authenticated:
        rating_obj = Rating.objects.filter(article=article, user=request.user).first()
        if rating_obj:
            user_rating = rating_obj.value
        is_bookmarked = Bookmark.objects.filter(article=article, user=request.user).exists()
    context = {
        'article': article,
        'user_rating': user_rating,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def article_create(request):
    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован')
        return redirect('home')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'pending'
            article.save()
            article.slug = slugify(f'{article.title}-{article.id}')
            article.save(update_fields=['slug'])
            messages.success(request, 'Статья отправлена на модерацию')
            return redirect('home')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ArticleForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author and not request.user.can_moderate_articles():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article, user=request.user)
        if form.is_valid():
            updated_article = form.save(commit=False)
            if not request.user.can_moderate_articles():
                updated_article.status = 'pending'
            updated_article.save()
            messages.success(request, 'Статья обновлена')
            return redirect('article_detail', pk=article.pk)
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ArticleForm(instance=article, user=request.user)
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/form.html', context)


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author and not request.user.can_moderate_articles():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена')
        return redirect('home')
    return render(request, 'articles/delete.html', {'article': article})


@login_required
def rate_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован')
        return redirect('article_detail', pk=pk)
    value = request.POST.get('value')
    if value and value.isdigit() and 1 <= int(value) <= 5:
        Rating.objects.update_or_create(
            article=article,
            user=request.user,
            defaults={'value': int(value)}
        )
        article.update_rating()
        messages.success(request, 'Оценка сохранена')
    return redirect('article_detail', pk=pk)


@login_required
def toggle_bookmark(request, pk):
    article = get_object_or_404(Article, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(article=article, user=request.user)
    if not created:
        bookmark.delete()
        messages.success(request, 'Удалено из закладок')
    else:
        messages.success(request, 'Добавлено в закладки')
    return redirect('article_detail', pk=pk)


@login_required
def bookmarks(request):
    bookmarks_list = Bookmark.objects.filter(user=request.user).select_related('article', 'article__author', 'article__category')
    context = {
        'bookmarks': bookmarks_list,
    }
    return render(request, 'articles/bookmarks.html', context)


@login_required
def moderate_articles(request):
    if not request.user.can_moderate_articles():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    articles = Article.objects.filter(status='pending').select_related('author', 'category')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/moderate.html', context)


@login_required
def approve_article(request, pk):
    if not request.user.can_moderate_articles():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    article = get_object_or_404(Article, pk=pk)
    article.status = 'published'
    article.save(update_fields=['status'])
    messages.success(request, 'Статья опубликована')
    return redirect('moderate_articles')


@login_required
def reject_article(request, pk):
    if not request.user.can_moderate_articles():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    article = get_object_or_404(Article, pk=pk)
    article.status = 'rejected'
    article.save(update_fields=['status'])
    messages.success(request, 'Статья отклонена')
    return redirect('moderate_articles')
