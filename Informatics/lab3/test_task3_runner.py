from Informatics_Lab3_Task3 import get_problems


QTY_MSG = "Сумма всех цифр в вашем пароле должна составлять 25."
MONTH_MSG = "В вашем пароле должен быть указан месяц года."
SPECIAL_MSG = "В вашем пароле должен быть специальный символ."
UPPER_MSG = "В вашем пароле должна быть заглавная буква."
LEN_MSG = "Длина вашего пароля должна составлять не менее 5 символов."


TEST_CASES = [
    # полностью валидный пароль
    ("Январь!" + "1" * 25, ""),
    # нет специального символа
    ("Январь" + "1" * 25, SPECIAL_MSG),
    # нет заглавной буквы
    ("январь!" + "1" * 25, UPPER_MSG),
    # неверная сумма цифр 
    ("Январь!" + "1" * 24, QTY_MSG),
    # нет месяца и нет спецсимвола
    ("A" + "1" * 25, "\n".join([MONTH_MSG, SPECIAL_MSG])),
    # нет цифр
    ("Январь!", "\n".join([QTY_MSG])),
    # короткий и много ошибок
    ("Ab", "\n".join([QTY_MSG, MONTH_MSG, SPECIAL_MSG, LEN_MSG])),
    # есть спец и заглавная, но нет цифр и нет месяца (и слишком короткий)
    ("Abc!", "\n".join([QTY_MSG, MONTH_MSG, LEN_MSG])),
    # месяц есть, нет цифр и нет заглавной
    ("январь!", "\n".join([QTY_MSG, UPPER_MSG])),
    # ещё один валидный пример (другое название месяца)
    ("Март#" + "2" * 25, QTY_MSG),
]


def run_tests():
    total = len(TEST_CASES)
    passed = 0
    print("Всего тестов:", total)
    print("-----   " * 18)

    for i, (password, waiting) in enumerate(TEST_CASES, 1):
        problems = get_problems(password)
        out = "\n".join(problems)
        # Подменяем в ожидаемой строке сообщение о сумме на строку с реальной суммой цифр
        digit_sum = sum(int(d) for d in __import__('re').findall(r"\d", password))
        waiting_output = waiting.replace(QTY_MSG, f"{QTY_MSG} (текущая сумма: {digit_sum})")

        if out == waiting_output:
            print('\n', f"✅Тест {i}: пройден✅")
            passed += 1
        else:
            print(f"❌Тест {i}: НЕ ПРОЙДЕН❌")

        print("  Пароль:", password)
        print("  Ожидалось:", repr(waiting_output))
        print("  Получено:", repr(out), '\n')
        print("-----   " * 18)

    print("Итого пройдено:", passed, "из", total)


if __name__ == '__main__':
    run_tests()
