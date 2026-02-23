from os import path
import hashlib
import struct

from Crypto.Cipher import AES

SECTOR_SIZE = 512

def essiv_sha256(current_sector_number: int, iv_generation_key: bytes) -> bytes:
    sector_number = struct.pack('<I', current_sector_number) + bytes(b'\x00' * 12) #Упаковываем номер сектора в 256-битный int
    
    cipher = AES.new(iv_generation_key, AES.MODE_ECB)
    return cipher.encrypt(sector_number)                                           #Генерируем iv
    
start_sector_number = 324
input_data_path = "C:\\CTF Tasks\\Task 1\\Condition\\encrypted_data.dump"
output_data_path = "C:\\CTF Tasks\\Task 1\\Answer\\data.dump_test"
master_key = b'\xad\x1b\x48\x56\x65\x3d\x9f\x1e\xdc\x8a\x3c\x3f\xda\xdf\xec\x53'  

with open(input_data_path, 'rb') as input_data:

    with open(output_data_path, 'wb') as output_data:
        
        final_sector_number = (path.getsize(input_data_path) // 512 + start_sector_number)  
        iv_generation_key = hashlib.sha256(master_key).digest()                   #Создаем ключ генерации iv

        for i in range(start_sector_number, final_sector_number):
            data = input_data.read(SECTOR_SIZE)

            iv = essiv_sha256(i, iv_generation_key)                               #Генерируем iv для текущего сектора
            cipher = AES.new(master_key, AES.MODE_CBC, iv=iv)
         

            output_data.write(cipher.decrypt(data))                               #Расшифровываем и записываем сектор

    output_data.close()

input_data.close()