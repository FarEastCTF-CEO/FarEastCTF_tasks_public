# Райтап: USB HID Keyboard Forensics (Boris.pcap)

---

## 1) Дано

Есть файл дампа `Boris.pcap`.  
Проверяем тип:

```bash
file Boris.pcap
```

Обычно вывод будет похож на: `pcap … (USB with USBPcap header)`.  
Это означает, что трафик снят **USBPcap (Windows)**, а не обычный сетевой pcap.

Во многих таких задачах внутри находятся **HID-репорты клавиатуры**
(interrupt transfers, чаще всего endpoint `0x81`) — то есть то, **что печатали**.

---

## 2) Метод решения

Клавиатура USB HID отправляет репорт фиксированного размера **8 байт**:

- `byte0` — модификаторы (Shift/Ctrl/Alt…)
- `byte1` — зарезервировано (обычно `00`)
- `byte2..byte7` — до 6 одновременно нажатых клавиш (HID keycodes)

Так как в дампе идут события “нажал/отпустил”, нужно:

- пройтись по HID-репортам;
- **учитывать только новые** keycode’ы относительно предыдущего репорта;
- учитывать Shift:
  - левый Shift — бит `0x02`
  - правый Shift — бит `0x20`

В `USBPcap`-pcap перед HID-данными присутствует служебный заголовок.
В этом дампе полезная HID-нагрузка начинается после фиксированного заголовка длиной **27 байт**,
а сам HID-репорт занимает **8 байт**.

---

## 3) Извлечение нажатий (скрипт)

Ниже скрипт, который:

- читает pcap как бинарный файл;
- извлекает HID-репорты;
- мапит HID keycode → символ (US раскладка);
- собирает введённый текст и выводит его (включая флаг).

```python
import struct
from pathlib import Path

PCAP = "Boris.pcap"
USBPCAP_HDR_LEN = 27          # в этом дампе всегда 27
HID_REPORT_LEN = 8            # стандартный HID keyboard report

# HID keycode -> (без Shift, с Shift) для US раскладки
hid = {}

# a-z (0x04..0x1d)
for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz", start=0x04):
    hid[i] = (ch, ch.upper())

# 1-0 (0x1e..0x27)
nums = "1234567890"
shift_nums = "!@#$%^&*()"
for i, (ch, sh) in enumerate(zip(nums, shift_nums), start=0x1e):
    hid[i] = (ch, sh)

# пробел/таб/энтер
hid[0x2c] = (" ", " ")
hid[0x2b] = ("\t", "\t")
hid[0x28] = ("\n", "\n")

# знаки
hid.update({
    0x2d: ("-", "_"),
    0x2e: ("=", "+"),
    0x2f: ("[", "{"),
    0x30: ("]", "}"),
    0x31: ("\\", "|"),
    0x33: (";", ":"),
    0x34: ("'", '"'),
    0x35: ("`", "~"),
    0x36: (",", "<"),
    0x37: (".", ">"),
    0x38: ("/", "?"),
})

def parse_pcap(path: str):
    data = Path(path).read_bytes()
    # global header (24 bytes)
    if data[:4] != b"\xd4\xc3\xb2\xa1":
        raise ValueError("Ожидался little-endian PCAP (magic d4 c3 b2 a1)")
    off = 24
    while off + 16 <= len(data):
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack("<IIII", data[off:off+16])
        off += 16
        pkt = data[off:off+incl_len]
        off += incl_len
        yield pkt

def decode_keyboard(pkts):
    out = []
    prev_keys = set()

    for pkt in pkts:
        if len(pkt) < USBPCAP_HDR_LEN + HID_REPORT_LEN:
            continue

        rep = pkt[USBPCAP_HDR_LEN:USBPCAP_HDR_LEN + HID_REPORT_LEN]
        mod = rep[0]
        shift = bool(mod & 0x22)  # левый(0x02) или правый(0x20) Shift

        keys = {k for k in rep[2:] if k != 0}

        # печатаем только новые нажатия
        for k in sorted(keys - prev_keys):
            if k == 0x2a:         # backspace
                if out:
                    out.pop()
                continue
            if k in hid:
                out.append(hid[k][1] if shift else hid[k][0])
            else:
                out.append(f"<{k:02x}>")  # на случай неизвестного кода

        prev_keys = keys

    return "".join(out)

if __name__ == "__main__":
    text = decode_keyboard(parse_pcap(PCAP))
    print(text)
```

---

## 4) Запуск и результат

Запуск:

```bash
python3 solve.py
```

Вывод содержит введённую строку с флагом:

```
SplitCTF{6op15_5M@5H!!!}
```

---

## 5) Итог

- Тип задачи: **форензика USB (USBPcap)**
- Источник данных: **HID keyboard reports**
- Метод: извлечь 8-байтовые репорты, учесть Shift и “новые” keycode’ы
- Флаг: `SplitCTF{6op15_5M@5H!!!}`
