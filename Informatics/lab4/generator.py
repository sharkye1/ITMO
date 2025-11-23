"""
Генератор случайных TOML-файлов с вложенными таблицами и комментариями.
Для тестирования парсеров TOML.
"""

import random

WORDS = [
    "arbuz", "banan", "itmo", "python", "laba", "hz",
    "kek", "lol", "word", "example", "data", "value",
    "privet", "poka", "test", "random", "structure",
    "informatics", "computer", "science", "code",
    "function", "variable", "loop", "condition", 
    "subway", "coffee", "tea", "book", "music",
    "baraban", "guitar", "piano", "drum",
    "sun", "moon", "star", "sky", "cloud",
    "river", "mountain", "forest", "tree", "flower",
    "makson", "artur", "sergey", "alex", 
    "odin", "dva", "tri", "chetyre", "pyat",
    "shest", "sem", "vosem", "devyat", "desyat",
    "korona", "stella", "ginnes", "blanche",
    "Jagermeister", "baileys", "martini", "tequila",
    "balantines", "chivas", "johnnie", "walker",
    "Jack", "daniels", "rum", "vodka",
    "Aprol", "Becherovka", "Campari", "Cointreau",
    "Fernet", "Gordon's", "Hendrick's", "Jinger",
    "Kahlua", "Malibu", "Sambuca", "Tia", "Maria",
    "Limoncello", "Midori", "Suze", "Tatratea",
    "Redigaffi", "Tinto", "Picon", "Suze", "Amer",
    "Dubonnet", "Byrrh", "Cynar", "Galliano", "Chartreuse",
    "Frangelico", "Galliano", "Strega", "Amaretto", "Disaronno",
    "Grappa", "Sambuca", "Lillet", "Pastis", "Absinthe",
    "Ouzo", "Raki", "Tsipouro", "Baijiu", "Soju"
]

COMMENT_COUNTER = 1

def rnd_word():
    return random.choice(WORDS)

def rnd_value():
    t = random.randint(0, 3)
    if t == 0:
        return f"\"{rnd_word()}\""
    if t == 1:
        return str(random.randint(0, 999))
    if t == 2:
        return "true" if random.randint(0,1) else "false"
    return f"\"{rnd_word()} {rnd_word()}\""

def gen_kv(indent_level):
    key = rnd_word()
    val = rnd_value()
    indent = "\t" * indent_level
    global COMMENT_COUNTER
    comment = f" # comment {COMMENT_COUNTER}"
    COMMENT_COUNTER += 1
    return f"{indent}{key} = {val}{comment}\n"

def gen_table(name, indent_level):
    indent = "\t" * indent_level
    global COMMENT_COUNTER
    s = f"{indent}[{name}] # comment {COMMENT_COUNTER}\n"
    COMMENT_COUNTER += 1
    return s

def gen_array_table(name, indent_level):
    indent = "\t" * indent_level
    global COMMENT_COUNTER
    s = f"{indent}[[{name}]] # comment {COMMENT_COUNTER}\n"
    COMMENT_COUNTER += 1
    return s

def generate_nested(name, depth, max_depth, indent_level):
    """Генерация вложенных таблиц с красивыми отступами."""
    s = ""

    # таблица верхнего уровня
    if random.randint(0, 1):
        s += gen_table(name, indent_level)
    else:
        s += gen_array_table(name, indent_level)

    # несколько ключей внутри текущей
    for _ in range(random.randint(1, 3)):
        s += gen_kv(indent_level)

    # вложенность
    if depth < max_depth:
        # создаём 1–3 вложенные структуры
        for _ in range(random.randint(1, 3)):
            child_name = f"{name}.{rnd_word()}"
            s += generate_nested(child_name, depth + 1, max_depth, indent_level)
    return s

def generate_toml(size):
    """
    size — от 1 до 10+
    Чем больше size, тем больше структур и глубже вложенность.
    """
    random.seed()

    max_depth = min(7, size)  # ограничиваем глубину
    structures = size * 3      # количество верхнеуровневых элементов

    result = "# generated TOML file\n\n"

    for _ in range(structures):
        name = rnd_word()
        result += generate_nested(name, 1, max_depth, 0)
        result += "\n"

    return result


def main():
    size = int(input("Введите размер TOML: "))
    # size = 2 ~ 60 строк
    # size = 3 ~ 200 строк
    # size = 4 ~ 600 строк
    # size = 5 ~ 1300 строк
    # size = 9 ~ 11000 строк
    # size = 25 ~ 30000 строк
    # size = 50 ~ 60000 строк
    data = generate_toml(size)

    with open(f"{script_dir}/generated.toml", "w", encoding="utf-8") as f:
        f.write(data)

    print("Файл generated.toml успешно создан!")

if __name__ == "__main__":
    script_dir = __file__.replace('\\','/').rsplit('/',1)[0]
    main()
