"""Тестовый раннер для задания 3 (проверка паролей).

Структура аналогична test_task1_runner.py и test_task2_runner.py: простой студенческий
стиль вывода, набор тестов в TEST_CASES и функция run_tests().
"""

import io
import contextlib

from Informatics_Lab3_Task3 import solve


# Сообщения, которые печатает функция (должны совпадать точно)
QTY_MSG = "Количество цифр в вашем пароле должно составлять 25."
MONTH_MSG = "В вашем пароле должен быть указан месяц года."
SPECIAL_MSG = "В вашем пароле должен быть специальный символ."
UPPER_MSG = "В вашем пароле должна быть заглавная буква."
DIGIT_MSG = "Ваш пароль должен содержать цифру."
LEN_MSG = "Длина вашего пароля должна составлять не менее 5 символов."


# Набор тестовых случаев: (пароль, ожидаемая_строка)
# ожидаемая_строка — это то, что функция печатает в stdout (строки через '\n'),
# или пустая строка, если ожидаем, что ошибок не будет.
TEST_CASES = [
    # полностью валидный пароль
    ("Январь!" + "1" * 25, ""),
    # нет специального символа
    ("Январь" + "1" * 25, SPECIAL_MSG),
    # нет заглавной буквы
    ("январь!" + "1" * 25, UPPER_MSG),
    # неверное количество цифр (24)
    ("Январь!" + "1" * 24, QTY_MSG),
    # нет месяца и нет спецсимвола
    ("A" + "1" * 25, "\n".join([MONTH_MSG, SPECIAL_MSG])),
    # совсем нет цифр
    ("Январь!", "\n".join([QTY_MSG, DIGIT_MSG])),
    # короткий и много ошибок
    ("Ab", "\n".join([QTY_MSG, MONTH_MSG, SPECIAL_MSG, DIGIT_MSG, LEN_MSG])),
    # есть спец и заглавная, но нет цифр и нет месяца (и слишком короткий)
    ("Abc!", "\n".join([QTY_MSG, MONTH_MSG, DIGIT_MSG, LEN_MSG])),
    # месяц есть, нет цифр и нет заглавной
    ("январь!", "\n".join([QTY_MSG, UPPER_MSG, DIGIT_MSG])),
    # ещё один валидный пример (другое название месяца)
    ("Март#" + "2" * 25, ""),
]


def run_tests():
    # Простой студентский стиль: печатаем номер теста, результат и детали
    total = len(TEST_CASES)
    passed = 0
    print("Всего тестов:", total)
    print("-")

    for i, (password, expected) in enumerate(TEST_CASES, 1):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            solve(password)
        out = buf.getvalue().strip()

        if out == expected:
            print(f"Тест {i}: пройден")
            passed += 1
        else:
            print(f"Тест {i}: НЕ ПРОЙДЕН")

        print("  Пароль:", password)
        print("  Ожидалось:", repr(expected))
        print("  Получено:", repr(out))
        print("-----")

    print("Итого пройдено:", passed, "из", total)


if __name__ == '__main__':
    run_tests()
