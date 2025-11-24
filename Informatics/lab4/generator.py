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
    "Fernet", "Gordons", "Hendricks", "Jinger",
    "Kahlua", "Malibu", "Sambuca", "Tia", "Maria",
    "Limoncello", "Midori", "Suze", "Tatratea",
    "Redigaffi", "Tinto", "Picon", "Suze", "Amer",
    "Dubonnet", "Byrrh", "Cynar", "Galliano", "Chartreuse",
    "Frangelico", "Galliano", "Strega", "Amaretto", "Disaronno",
    "Grappa", "Boklan", "Lillet", "Pastis", "Absinthe",
    "Ouzo", "Raki", "Tsipouro", "Baijiu", "Soju"
]

COMMENT_COUNTER = 1
USED_NAMES = set()  # отслеживание использованных имён

def rnd_word():
    """
    Возвращает случайное слово из списка WORDS
    """
    return random.choice(WORDS)

def rnd_unique_name(used_keys, prefix=""):
    """
    Генерирует уникальное имя, комбинируя слова если нужно
    """
    for _ in range(100):  # пробуем найти уникальное
        if random.randint(0, 1):
            name = rnd_word()
        else:
            name = f"{rnd_word()}_{rnd_word()}"
        
        full_name = f"{prefix}.{name}" if prefix else name
        if full_name not in used_keys:
            used_keys.add(full_name)
            return name
    # если не нашли за 100 попыток, добавляем счётчик
    name = f"{rnd_word()}_{random.randint(1000, 9999)}"
    full_name = f"{prefix}.{name}" if prefix else name
    used_keys.add(full_name)
    return name

def rnd_value():
    """
    Возвращает случайное значение для TOML: строку, число или булево
    """
    t = random.randint(0, 3)
    if t == 0:
        return f"\"{rnd_word()}\""
    if t == 1:
        return str(random.randint(0, 999))
    if t == 2:
        return "true" if random.randint(0,1) else "false"
    return f"\"{rnd_word()} {rnd_word()}\""

def gen_kv(indent_level, used_keys_in_scope):
    """
    Генерирует строку ключ-значение с отступом и комментарием
    """
    key = rnd_unique_name(used_keys_in_scope)
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

def generate_nested(name, depth, max_depth, indent_level, used_keys_global):
    """
    Генерация вложенных таблиц с красивыми отступами и уникальными ключами
    """
    s = ""
    used_keys_in_scope = set()  # ключи внутри текущей таблицы

    # таблица верхнего уровня
    if random.randint(0, 1):
        s += gen_table(name, indent_level)
    else:
        s += gen_array_table(name, indent_level)

    # несколько ключей внутри текущей
    for _ in range(random.randint(1, 3)):
        s += gen_kv(indent_level + 1, used_keys_in_scope)

    # вложенность
    if depth < max_depth:
        # создаём 1–3 вложенные структуры
        for _ in range(random.randint(1, 3)):
            child_name_part = rnd_unique_name(used_keys_global, prefix=name)
            child_name = f"{name}.{child_name_part}"
            s += generate_nested(child_name, depth + 1, max_depth, indent_level + 1, used_keys_global)
    return s

def generate_toml(size):
    """
    size — от 1 до 10+
    Чем больше size, тем больше структур и глубже вложенность
    """
    random.seed()

    max_depth = min(7, size)  # ограничиваем глубину
    structures = size * 3      # количество верхнеуровневых элементов
    used_keys_global = set()   # глобальное отслеживание имён

    result = "# generated TOML file\n\n"

    for _ in range(structures):
        name = rnd_unique_name(used_keys_global)
        result += generate_nested(name, 1, max_depth, 0, used_keys_global)
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

    with open(f"{script_dir}/sources/generated.toml", "w", encoding="utf-8") as f:
        f.write(data)

    print("Файл generated.toml успешно создан!")

if __name__ == "__main__":
    script_dir = __file__.replace('\\','/').rsplit('/',1)[0]
    main()
