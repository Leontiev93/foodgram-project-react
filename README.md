
# Foodgram - продуктовый помощник
### Описание
Продуктовый помощник это отличное решение для любого человека который любит вкусно покушать. В данном приложении возможно просматривать, создавать, редактировать а так же добавлять в избранное и в карзину рецепты.
Проект доступен по адресу  http://158.160.107.119/ или http://product-helper.zapto.org
### Технологии
-Python 3.10

-Django 4.2

-Django REST framework 3.14

-Docker

-Docker-compose

-Gunicorn

-NGINX

-PostgreSQL

-Yandex Cloud

-Continuous Integration Continuous Deployment

### Как запустить проект
- Клонировать репозиторий:
```
git@github.com:Leontiev93/foodgram-project-react.git
```

- Установить на сервере Docker, Docker Compose:

```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

- Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra а так же папку docs из корневой папки infra (на сервере создать папку foodgram):

```
scp docker-compose.yml nginx.conf username@IP:/home/username/foodgram   # username - имя пользователя на сервере    
                                                                        # IP - публичный IP сервера
scp -r /docs username@IP:/home/username/foodgram                        # username - имя пользователя на сервере                                                 
                                                                        # IP - публичный IP сервера
```
Для успешного запуска в папке foodgram/ на сервере необходимо создать файл с расширением .env с следующим нполнением 


```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

- Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```


Для запуска через Docker образ на сервере, необходимо выполнить команду 

```
docker pull leontiev93/infra_web:v1.0
```
Выполните команду 
```
docker-compose up -d --build 
```
Проверьте запустились ли контейнеры
```
docker container ls
```
- После успешной сборки выполнить миграции:
```
sudo docker compose exec backend python manage.py migrate
```

- Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

- Собрать статику:
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

- Наполнить базу данных содержимым из файла ingredients.json:
```
sudo docker compose exec backend python manage.py load_data data/ingredients.json
```

- Для остановки контейнеров Docker:
```
sudo docker compose down -v      # с их удалением
sudo docker compose stop         # без удаления
```

### Запуск проекта на локальной машине:

- Клонировать репозиторий:
```
git@github.com:Leontiev93/foodgram-project-react.git
```

- В директории /infra файл создать файл .env и заполнить своими данными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ Django'
```

- После запуска проект будут доступен по адресу: [http://localhost/](http://localhost/)


- Документация будет доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)
## Техническое задание
### Описание workflow
* проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
* сборка и доставка докер-образа для контейнера web на Docker Hub
* автоматический деплой проекта на боевой сервер
### Базовые модели проекта
### Рецепт - все поля обязательны для заполнения
* Автор публикации (пользователь)
* Название
* Картинка
* Текстовое описание
* Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения
* Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных)
* Время приготовления в минутах
### Тег - все поля обязательны для заполнения и уникальны
* Название
* Цветовой HEX-код (например, #49B64E)
* Slug
### Ингредиент - все поля обязательны для заполнения
Данные об ингредиентах хранятся в нескольких связанных таблицах. В результате на стороне пользователя ингредиент должен описываться такими полями:
* Название
* Количество
* Единицы измерения
## Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым)
Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация
## Страница рецепта
На странице — полное описание рецепта
Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта
## Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя

## Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.
Сценарий поведения пользователя:
1. Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
2. Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
3. При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».
## Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.
Сценарий поведения пользователя:
1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
2. Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
3. При необходимости пользователь может удалить рецепт из избранного.
## Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.
Сценарий поведения пользователя:
1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
2. Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
3. При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).
При скачивании списка покупок ингредиенты в результирующем списке не должны дублироваться; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.
В результате список покупок может выглядеть так:
* Фарш (баранина и говядина) (г) — 600
* Сыр плавленый (г) — 200
* Лук репчатый (г) — 50
* Картофель (г) — 1000
* Молоко (мл) — 250
* Яйцо куриное (шт) — 5
* Соевый соус (ст. л.) — 8
* Сахар (г) — 230
* Растительное масло рафинированное (ст. л.) — 2
* Соль (по вкусу) — 4
* Перец черный (щепотка) — 3
## Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.
При фильтрации на странице пользователя должны фильтроваться только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.

## Регистрация и авторизация
### Обязательные поля для пользователя
* Логин
* Пароль
* Email
* Имя
* Фамилия
### Уровни доступа пользователей
* Гость (неавторизованный пользователь)
* Авторизованный пользователь
* Администратор
## Что могут делать неавторизованные пользователи
* Создать аккаунт
* Просматривать рецепты на главной
* Просматривать отдельные страницы рецептов
* Просматривать страницы пользователей
* Фильтровать рецепты по тегам
## Что могут делать авторизованные пользователи
* Входить в систему под своим логином и паролем
* Выходить из системы (разлогиниваться)
* Менять свой пароль
* Создавать/редактировать/удалять собственные рецепты
* Просматривать рецепты на главной
* Просматривать страницы пользователей
* Просматривать отдельные страницы рецептов
* Фильтровать рецепты по тегам
* Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов
* Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок
* Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок
## Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя
Плюс к этому он может:
* изменять пароль любого пользователя
* создавать/блокировать/удалять аккаунты пользователей
* редактировать/удалять любые рецепты
* добавлять/удалять/редактировать ингредиенты
* добавлять/удалять/редактировать теги
## Настройки админки
### Модели
* Вывести все модели с возможностью редактирования и удаления записей
### Модель пользователей:
* Добавить фильтр списка по email и имени пользователя
### Модель рецептов:
* В списке рецептов вывести название и автора рецепта
* Добавить фильтры по автору, названию рецепта, тегам
* На странице рецепта вывести общее число добавлений этого рецепта в избранное
### Модель ингредиентов:
* В список вывести название ингредиента и единицы измерения
* Добавить фильтр по названию
## Технические требования и инфраструктура
* Проект должен использовать базу данных PostgreSQL
* Код должен находиться в репозитории `foodgram-project-react`
* В Django-проекте должен быть файл `requirements.txt` со всеми зависимостями
* Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом должен быть запушен на Docker Hub
## Документация

Данные для входа в админ зону
http://158.160.107.119/admin/
* пользователь **admin**
* email **admin@yandex.ru**
* password **admin**

Подробная документация по проекту:
[https://127.0.0.1:3000/api/docs/](https://127.0.0.1:3000/api/docs/)

## Автор 

- [@Leontie93](https://github.com/Leontiev93) -- backend

