def int_to_chars(value, length):
    chars = []
    for _ in range(length):
        chars.append(chr(value & 0xff))
        value >>= 8
    return ''.join(chars)

def reverse_hashes():
    local6 = 0xcafedead

    # Вычисляем части путем обратных операций
    first_part = 0x1114f2dff - local6
    second_part = 0x10b421402 - local6
    third_part = 0xcb431201 - local6

    # Преобразуем части в символы
    first_chars = int_to_chars(first_part, 4)
    second_chars = int_to_chars(second_part, 4)
    third_chars = int_to_chars(third_part, 3)

    # Объединяем части
    matching_word = first_chars + second_chars + third_chars

    return matching_word

matching_word = reverse_hashes()
print(f"Слово, которое выводит 'RIGHT!': {matching_word}")
