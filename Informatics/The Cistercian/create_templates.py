"""
Скрипт для создания шаблонов из обучающих изображений.
Использует правильные метки для каждого числа.
"""
from tools import load_and_binarize, find_vertical_axis, quadrant_mask
from PIL import Image
import numpy as np
import os

# Получаем директорию скрипта для правильных путей
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Обучающие данные: filename -> правильное число
training_data = {
    'num0000.png': 0,
    'num1111.png': 1111,
    'num2222.png': 2222,
    'num3333.png': 3333,
    'num4444.png': 4444,
    'num5555.png': 5555,
    'num6666.png': 6666,
    'num7777.png': 7777,
    'num8888.png': 8888,
    'num9999.png': 9999,
    # Дополнительные примеры для разнообразия (из папки nums)
    'nums/num1234.png': 1234,
    'nums/num1492.png': 1492,
    'nums/num1993.png': 1993,
    'nums/num4723.png': 4723,
    'nums/num6859.png': 6859,
    'nums/num7085.png': 7085,
    'nums/num9433.png': 9433,
    'nums/num9216.png': 9216,
    'nums/num1913.png': 1913,
    'nums/num8085.png': 8085,
    'nums/num90.png': 90,
}

# Схема: BL=тысячи, BR=сотни, TL=десятки, TR=единицы
def extract_digits(number):
	"""Извлекает цифры по квадрантам из числа"""
	return {
		'TR': number % 10,           # единицы
		'TL': (number // 10) % 10,   # десятки
		'BR': (number // 100) % 10,  # сотни
		'BL': (number // 1000) % 10  # тысячи
	}# Создаём папку для шаблонов
templates_dir = os.path.join(SCRIPT_DIR, 'templates')
os.makedirs(templates_dir, exist_ok=True)

print("Создание шаблонов из обучающих данных...\n")

for filename, correct_number in training_data.items():
    print(f"Обработка {filename} (число: {correct_number})")
    
    # Загружаем и находим ось
    full_path = os.path.join(SCRIPT_DIR, filename)
    bw = load_and_binarize(full_path)
    h, w = bw.shape
    axis_x = find_vertical_axis(bw)
    axis_y = h // 2  # Середина по вертикали
    
    # Извлекаем правильные цифры
    correct_digits = extract_digits(correct_number)
    
    # Обрабатываем каждый квадрант
    for quad_name in ['BR', 'TR', 'TL', 'BL']:
        digit = correct_digits[quad_name]
        
        # Извлекаем квадрант
        mask = quadrant_mask(bw, axis_x, axis_y, quad_name)
        ys, xs = np.where(mask)
        
        if len(ys) > 0:  # Сохраняем все, включая нули
            y0, y1 = ys.min(), ys.max()
            x0, x1 = xs.min(), xs.max()
            crop = bw[y0:y1+1, x0:x1+1] * mask[y0:y1+1, x0:x1+1]
            
            # Сохраняем как шаблон
            template_name = os.path.join(templates_dir, f"{quad_name}_{digit}_{correct_number}.png")
            img = (1 - crop) * 255  # Инверсия для визуализации
            im = Image.fromarray(img.astype(np.uint8), mode='L')
            im.save(template_name)
            print(f"  Сохранён шаблон: {quad_name}_{digit} -> {template_name}")

print("\n✓ Шаблоны созданы в папке templates/")
print("\nТеперь можно использовать их для распознавания:")
print("  python main.py <image.png> --template-dir templates")
