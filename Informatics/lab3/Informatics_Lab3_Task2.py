# Author = Gevorkyan Aleksey Stanislavovich
# Group = P3118
# Date =10.11.2025


# С помощью регулярного выражения найти в тексте слова, в которых встречается
# строго одна гласная буква (встречаться она может несколько раз). Пример таких
# слов: окно, трава, молоко, etc.
# После чего данные слова требуется отсортировать сначала по увеличению длины
# слова, а затем лексикографически.
  

import re

def solve(text):
    text = text.lower()
    vowels = set('аеёиоуыэюяaeiouy')
    words = re.findall(r"[a-zа-яё]+", text)

    selected = []
    for w in words:
        vowel_set = set()
        
        for ch in w:
            if ch in vowels:
                vowel_set.add(ch)

        if len(vowel_set) == 1:
            selected.append(w)

        print(vowel_set)

    unique = sorted(set(selected), key=lambda x: (len(x), x))
    return unique

if __name__ == "__main__":
    text = input("Введите текст: ")
    result = solve(text)
    for word in result:
        print(word)
