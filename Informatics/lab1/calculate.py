# script.py
def to_symmetric_base(num, base):
    # Проверка, что входные данные - целые числа
    if not isinstance(num, int):
        raise ValueError("Число должно быть целым.")
    if not isinstance(base, int):
        raise ValueError("Основание должно быть целым.")
    
    # Проверка основания: должно быть >= 3 и нечётным
    if base < 3:
        raise ValueError("Основание должно быть не меньше 3.")
    if base % 2 == 0:
        raise ValueError("Основание должно быть нечётным для симметричной системы.")
    
    # Если число 0, возвращаем "0"
    if num == 0:
        return "0"
    
    digits = []  # Список для хранения цифр
    while num != 0:
        remainder = num % base  # Остаток от деления
        num = num // base  # Целочисленное деление
        
        # В симметричной системе корректируем остаток, если он больше floor(base/2)
        half_base = base // 2
        if remainder > half_base:
            remainder -= base
            num += 1
        
        digits.append(remainder)  # Добавляем цифру
    
    # Переворачиваем цифры
    digits.reverse()
    
    # Формируем строку результата
    result = ""
    for d in digits:
        if d < 0:
            result += "{^" + str(-d) + "}"  # Отрицательные цифры как {^k}
        else:
            result += str(d)
    
    return result

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