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
    # Приводим текст к нижнему регистру
    text = text.lower()
    # Набор русских гласных (включая ё)
    vowels = set('аеёиоуыэюя')
    # Находим слова, состоящие только из русских букв
    found_words = re.findall(r"\b[а-яё]+\b", text)

    selected = []
    for w in found_words:
        # множество разных гласных, которые встречаются в слове
        vowel_set = {ch for ch in w if ch in vowels}
        # если ровно одна буква-гласная (она может повторяться) — принимаем слово
        if len(vowel_set) == 1 and vowel_set:
            selected.append(w)

    # убираем дубли и сортируем: сначала по длине, потом лексикографически
    unique = sorted(set(selected), key=lambda x: (len(x), x))
    return unique

if __name__ == "__main__":
    text = input("Введите текст: ")
    result = solve(text)
    for word in result:
        print(word)
