# api_yamdb 

**api_yamdb** - проект, который собирает **отзывы** пользователей на **произведения**. Сами произведения в **api_yamdb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка».
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.

## 📝 **Ключевые собенности:**

🔸 Система регистрации при помощи JWT-токена

🔸 Пользовательские роли: **Аноним**, **Аутентифицированный пользователь**, **Модератор**, **Администратор**

🔸 Категории **categories** и жанры **genres** произведений

🔸 Возможность оставлять отзывы **reviews** с оценками и комментарии **comments** к ним пользователями **users**

## Технологический стек
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=cd5c5c)](https://www.python.org/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=0095b6)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/-SQLite-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=cd5c5c)](https://www.sqlite.org/)


## 🚀 Запуск проекта: 

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SFGRonk/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## База данных:

Для загрузки данных, получаемых вместе с проектом, используйте management-команду, добавляющую данные в БД через Django ORM. Предварительно надо удалить базу: если у вас уже есть файл **db.sqlite3**, удалите его. Затем подготовьте и проведите миграции:
```
python manage.py makemigrations
python manage.py migrate
```
Затем  management-команда:
```
python manage.py import
```
Результатом успешного импорта данных из файлов csv в БД будет строка, выведенная в терминал:
```
$ Данные успешно загружены
```

Запустить проект:

```
python3 manage.py runserver
```
## 📋 Документация к API:

После запуска dev-сервера доступ к подробной документация по адресу:
 <http://127.0.0.1:8000/redoc/>

### Регистация нового пользователя:
```POST /api/v1/auth/signup/```


```json
{
  "email": "string",
  "username": "string"
}

```

### Получение JWT-токена:

```POST /api/v1/auth/token/```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

## 💻 Примеры запросов:
### Для авторизованных пользователей:
➕ **Добавление категории:**
- Права доступа: **Администратор**.

```POST /api/v1/categories/```

```json
{
  "name": "string",
  "slug": "string"
}
```

➖ **Удаление категории:**
- Права доступа: **Администратор.**

```DELETE /api/v1/categories/{slug}/```

➕ **Добавление жанра:**

- Права доступа: **Администратор.**

```POST /api/v1/genres/```

```json
{
  "name": "string",
  "slug": "string"
}
```

➖ **Удаление жанра:**

- Права доступа: **Администратор**.

```DELETE /api/v1/genres/{slug}/```


🔄 **Обновление публикации:**

```PUT /api/v1/posts/{id}/```

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

➕ **Добавление произведения:**

- Права доступа: **Доступ без токена**.

```GET /api/v1/titles/{titles_id}/```

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

✋ **Получение данных своей учетной записи:**

- Права доступа: **Любой авторизованный пользователь**.

```GET /api/v1/users/me/ - Получение данных своей учетной записи```


### 😎 Авторы проекта:
#### Ekaterina Tarasenko
```Github:```<https://github.com/kora21>
#### Денис Ясенев
```Github:```<https://github.com/SFGRonk>
#### Дмитрий Исаков
```Github:```<https://github.com/isadmiale>
