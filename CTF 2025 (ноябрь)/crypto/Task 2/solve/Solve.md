# WriteUp
Для генерации псевдослучайных чисел в программе используется линейно конгруэртный генератор. Он не является криптостойким т.к. если известы три последовательных значения $$x_{k-1},x_k,x_{k+1}$$, то параметры генератора $$a,b$$ восстанавливаются как решение системы сравнений:<br>


$$x_k+1 = a \cdot x_k + b \pmod n$$ <br>
$$x_k = a \cdot x_{k-1} + b \pmod n$$ <br>


Отсюда получаем:<br>


$$a(x_k-x_{k-1}) = (x_{k+1} - x_k) \pmod n$$<br>
$$b = x_k - a \cdot x_{k-1} \pmod n$$<br>


Тогда, $$x_0$$ восстанавливается как решение сравнения:<br>


$$a \cdot x_0 + b = x_1 \pmod n$$<br>


При этом, для генерации каждой комнаты используется только одно значение полученное от линейно конгруэртного генератора. Комната генерируется с помощью следующих соотношений:
```python
    room_width = 7 + room_seed % 13
    room_length = 5 + room_seed % 11
    flame_walls_quantity = room_seed % ( room_width // 2)
    chest_quantity = room_seed % 3
    diamonds_quantity = room_seed % 8

    if room_seed % 2: 
        room_map [chest_quantity + 1][1] = 6
    else:
        room_map [chest_quantity + 1][1] = 7
```
### Room_1
Для того чтобы восстановить $$x_1$$ достаточно следующих данных:
- room_width = 19
- room_length = 10
- flame_walls_quantity = 1
- diamonds_quantity = 5 <br>


Тогда:<br>


$$x_1 = 12 \pmod {13}$$<br>
$$x_1 = 5 \pmod {11}$$<br>
$$x_1 = 1 \pmod 9$$<br>
$$x_1 = 5 \pmod 8$$<br>


Отсюда, получаем:<br>


$$M = 13 \cdot 11 \cdot 9 \cdot 8 = 10296$$<br>
$$M_1 = 792 \to 792\cdot b_1 = 12 \pmod {13} \to b_1 = 1$$<br>
$$M_2 = 936 \to 936\cdot b_2 = 5 \pmod {11} \to b_2 = 5$$<br>
$$M_3 = 1144 \to 1144\cdot b_3 = 1 \pmod 9 \to b_3 = 1$$<br>
$$M_4 = 1287 \to 1287\cdot b_4 = 5 \pmod 8 \to b_4 = 3$$<br>
$$x_1 = 792 \cdot 1 + 936 \cdot 5 + 1144 \cdot 1 + 1287 \cdot 3 = 10477 = 181 \pmod {10296}$$

### Room_2
- room_width = 18
- room_length = 5
- flame_walls_quantity = 7
- diamonds_quantity = 2


Отсюда:<br>

$$x_2 = 11 \pmod {13}$$<br>
$$x_2 = 0 \pmod {11}$$<br>
$$x_2 = 7 \pmod 9$$<br>
$$x_2 = 2 \pmod 8$$<br>


Решив систему сравнений получаем:<br>


$$x_2 = 792 \cdot 2 + 936 \cdot 0 + 1144 \cdot 7 + 1287 \cdot 6 = 7018 \pmod {10296}$$


### Room_3
- room_width = 11
- room_length = 14
- flame_walls_quantity = 0
- diamonds_quantity = 7
- chest_quantity = 1


Отсюда:<br>


$$x_3 = 4 \pmod {13}$$<br>
$$x_3 = 9 \pmod {11}$$<br>
$$x_3 = 0 \pmod 5$$<br>
$$x_3 = 7 \pmod 8$$<br>
$$x_3 = 1 \pmod 3$$<br>


Решив систему сравнений получаем:<br>


$$x_3 = 1320 \cdot 8 + 1560 \cdot 1 + 3432 \cdot 0 + 2145 \cdot 7  + 5720 \cdot 2 = 4255 \pmod {17160}$$

### Расчет $$x_0$$


$$x_1 = 181$$ <br>
$$x_2 = 7018$$ <br>
$$x_3 = 4255$$ <br>


Восстановление параметров генератора:<br>


$$a(7018-181) = (4255-7018) \pmod {8192}$$<br>
$$a(6837) = 5429 \pmod {8192}$$ <br>
$$6837^{-1} = 925 \cdot {8192} \to a = 129$$ <br><br>

$$b = 4255 - 129 \cdot 7018 = 53$$<br>


Тогда:<br>


$$129x + 53 = 181 \pmod {8129}$$<br>
$$129x = 128 \pmod {8129}$$<br>
$$129^{-1} = 8065 \pmod {8192} \to x = 128 \pmod {8192}$$

Таким образом мы получаем флаг: FECTF{128}