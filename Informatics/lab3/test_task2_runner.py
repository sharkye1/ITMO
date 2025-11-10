from Informatics_Lab3_Task2 import solve


TEST_CASES = [
    ("Окно трава молоко дом", ['дом', 'окно', 'трава', 'молоко']),
    ("Мама мыла раму окно ёлка", ['мама', 'окно']),
    ("Test word abcd eee", ['eee', 'abcd', 'test', 'word']),
    ("Тест ворд абсд ууу", ['ууу', 'абсд', 'ворд', 'тест']),
    ("oko oco abc", ['abc', 'oco', 'oko']),
    ("eee ooo iii", ['eee', 'iii', 'ooo']),
    ("пальто автобус корова", []),
    ("circle cake cow row", ['cow', 'row']),
    ("молоко moloko oko", ['oko', 'moloko', 'молоко']),
    ("тесто окно трава", ['окно', 'трава']),
    ("bbb vvv ggg", []),
]


def run_tests():
    ln = len(TEST_CASES)
    passed = 0
    print("Всего тестов:", ln)
    print("-----   " * 15)

    for idx, (test_text, ожидаемый) in enumerate(TEST_CASES, 1):
        matches = solve(test_text)

        if matches == ожидаемый:
            print(f"✅Тест {idx}: пройден✅")
            passed += 1
        else:
            print(f"❌Тест {idx}: НЕ ПРОЙДЕН❌")

        print("  Текст:", test_text)
        print("  Ожидалось:", ожидаемый)
        print("  Получено:", matches)
        print("-----   " * 15)

    print("Итого пройдено:", passed, "из", ln)


if __name__ == '__main__':
    run_tests()
