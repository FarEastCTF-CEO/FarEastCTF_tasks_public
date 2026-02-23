from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_rsa_parameters(public_key_openssh):
    # Загружаем открытый ключ из формата OpenSSH
    public_key = serialization.load_ssh_public_key(
        public_key_openssh.encode('utf-8'),
        backend=default_backend()
    )

    # Получаем открытые числа e и m из открытого ключа
    public_numbers = public_key.public_numbers()
    e = public_numbers.e
    m = public_numbers.n

    return e, m

if __name__ == "__main__":
    # Ваш открытый ключ
    public_key_openssh = "ssh-rsa AAAAB3NzaC1yc2EAAAEBAPOVnZeOAuufBt7z8zXY+K/XYJlR3axgtxS2wirw+pEvIQs0IGvSSpYBx430oCdfEH/Tq1UtlQV+uTTnG93NcEXCSxhYe4yPz1rdTF2D8Md8lNycUMvkOOK2e6/TFjO2qvF4HZDDrW8D0DezMhgBsjVG1IPmfiYGf3siNH3bwMLVks6BTL9d/MwUFDfxTgs5kPiAYeXwuuXwHj+nDbDpYF58/VdenIHv7sUpwz/ZA3og/YrNUTrJY3doMT5j+YOK41Ec3QqaK1FvIUjI1HWjYKBjWUSXOe7NJRq7QrAUVz5Dny+kVzVXslaZ/8EeYxzo7pdahuficrz192qTRQNI/j8AAAEBA2cZjWtWFOlYE63Y8ipHF7xyvh6r2TPRuGlE/bdbjtIwvmLX0badIiCVwSjIb4IBLssRYZH9nQGKbQL4TbJ7xRohMH3Ib0v3ccaRwUPlq+VJtb0tbrGiH9YnDn4bSP4GEfuy4bCzUk5vTei05KNF2kShPegltyYI22x8SkC3gmbmyHu/3va0g4HUnEUHpYvNR7dtZLRZCLFYvX68Taywsc/WwsGVdPQOsu/Q6eENxwBcrTm8r1K56sOHM2jWkDHF5yRoSkTwaO/R09wJbZtdZBHli97kPka5mg0ElLnbKBla+QGv8TDUpuID2tCNpX+n5AJipbrbKjI+2ii0RparMF0= mike@ctf-server"
    # Получаем параметры e и m
    e, m = get_rsa_parameters(public_key_openssh)

    print("Параметр e:", e)
    print("Параметр m:", m)