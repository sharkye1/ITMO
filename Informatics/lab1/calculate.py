# script.py
def to_symmetric_base(num, base):
    # Функция для конвертации числа num в симметричную систему с основанием base.
    if base < 3:  # Минимальное основание для симметричной - 3.
        raise ValueError("Основание должно быть не меньше 3.")
    
    if num == 0:
        return "0"  # Если число 0, то и в любой системе 0.
    
    digits = []  # Список для хранения цифр.
    while num != 0:
        remainder = num % base  # Остаток от деления.
        num = num // base  # Целочисленное деление.
        
        # В симметричной, если остаток больше floor(base/2), корректируем.
        half_base = base // 2
        if remainder > half_base:
            remainder -= base
            num += 1
        
        digits.append(remainder)  # Добавляем цифру в список.
    
    # Переворачиваем список, потому что собирали с конца.
    digits.reverse()
    
    # Преобразуем в строку с обозначениями.
    result = ""
    for d in digits:
        if d < 0:
            result += "{^" + str(-d) + "}"  # Для отрицательных: {^k}
        else:
            result += str(d)
    
    return result

# Интерактивная часть только для запуска напрямую
if __name__ == "__main__":
    try:
        input_num = input("Введите число в десятичной системе: ")
        num = int(input_num)
        input_base = input("Введите основание n для симметричной системы (например, 9): ")
        base = int(input_base)
        result = to_symmetric_base(num, base)
        print("Число в симметричной системе с основанием", base, ":", result)
    except ValueError as ve:
        print("Ошибка: неверный ввод. Убедитесь, что ввели целые числа и основание >= 3.", ve)
    except ZeroDivisionError:
        print("Ошибка: основание не может быть 0.")
    except Exception as e:
        print("Неизвестная ошибка:", e)