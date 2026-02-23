# Решение

Внутри `da_cat.png` в синем канале спрятан QR-код во втором битовом слое (blue plane 1).

1) Достаньте битплейн (bit 1) синего канала и получите чёрно-белую картинку.
2) Считайте QR любым сканером.

Пример на Python (OpenCV):

```python
from PIL import Image
import numpy as np
import cv2

img = Image.open("da_cat.png").convert("RGB")
arr = np.array(img)

blue = arr[:, :, 2]
plane = ((blue >> 1) & 1).astype(np.uint8) * 255

detector = cv2.QRCodeDetector()
data, _, _ = detector.detectAndDecode(plane)
print(data)
```

QR содержит строку `hes_old`, собираем флаг.

**Флаг:** `FECTF{hes_old}`