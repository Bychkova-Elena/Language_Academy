# Проект: «🌐Сайт для учителя английского языка»

Личный кабинет для учителя и ученика, в котором они могут удобно давать и отслеживать домашнее задание, вести список групп и платить за обучение

# 📄Требования

| Технология  | Версия  |
| ----------- | ------- |
| Python      |         |

# 💿Установка проекта

1. Создать виртуальное окружение `pyhton -m venv <название окружения>`
3. Убрать отслеживание папки окружения гитом: создать файл .gitignore в папке окружения с контентом `*`
4. Активировать виртуальное окружение `./<название окружения>/Scripts/activate.bat`
5. Установить зависимости `pip install -r requirements.txt`
6. Применить миграции `python manage.py migrate`
7. Создать супер пользователя `python manage.py createsuperuser`


# 🚀Запуск проекта

`python manage.py runserver` Запустит сервер на 8000 порте. Для доступа в админку перейдите на /admin/ и укажите те логин и пароль, которые указывали при создание супер пользователя

# Возможные ошибки и способы их исправления.
1. `django.db.migrations.exceptions.NodeNotFoundError: Migration education.0001_initial dependencies reference nonexistent parent node...`

Исправление ошибки:
- Удаление файла education/0001_initial.py;
- Удаление бд (файла db.sqlite3);
- Выполнение команды `python manage.py makemigrations`;
- Выполнение команды `python manage.py migrate`.



