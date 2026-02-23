from random import seed, randint
from PIL import Image

f = open('encoding.txt', 'r')
line = f.readline()
im = Image.open('image.png')

width, height = im.width, im.height

print(width, height)

answer_to_the_ultimate_question_of_life = 42

seed(answer_to_the_ultimate_question_of_life)

amount_of_pixels_needed = len(line) * 8 // 3
bin_value_of_string = ''

for letter in line:
    bin_value = bin(ord(letter))[2:]
    while len(bin_value) < 8:
        bin_value = '0' + bin_value
    bin_value_of_string += bin_value

seed(42)

pixels = [(randint(0, height - 1), randint(0, width - 1)) for x in range(amount_of_pixels_needed)]

for pixel in pixels:

    r, g, b, t = im.getpixel(pixel) # png поддерживает прозрачность, она нам не нужна

    sub = bin_value_of_string[:3]

    r = (r >> 1 << 1) + int(sub[0])
    g = (g >> 1 << 1) + int(sub[1])
    b = (b >> 1 << 1) + int(sub[2])
    im.putpixel(pixel, (r, g, b, t))
    bin_value_of_string = bin_value_of_string[3:]

im.save('task.png')
im.close()

