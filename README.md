# Foodgram - Дипломный проект Яндекс.Практикум

***
## Развёрнутый и запущенный проект можно посмотреть по адресу http://51.250.23.112/
![example workflow](https://github.com/shtrihh88/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
***

## Используемые технологии:

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

***
## Описание: 
***
 «Продуктовый помощник». Онлайн-сервис и API для него.
 На этом сервисе пользователи смогут публиковать рецепты,
 подписываться на публикации других пользователей, добавлять
 понравившиеся рецепты в список «Избранное», а перед походом
 в магазин скачивать сводный список продуктов, необходимых для
 приготовления одного или нескольких выбранных блюд.
 
***

## Установка проекта на локальном компьютере

***

### 1. Подготовить docker согласно официальной [инструкции](https://docs.docker.com/engine/install/).

### 2.Клонировать репозиторий, перейти в папку проекта:
```
git clone https://github.com/shtrihh88/foodgram-project-react
cd foodgram-project-react
```

### 3.В папке infra проекта создать файл .env.
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<имя пользователя>
POSTGRES_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<SECRET_KEY_Django>
```

### 4.Перейти в папку infra, создать и применить миграции, собрать статику, создать суперпользователя:
```
docker-compose up -d --build
docker-compose exec backend python manage.py makemigrations --noinput
docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```

### 5. Загрузить тестовые данные в базу:
```
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags
```

***
### Ссылка на DockerHub:
https://hub.docker.com/repository/docker/shtrihh88/api_foodgram

### Об авторе
Громов Александр, github.com/shtrihh88, shtrihh88@gmail.com