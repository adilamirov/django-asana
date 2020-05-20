# Как запустить проект

Укажите свой Private Access Token и GID Workspace'а в файле `.env`.

Далее можно воспользоваться `docker-compose up`

При запуске сервис автоматически заберет всех пользователей из указанного Workspace и добавит в базу.
При необходимости можно автоматически добавлять новых пользователей запуском
`docker exec <CONTAINER_NAME> python manage.py loadusers`.

Сервис будет доступен по адресу http://localhost:8080/admin/

Стандартный логин/пароль - admin/admin
