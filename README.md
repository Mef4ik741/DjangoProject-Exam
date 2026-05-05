# Новостной сайт (Хабр-подобный)

## Описание

Полнофункциональный новостной сайт с системой ролей, модерацией статей, оценками и закладками.

## Роли пользователей

- **Супер Админ**: может всё, назначает админов
- **Админ**: модерирует статьи, банит пользователей
- **Пользователь**: создаёт статьи (с модерацией), управляет своими статьями
- **Гость**: только чтение статей

## Категории

- Backend
- Frontend
- AI
- Cyber Security
- Cyber Sport
- Game Development

## Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Миграции (SQLite используется по умолчанию)
python manage.py migrate

# Создание суперпользователя
python manage.py shell -c "
from users.models import User
User.objects.create_superuser('superadmin', 'admin@example.com', 'admin123', role='superadmin')
"

# Создание категорий
python manage.py shell -c "
from articles.models import Category
categories = ['Backend', 'Frontend', 'AI', 'Cyber Security', 'Cyber Sport', 'Game Development']
for name in categories:
    slug = name.lower().replace(' ', '-')
    Category.objects.get_or_create(name=name, defaults={'slug': slug})
"

# Запуск сервера
python manage.py runserver
```

## Развёртывание на Railway

1. Установите переменную окружения:
   ```
   USE_POSTGRES=1
   ```

2. Railway использует предоставленные PostgreSQL credentials:
   - Host: postgres.railway.internal
   - Port: 5432
   - Database: railway
   - User: postgres
   - Password: niNTUMFHhxpojeprqrstKEpKXWlTvzVu

3. Для медиа-файлов используется Cloudinary:
   - Cloud Name: duygiwcsz
   - API Key: 149696794782919
   - API Secret: DlKE6PeZb9oCXAqAFPndLYTuFvQ

## Данные для входа

**Super Admin:**
- Username: `superadmin`
- Password: `admin123`

## Функционал

- Регистрация и авторизация
- Создание статей (требует модерации)
- Оценка статей (1-5)
- Закладки
- Просмотр по категориям
- Популярные статьи (рейтинг 4+)
- Модерация статей админами
- Бан/разбан пользователей
- Назначение админов (супер админом)
