import struct
from itertools import product

EXE_PATH = "supertask.exe"

# Адрес зашифрованного блока кода (loc_423CC0)
CODE_VA = 0x423CC0

# Step1: 4 байта, которые sub_423C60 кладёт в byte_59D5D0
STEP1_CIPHER = bytes([0x85, 0xF7, 0xFE, 0xD3])
STEP1_PLAIN  = b"stp1"


def parse_pe_sections(data: bytes):
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e_lfanew:e_lfanew+4] != b"PE\0\0":
        raise ValueError("Not a PE file")

    _, nsec, _, _, _, size_opt, _ = struct.unpack_from("<HHIIIHH", data, e_lfanew + 4)
    opt_off = e_lfanew + 4 + 20
    magic = struct.unpack_from("<H", data, opt_off)[0]

    if magic == 0x10B:  # PE32
        image_base = struct.unpack_from("<I", data, opt_off + 28)[0]
    elif magic == 0x20B:  # PE32+
        image_base = struct.unpack_from("<Q", data, opt_off + 24)[0]
    else:
        raise ValueError(f"Unknown PE magic: {hex(magic)}")

    sec_off = opt_off + size_opt
    sections = []
    for i in range(nsec):
        off = sec_off + i * 40
        name = data[off:off+8].split(b"\0", 1)[0].decode(errors="ignore")
        vsize, vaddr, raw_size, raw_ptr = struct.unpack_from("<IIII", data, off + 8)
        # берем "покрываемый" размер как max(vsize, raw_size)
        sections.append((name, vaddr, max(vsize, raw_size), raw_ptr))

    return image_base, sections


def va_to_off(va: int, image_base: int, sections):
    rva = va - image_base
    for name, vaddr, size, raw_ptr in sections:
        if vaddr <= rva < vaddr + size:
            if raw_ptr == 0:
                raise ValueError(f"Section {name} has no raw data")
            return raw_ptr + (rva - vaddr)
    raise ValueError("VA not mapped to file offset")


def normalize_key(key: bytes) -> bytes:
    # поведение sub_423FC0: если длина нечётная — дублируем последний байт
    if len(key) % 2 == 1:
        return key + key[-1:]
    return key


def decrypt_block(buf: bytes, key: bytes) -> bytes:
    key = normalize_key(key)
    out = bytearray(buf)
    j = 1  # как в sub_423ED0
    for i in range(len(out)):
        out[i] = ((out[i] ^ key[j - 1]) - key[j]) & 0xFF
        j += 2
        if j == len(key) + 1:
            j = 1
    return bytes(out)


def find_len_by_10_nops(block: bytes) -> int:
    # как sub_423C80: найти 10 подряд 0x90, вернуть (pos_after - 12)
    idx = block.find(b"\x90" * 10)
    if idx == -1:
        raise ValueError("10xNOP marker not found")
    return (idx + 10) - 12


def extract_secret_from_decrypted(dec: bytes, n=10):
    """
    Извлекаем байты, которые записываются инструкциями вида:
      C6 /0 r/m8, imm8
    и конкретно нас интересуют записи в [EAX + disp] с disp=0..9.
    """
    writes = {}
    i = 0
    while i < len(dec) - 3:
        if dec[i] == 0xC6:
            modrm = dec[i + 1]
            mod = (modrm >> 6) & 3
            reg = (modrm >> 3) & 7
            rm  = modrm & 7

            # mov r/m8, imm8  => reg должен быть 0
            # берём только адресацию через EAX (rm=0) и mod 00/01/10 (память)
            if reg == 0 and rm == 0 and mod in (0, 1, 2):
                j = i + 2
                disp = 0
                if mod == 1:
                    disp = struct.unpack_from("<b", dec, j)[0]
                    j += 1
                elif mod == 2:
                    disp = struct.unpack_from("<i", dec, j)[0]
                    j += 4

                if j < len(dec) and 0 <= disp < 0x100:
                    imm = dec[j]
                    writes[disp] = imm

                i = j + 1
                continue

        i += 1

    if all(k in writes for k in range(n)):
        return bytes(writes[k] for k in range(n))
    return None


def main():
    exe = open(EXE_PATH, "rb").read()
    image_base, sections = parse_pe_sections(exe)

    # достаём ciphertext кода из файла
    code_off = va_to_off(CODE_VA, image_base, sections)
    window = exe[code_off:code_off + 0x400]  # с запасом
    code_len = find_len_by_10_nops(window)
    code_cipher = exe[code_off:code_off + code_len]

    # кандидаты ключа по Step1 (ограничим A-Z, как обычно в таких задачах)
    AZ = range(ord("A"), ord("Z") + 1)
    pairs = []
    for c, p in zip(STEP1_CIPHER, STEP1_PLAIN):
        sols = []
        for k0 in AZ:
            k1 = ((c ^ k0) - p) & 0xFF
            if ord("A") <= k1 <= ord("Z"):
                sols.append((k0, k1))
        pairs.append(sols)

    # 1-й фильтр: пролог (быстро отсеивает мусор)
    expected_prologue = bytes.fromhex("55 89 E5 83 EC 08 89 45 FC 89 55 F8")

    key_found = None
    secret_found = None

    for (k0, k1), (k2, k3), (k4, k5), (k6, k7) in product(*pairs):
        key = bytes([k0, k1, k2, k3, k4, k5, k6, k7])

        if decrypt_block(code_cipher[:12], key) != expected_prologue:
            continue

        dec = decrypt_block(code_cipher, key)

        # 2-й фильтр: в корректно расшифрованном коде должны быть записи байтов [eax+0..9]
        secret = extract_secret_from_decrypted(dec, n=10)
        if secret is None:
            continue

        key_found = key
        secret_found = secret
        break

    if not key_found:
        raise RuntimeError("Key not found (maybe key charset is not A-Z?)")

    print("KEY =", key_found.decode())
    print("SECRET WORD =", secret_found.decode(errors="replace"))


if __name__ == "__main__":
    main()
