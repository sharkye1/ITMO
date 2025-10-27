# Author = Gevorkyan Aleksey Stanislavovich
# Group = P3118
# Date = 26.10.2025


# С помощью регулярного выражения найти в тексте слова, в которых встречается
# строго одна гласная буква (встречаться она может несколько раз). Пример таких
# слов: окно, трава, молоко, etc.
# После чего данные слова требуется отсортировать сначала по увеличению длины
# слова, а затем лексикографически.
  

import re

def solve(text):
    text = text.lower()
    pattern = r'\b(?=\w*[еаоэяию])\w*([еаоэяию])(?:\w*\1\w*)*\b'
    words = re.findall(pattern, text)  
    matches = re.finditer(r'\b(?=\w*[еаоэяию])\w*([еаоэяию])(?:\w*\1\w*)*\b', text)
    words = [m.group(0) for m in matches]
    unique_words = sorted(set(words), key=lambda x: (len(x), x))
    return unique_words

if __name__ == "__main__":
    text = input("Введите текст: ")
    result = solve(text)
    for word in result:
        print(word)
