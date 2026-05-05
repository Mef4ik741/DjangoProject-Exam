from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import User
from articles.models import Article, Bookmark


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Имя пользователя уже занято')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email уже используется')
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Регистрация успешна')
        return redirect('home')
    return render(request, 'users/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_banned:
                messages.error(request, 'Ваш аккаунт заблокирован')
                return redirect('login')
            login(request, user)
            messages.success(request, 'Вы вошли в систему')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return redirect('login')
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('home')


@login_required
def profile(request, pk=None):
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user
    articles = Article.objects.filter(author=user, status='published')
    bookmarks = Bookmark.objects.filter(user=user).select_related('article')
    context = {
        'profile_user': user,
        'articles': articles,
        'bookmarks': bookmarks,
    }
    return render(request, 'users/profile.html', context)


@login_required
def authors(request):
    authors_list = User.objects.filter(articles__status='published').distinct()
    context = {
        'authors': authors_list,
    }
    return render(request, 'users/authors.html', context)


@login_required
def ban_user(request, pk):
    if not request.user.can_ban_users():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, 'Нельзя забанить себя')
        return redirect('home')
    if user.is_super_admin() and not request.user.is_super_admin():
        messages.error(request, 'Нельзя забанить супер админа')
        return redirect('home')
    user.is_banned = True
    user.save()
    messages.success(request, f'Пользователь {user.username} забанен')
    return redirect('home')


@login_required
def unban_user(request, pk):
    if not request.user.can_ban_users():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    user = get_object_or_404(User, pk=pk)
    user.is_banned = False
    user.save()
    messages.success(request, f'Пользователь {user.username} разбанен')
    return redirect('home')


@login_required
def promote_user(request, pk):
    if not request.user.can_assign_admins():
        messages.error(request, 'Недостаточно прав')
        return redirect('home')
    user = get_object_or_404(User, pk=pk)
    if user.role == 'user':
        user.role = 'admin'
        user.save()
        messages.success(request, f'Пользователь {user.username} назначен админом')
    else:
        messages.error(request, 'Нельзя назначить админом')
    return redirect('home')
