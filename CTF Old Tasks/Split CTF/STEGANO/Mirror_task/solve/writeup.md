# Writeup: Mirror_task

## Идея
Задание — простая стеганография в изображении: флаг «нарисован» в **младшем бите (LSB)** одного из цветовых каналов.

## Решение
1. Открываем PNG и проверяем скрытые плоскости (planes) / младшие биты каналов.
2. При просмотре **LSB красного канала (R & 1)** появляется читаемая строка с флагом.

### Вариант через StegSolve
1. Открыть картинку в StegSolve.
2. Переключаться по плоскостям (`Red plane 0`, `Green plane 0`, ...).
3. На **`Red plane 0`** видна надпись:

**SplitCTF{3epKaJLa_1s_GooD}**

### Вариант через Python
```python
from PIL import Image
import numpy as np

img = Image.open('Mirror_task_50.png').convert('RGBA')
arr = np.array(img)

# LSB красного канала
lsb_r = (arr[:, :, 0] & 1) * 255
Image.fromarray(lsb_r.astype('uint8')).save('lsb_r.png')
print('Откройте lsb_r.png — там будет флаг')
```

## Флаг
`SplitCTF{3epKaJLa_1s_GooD}`
