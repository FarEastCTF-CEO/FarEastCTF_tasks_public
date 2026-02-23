# Решение

В архиве 5141 фрагмент (файлы `1.png` ... `5141.png`). Номера идут по строкам слева направо.

1. Раскладываем количество фрагментов на множители:
   - 5141 = 53 * 97
2. Пробуем собрать сетку 53 строки на 97 столбцов.
3. Склеиваем тайлы в этом порядке и получаем картинку с флагом.

Пример скрипта на Python:

```python
from PIL import Image
import os

def assemble_image(rows, cols, image_dir):
    first = Image.open(os.path.join(image_dir, "1.png"))
    w, h = first.size
    out = Image.new("RGB", (cols * w, rows * h))

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c + 1
            piece = Image.open(os.path.join(image_dir, f"{idx}.png"))
            out.paste(piece, (c * w, r * h))
    return out

img = assemble_image(53, 97, "chunks")
img.save("assembled.png")
```

## Флаг

`FECTF{I_d0nt_f3e1_s0_g0od}`
