# Решение

DOCX - это ZIP-архив. Флаг закодирован в `word/styles.xml` в виде последовательности атрибутов `w:semiHidden="0/1"`.

1) Распакуйте документ:
```bash
unzip SemiHidden.docx -d semi
```

2) Соберите все биты из `semi/word/styles.xml` и переведите в байты:

```python
import re

xml = open("semi/word/styles.xml", "r", encoding="utf-8").read()
bits = "".join(re.findall(r'w:semiHidden="([01])"', xml))

data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
print(data.decode("utf-8"))
```

**Флаг:** `FECTF{72f5bccdf801}`