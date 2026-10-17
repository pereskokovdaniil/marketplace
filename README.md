# Маркетплейс

Веб-приложение для размещения и продажи товаров от независимых продавцов.

## Функционал
- Регистрация и вход с разделением ролей (покупатель, продавец)
- Каталог товаров с поиском и фильтрацией по категориям
- Корзина и оформление заказов
- История заказов
- Оценки на товары с рейтингом
- Добавление и редактирование товаров продавцом

## Технологии
- Python 3.14
- Django 6.0
- PostgreSQL
- HTML, CSS, JavaScript

## Запустить локально

### Клонировать репозиторий
```bash
git clone https://github.com/pereskokovdaniil/marketplace.git
cd marketplace
```

### Установить зависимости и создать виртуальное окружение
```bash
uv sync
```

### Создать файл .env на основе .env.example
```bash
cp .env.example .env
```
- Открыть .env и заполнить своими данными

### Применить миграции
```bash
uv run python manage.py migrate
```

### Создать суперпользователя для входа в админку
```bash
uv run python manage.py createsuperuser
```

### Запустить сервер
```bash
uv run python manage.py runserver
```

### Открыть в браузере
```
http://127.0.0.1:8000/
```

## Автор
[pereskokovdaniil](https://github.com/pereskokovdaniil)