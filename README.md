# Платформа для обмена вещами (бартерная система)

Веб-приложение на Django для организации обмена вещами между пользователями.

## Функциональность

- Создание, редактирование и удаление объявлений
- Поиск и фильтрация объявлений
- Система обмена предложениями между пользователями
- REST API для работы с объявлениями и предложениями
- Авторизация пользователей

## Требования

- Python 3.8+
- Django 4+
- Остальные зависимости указаны в requirements.txt

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/sromanov103/Trade_Django.git
cd Trade_Django
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Тестирование

Для запуска тестов используйте:
```bash
pytest
```

## API документация

После запуска сервера, документация API доступна по адресу:
http://localhost:8000/api/schema/swagger-ui/ 
