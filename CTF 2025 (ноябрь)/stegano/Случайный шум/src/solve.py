from PIL import Image
from collections import Counter

img = Image.open("task.png").convert("RGB")

pixels = []
w, h = img.size
for y in range(h):
    for x in range(w):
        pixels.append(img.getpixel((x, y)))

pixels_counter = Counter(pixels)

for y in range(h):
    for x in range(w):
        if pixels_counter[img.getpixel((x, y))] == 1:
            img.putpixel((x, y), (0, 0, 0))
        else:
            img.putpixel((x, y), (255, 255, 255))

img.save("solve.png")
