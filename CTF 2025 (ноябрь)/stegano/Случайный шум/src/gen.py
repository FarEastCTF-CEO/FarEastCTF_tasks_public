from PIL import Image
import random

img = Image.new("RGB", (400, 300), (255, 255, 255))

pixels = []

for _ in range(400 * 300 + 15090 // 2):
    pixels.append((
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255)
    ))
pixels = list(set(pixels))

while len(pixels) != (400 * 300 + 15090 // 2):
    pixels.append((
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255)
    ))
    pixels = list(set(pixels))

random_pixels = pixels[:400 * 300]
flag_pixels = pixels[400 * 300:]
flag_pixels = flag_pixels + flag_pixels
random.shuffle(flag_pixels)

k = 0
for i in range(400):
    for j in range(300):
        img.putpixel((i, j), random_pixels[k])
        k += 1

img.save("random.png")
img_flag = Image.open("flag.png").convert("RGB")
p = 0
w, h = img_flag.size
for y in range(h):
    for x in range(w):
        r, g, b = img_flag.getpixel((x, y))
        if r != 255 and g != 255 and b != 255:
            pxl = flag_pixels.pop()
            img.putpixel((x, y), pxl)
            p+=1
print(p)
img.save("task.png")