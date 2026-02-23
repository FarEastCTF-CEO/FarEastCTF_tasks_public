from random import seed, randint
from PIL import Image

im = Image.open('task.png')
width, height = im.width, im.height

seed(42) # устанавливаем seed в соответствии с заданием
amount_of_pixels = 500 # сколько пикселей мы считываем (здесь нужно ~200, после идет лишь мусор)

bin_value = ''

for i in range(amount_of_pixels):
    x = randint(0, width - 1)  # генерируем "случайное" число в диапазоне от 0 до width - 1
    y = randint(0, height - 1) # генерируем "случайное" число в диапазоне от 0 до height - 1
    for component in im.getpixel((x,y))[:-1]: # последняя компонента - компонента прозрачности, она нам не нужна
        # смотрим последний бит каждой из компонент
        bin_value += str(component & 1)  # добавляем все в большую строку, содержащую каждый бит (чтобы не потерять нули)
        
decoded_message = ''
for i in range(0, len(bin_value), 8):
    char = chr(int(bin_value[i:i+8], 2)) # декодируем каждые 8 бит 
    decoded_message += char              # и добавляем в строку декодированного сообщения

print(decoded_message)
    







