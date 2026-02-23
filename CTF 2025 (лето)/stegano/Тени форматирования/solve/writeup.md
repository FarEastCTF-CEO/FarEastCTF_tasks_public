# Решение

В документе используются два стиля абзаца: обычный и `No Spacing` (без интервала).

1) Для каждого непустого абзаца выписываем бит:
- `Normal` -> 0
- `No Spacing` -> 1

2) Группируем биты по 8 и переводим в байты (UTF-8). Пример скрипта:

```python
from docx import Document

doc = Document("Необычайное приключение.docx")

bits = []
for p in doc.paragraphs:
    if not p.text.strip():
        continue
    bits.append("1" if p.style.name == "No Spacing" else "0")

# отбросим хвост до кратности 8
bits = "".join(bits)
bits = bits[:len(bits)//8*8]

data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
print(data.decode("utf-8").rstrip("\x00"))
```

**Флаг:** `FECTF{f57_dfdx}`