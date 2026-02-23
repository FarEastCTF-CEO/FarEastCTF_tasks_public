# Writeup: Readable Source

## Что дают

Файл `proga.exe`.

## Разбор

1. Запускаем бинарник (Windows/.NET):
   - программа печатает строку `Hello! Find the flag in me` и ждёт нажатия клавиши в бесконечном цикле.
   - флаг при обычном запуске не выводится.

2. Открываем `proga.exe` в любом .NET‑декомпиляторе (dnSpy / ILSpy / dotPeek).

3. В классе `Program` есть метод `GetFlag()`, который **не вызывается** из `Main()`.
   Внутри `GetFlag()` собирается массив из 8 символов по формуле и затем печатается:

   ```csharp
   char[] a = new char[8];
   for (int i = 0; i < 8; i++) {
       int x = (i*i + 55*i) % 123;
       while (x < 65) x += 26;
       a[i] = (char)x;
   }
   Console.WriteLine("SplitCTF{" + new string(a) + "}");
   ```

4. Посчитаем получающуюся строку.

## Решение

Можно просто вручную посчитать 8 значений, либо быстро воспроизвести формулу скриптом:

```python
s = []
for i in range(8):
    x = (i*i + 55*i) % 123
    while x < 65:
        x += 26
    s.append(chr(x))
print('SplitCTF{' + ''.join(s) + '}')
```

Вывод:

`SplitCTF{NRrMqPxA}`

## Флаг

`SplitCTF{NRrMqPxA}`
