# Категория | Имя задачи
Web | != SQL

# Информация
Классическая NoSQL-инъекция в Express + Mongoose: `findOne({user: req.body.user, pass: req.body.pass})` вместе с `express.urlencoded({extended: true})` позволяет передавать операторы MongoDB через параметры вида `user[$gt]`.

# Деплой
Задача использует MongoDB, деплой через docker-compose:

```bash
cd deploy
docker compose up --build
```

Сервис будет доступен на `http://localhost:8080/`.

# Выдать участникам
Нет файлов (участникам выдаётся только ссылка на веб-сервис).

# Описание задачи
Один из главарей DedSec создал страничку, где хранит крайне важную информацию. Но мы не знаем его ник! Найди его.

# Флаг
SplitCTF{NoSQLInjectionExample}
