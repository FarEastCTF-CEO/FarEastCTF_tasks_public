# Решение

Внутри docx часть символов имеет цвет `#000001` вместо стандартного чёрного (визуально почти не отличается).

Вариант 1 (быстро): сохранить документ как XML (или распаковать docx как zip) и выбрать только те `w:r`, у которых стоит `<w:color w:val="000001"/>`.

Пример на Python:

```python
import zipfile
import xml.etree.ElementTree as ET

ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

with zipfile.ZipFile("Текст, сгенерированный нейросеткой.docx") as z:
    xml = z.read("word/document.xml")

root = ET.fromstring(xml)
out = []

for r in root.findall(".//w:r", ns):
    rpr = r.find("w:rPr", ns)
    if rpr is None:
        continue
    col = rpr.find("w:color", ns)
    if col is None:
        continue
    if col.attrib.get(f"{{{ns['w']}}}val") != "000001":
        continue
    for t in r.findall(".//w:t", ns):
        out.append(t.text or "")

print("".join(out))
```

**Флаг:** `FECTF{a_ty_horosh}`