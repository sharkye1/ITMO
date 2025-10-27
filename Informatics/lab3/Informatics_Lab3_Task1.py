# Author = Gevorkyan Aleksey Stanislavovich
# Group = P3118
# Date = 26.10.2025

# Необходимо найти в тексте каждый фрагмент, где сначала идёт слово «ВТ»,
# затем не более 4 слов, и после этого идёт слово «ИТМО».
import re


def find_VT_ITMO(text):
    pattern = r'\bВТ\b(?:\w+){0,4}?\W+\bИТМО\b'
    # \b ВТ \b - обозначает слово "ВТ" (границы слова)
    # (?:\W+\w+){0,4}? - не более 4 слов между "ВТ" и "ИТМО"
    # \w+ - одно или более словесных символов (буквы, цифры и тд)
    # \b ИТМО \b - обозначает слово "ИТМО" (границы слова)
    return re.findall(pattern, text)

if __name__ == "__main__":
    text = input()
    matches = find_VT_ITMO(text)
    
    for match in matches:
        print(match)
