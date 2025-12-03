"""

1. Число состояний системы равно 977. 
    Сколько дитов составляет мера Хартли для этой системы? 
    Округлить до целого в большую сторону.

2. Дан список x = ['I', 'like', 'to', 'study', 'at', 'ITMO']. 
    Напишите срез, который даст следующий результат: ['at', 'to', 'I'].

3. Сколько бит содержится в 2 KiB? 
    В ответе написать только целую часть результата.

4. Пусть имеется n=5 чисел (1,2,3,4,5). 
    Найти 93-ю перестановку. 
    Ответ записать в виде 5 чисел подряд без знаков препинания, пробелов и т.п.

5. Из канала передачи данных получено число, 
    закодированное с помощью классического кода Хэмминга: 0100011 
    Сообщение может содержать максимум одну ошибку. 
    Запишите изначальное отправленное сообщение (только информационные биты).

6. В результате перевода числа 44(10) в факториальную систему счисления было получено число 538(Ф). 
    Корректно ли был произведён перевод? 
    Если вы считаете, что да, то напишите слово "Correct" с большой буквы в английской раскладке без кавычек.
    Иначе – напишите слово "Wrong" с большой буквы в английской раскладке без кавычек.

7. Вычислите значение выражения и результат представьте в десятичной системе счисления: 20(14) + 18(13)

10. Переведите число 1960, представленное в системе счисления 10, в систему счисления -10 (нега-десятичную).
"""
import math
from itertools import permutations

def num1():
    states = 977
    # Hartley (dit) measure uses base-10 logarithm
    hartley_measure = math.ceil(math.log10(states))
    return hartley_measure

def num2():
    x = ['I', 'like', 'to', 'study', 'at', 'ITMO']
    return x[4::-2]

def num3():
    kibibytes = 2
    bits = kibibytes * 1024 * 8
    return bits

def num4():
    n = 5
    numbers = list(range(1, n + 1))
    perm = list(permutations(numbers))
    perm_93 = perm[92]  # 0-based index
    return ''.join(map(str, perm_93))

def num5():
    received = '0100011'
    p1 = int(received[0])
    p2 = int(received[1])
    d1 = int(received[2])
    p3 = int(received[3])
    d2 = int(received[4])
    d3 = int(received[5])
    d4 = int(received[6])

    # include parity bits in syndrome calculation
    c1 = (p1 + d1 + d2 + d4) % 2
    c2 = (p2 + d1 + d3 + d4) % 2
    c3 = (p3 + d2 + d3 + d4) % 2

    error_pos = c1 * 1 + c2 * 2 + c3 * 4

    if error_pos != 0:
        error_index = error_pos - 1
        received = list(received)
        received[error_index] = '1' if received[error_index] == '0' else '0'
        received = ''.join(received)

    data_bits = received[2] + received[4] + received[5] + received[6]
    return data_bits

def num6():
    number_decimal = 44
    factorial_representation = '538'

    # parse digits from the factorial representation string
    digits = [int(ch) for ch in factorial_representation]

    # compute decimal value: leftmost digit has weight len(digits)! down to 1!
    decimal_value = 0
    for i, d in enumerate(digits):
        weight = math.factorial(len(digits) - i)
        decimal_value += d * weight

    # validate that each digit is within allowed range: digit <= position index (len..1)
    valid = all(d <= (len(digits) - i) for i, d in enumerate(digits))

    if decimal_value == number_decimal and valid:
        return "Correct"
    else:
        return "Wrong"
    
def num7():
    num1_base14 = 2 * (14 ** 1) + 0 * (14 ** 0)
    num2_base13 = 1 * (13 ** 1) + 8 * (13 ** 0)
    result = num1_base14 + num2_base13
    return result

def num10():
    num = 1960
    base = -10
    nums = []
    while num != 0:
        num, remainder = divmod(num, base)
        if remainder < 0:
            remainder += -base
            num += 1
        nums.append(str(remainder))

    return ''.join(reversed(nums))



if __name__ == "__main__":
    print(f'номер 1: {num1()}')
    print(f'номер 2: {num2()}')
    print(f'номер 3: {num3()}')
    print(f'номер 4: {num4()}')
    print(f'номер 5: {num5()}')
    print(f'номер 6: {num6()}')
    print(f'номер 7: {num7()}')
    print(f'номер 10: {num10()}')