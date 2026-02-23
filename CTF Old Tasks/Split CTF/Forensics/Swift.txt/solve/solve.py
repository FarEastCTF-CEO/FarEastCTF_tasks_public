#!/usr/bin/env python3
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent / 'public'
BOOK_DIR = PUBLIC / 'book'
COORDS_FILE = PUBLIC / 'Swift.txt'

WORD_RE = re.compile(r"[A-Za-z]+")


def load_words(chapter_num: int) -> list[str]:
    # chapters are stored as 01_*.md .. 24_*.md
    prefix = f"{chapter_num:02d}_"
    matches = sorted(BOOK_DIR.glob(prefix + "*.md"))
    if not matches:
        raise FileNotFoundError(f"Chapter {chapter_num} not found in {BOOK_DIR}")
    text = matches[0].read_text(encoding='utf-8', errors='ignore')
    return WORD_RE.findall(text)


def main() -> None:
    lines = COORDS_FILE.read_text(encoding='utf-8', errors='ignore').splitlines()

    coords: list[tuple[int, int]] = []
    for ln in lines:
        m = re.fullmatch(r"\s*(\d+)\s*,\s*(\d+)\s*", ln)
        if m:
            coords.append((int(m.group(1)), int(m.group(2))))

    if not coords:
        raise SystemExit('No coordinates found in Swift.txt')

    cache: dict[int, list[str]] = {}
    extracted_words: list[str] = []

    for ch, idx in coords:
        if ch not in cache:
            cache[ch] = load_words(ch)
        words = cache[ch]
        if idx < 1 or idx > len(words):
            raise SystemExit(f"Bad coordinate: {ch},{idx} (chapter has {len(words)} words)")
        extracted_words.append(words[idx - 1])

    letters = ''.join(w[0] for w in extracted_words)
    odd = letters[0::2]
    even = letters[1::2]

    print('All letters:', letters)
    print('Odd letters :', odd)
    print('Even letters:', even)

    # In this task the odd letters are the flag body
    flag = f"SplitCTF{{{odd}}}"
    print('Flag:', flag)


if __name__ == '__main__':
    main()
