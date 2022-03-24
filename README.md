# Проект: «Сайт для учителя английского языка»

Личный кабинет для учителя и ученика, в котором они могут удобно давать и отслеживать домашнее задание, вести список групп и платить за обучение

# 📄Требования

| Технология  | Версия  |
| ----------- | ------- |
| Python      | 3.9     |

# Установка и запуск виртуального окружения. Установка пакетов

1. `python -m venv venv` - создание виртуального окружения.
2. `.\venv\scripts\activate` - активация виртуального окружения.
3. `pip install -r requirements.txt` - установка всех перечисленных в файле требований.

# 🚀Запуск проекта

`python manage.py runserver` - запуск проекта.

Проект будет доступен по адрессу: http://127.0.0.1:8000/

# Возможные ошибки и способы их исправления.
1. `django.db.migrations.exceptions.NodeNotFoundError: Migration education.0001_initial dependencies reference nonexistent parent node...`
    
    Исправление ошибки:
    - Удаление файла education/0001_initial.py;
    - Удаление бд (файла db.sqlite3);
    - Выполнение команды `python manage.py makemigrations`;
    - Выполнение команды `python manage.py migrate`.



