# WriteUp
Общее описание того, как работает FDE:<br>
https://xakep.ru/2017/01/13/cryptodroid-full-disk-file-based-encryption/<br>
https://source.android.com/docs/security/features/encryption/full-disk?hl=ru<br>
В crypt_mnt_ftr.bin по смещению 0x24 обнаруживаем то, что в нашем случае использовался режим шифрования aes-cbc-essiv:sha256. Так как, длина мастер ключа равна 128 бит, то в схеме используется aes-128. Реализовываем расшифрование и получаем data.dump. Далее остается лишь обрезать лишние байты и извлечь флаг.

Примерный код для расшифровки дампа: decrypt.py