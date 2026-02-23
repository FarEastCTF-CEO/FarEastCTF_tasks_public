import base64
from random import randint

def encode_to_random_baseX(flag, N, filepath):

    encode_str = flag.encode()
    print()
    
    for _ in range(N):
        basenum = randint(2, 5)
        if basenum % 5 == 0: 
            encode_str = base64.b16encode(encode_str)
            print("Encoded base16...")
        elif basenum % 4 == 0: 
            encode_str = base64.b32encode(encode_str)
            print("Encoded base32...")
        elif basenum % 3 == 0: 
            encode_str = base64.b64encode(encode_str)
            print("Encoded base64...")
        else: 
            encode_str = base64.b85encode(encode_str)
            print("Encoded base85...")

    with open(filepath, "w") as file:
        file.write(encode_str.decode())

flag = input("\nEnter the flag: ")
N = int(input("Enter the number of iterations: "))
filepath = input("Enter the path to the file: ")

encode_to_random_baseX(flag, N, filepath)