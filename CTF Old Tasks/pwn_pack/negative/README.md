# Категория | Имя задачи
Pwn | negative

# Информация
Задача на переполнение int32: подобрать положительное x, чтобы (int32)(a+x)==b.

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t negative .
docker run -d -p 40001:40001 negative
```

# Выдать участникам
- public/negative
- public/negative.c

# Описание задачи
Разработчик уверен, что отрицательное число нельзя получить из суммы с положительным x. Докажи обратное.

# Флаг
CTF{negative_int_overflow}
