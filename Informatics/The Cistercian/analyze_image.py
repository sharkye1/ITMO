"""Скрипт для детального анализа изображения цистерцианского числа"""
from tools import *
import matplotlib
matplotlib.use('Agg')  # Для сохранения без показа
import matplotlib.pyplot as plt
import argparse
import os

# Парсим аргументы
parser = argparse.ArgumentParser(description='Анализ цистерцианского числа')
parser.add_argument('image', help='Путь к изображению', type=str, default='num1111.png', nargs='?')
parser.add_argument('--template-dir', type=str, default=None, help='Папка с шаблонами')
args = parser.parse_args()

# Создаём папку для вывода
os.makedirs('debug_output', exist_ok=True)

# Получаем имя файла для отображения
image_filename = os.path.basename(args.image)

# Загружаем шаблоны если указаны
templates = None
if args.template_dir:
	templates = load_templates(args.template_dir)
	print(f"Загружено шаблонов: {sum(len(v) for v in templates.values())}")

# Загрузим изображение
bw = load_and_binarize(args.image)
h, w = bw.shape
print(f"Размер изображения: {w}x{h}")

# Найдем оси
axis_x = find_vertical_axis(bw)
axis_y = h // 2  # Фиксированная середина для одинаковых квадрантов
print(f"Найденная вертикальная ось: x = {axis_x}")
print(f"Горизонтальная ось (середина): y = {axis_y}")

# Построим проекции
col_sums = bw.sum(axis=0)
row_sums = bw.sum(axis=1)

# Визуализируем
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Исходное изображение с осями
ax = axes[0, 0]
ax.imshow(1-bw, cmap='gray')
ax.axvline(x=axis_x, color='r', linewidth=2, label='Вертикальная ось')
ax.axhline(y=axis_y, color='b', linewidth=2, label='Горизонтальная ось')
ax.set_title('Исходное изображение с осями')
ax.legend()

# Вертикальная проекция
ax = axes[0, 1]
ax.plot(col_sums)
ax.axvline(x=axis_x, color='r', linewidth=2, label=f'x={axis_x}')
ax.set_title('Вертикальная проекция (сумма по столбцам)')
ax.set_xlabel('x')
ax.set_ylabel('Количество черных пикселей')
ax.legend()
ax.grid(True)

# Горизонтальная проекция
ax = axes[1, 0]
ax.plot(row_sums, range(len(row_sums)))
ax.axhline(y=axis_y, color='b', linewidth=2, label=f'y={axis_y}')
ax.set_title('Горизонтальная проекция (сумма по строкам)')
ax.set_ylabel('y')
ax.set_xlabel('Количество черных пикселей')
ax.legend()
ax.grid(True)
ax.invert_yaxis()

# Квадранты
ax = axes[1, 1]
ax.imshow(1-bw, cmap='gray')
ax.axvline(x=axis_x, color='r', linewidth=1, linestyle='--')
ax.axhline(y=axis_y, color='b', linewidth=1, linestyle='--')

# Отметим квадранты (нужная схема) - добавим информацию после распознавания
# Сначала просто отметим названия
ax.text(axis_x//2, axis_y//2, 'TL\n(десятки)', ha='center', va='center', 
        color='red', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax.text(axis_x + (w-axis_x)//2, axis_y//2, 'TR\n(единицы)', ha='center', va='center',
        color='red', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax.text(axis_x//2, axis_y + (h-axis_y)//2, 'BL\n(тысячи)', ha='center', va='center',
        color='red', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax.text(axis_x + (w-axis_x)//2, axis_y + (h-axis_y)//2, 'BR\n(сотни)', ha='center', va='center',
        color='red', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax.set_title('Разметка квадрантов')

plt.tight_layout()
plt.savefig('debug_output/analysis.png', dpi=150)
print("\nАнализ сохранен в debug_output/analysis.png")

# Детальный анализ каждого квадранта (нужный порядок)
print("\n=== Детальный анализ квадрантов ===")
quads = [('TR', 1, 'единицы'), ('TL', 10, 'десятки'), ('BR', 100, 'сотни'), ('BL', 1000, 'тысячи')]
total_number = 0
quadrant_results = {}

for name, mul, desc in quads:
	mask = quadrant_mask(bw, axis_x, axis_y, name)
	feat = analyze_quadrant(bw, mask, axis_x, axis_y)
	digit_heuristic = classify_quadrant(feat)
	
	ys, xs = np.where(mask)
	if len(ys) > 0:
		y0, y1 = ys.min(), ys.max()
		x0, x1 = xs.min(), xs.max()
		crop = bw[y0:y1+1, x0:x1+1] * mask[y0:y1+1, x0:x1+1]
		black_pixels = crop.sum()
		total_pixels = crop.size
	else:
		black_pixels = 0
		total_pixels = 1
		crop = np.zeros((10,10), dtype=np.uint8)
	
	# Определяем цифру через шаблоны если доступны
	digit_template = None
	best_score = 0.0
	best_template_digit = None
	top3_matches = []  # Топ-3 совпадения для вывода
	
	# Всегда сохраняем оригинальный кроп
	from PIL import Image as PILImage
	img_crop_orig = PILImage.fromarray((1 - crop) * 255).convert('L')
	img_crop_orig.save(f'debug_output/{name}_crop_original.png')
	
	# Всегда сохраняем нормализованный кроп
	norm_crop = normalize_crop(crop)
	img_crop_norm = PILImage.fromarray((1 - norm_crop) * 255).convert('L')
	img_crop_norm.save(f'debug_output/{name}_crop_normalized.png')
	
	if templates and name in templates:
		digit_template, best_score = template_classify(crop, templates.get(name, []), min_score=0.30)
		
		# Найдём все совпадения и отсортируем по score
		all_matches = []
		max_score = 0.0
		for digit, tmpl in templates.get(name, []):
			norm_tmpl = normalize_crop(tmpl)
			inter = np.logical_and(norm_crop, norm_tmpl).sum()
			union = np.logical_or(norm_crop, norm_tmpl).sum()
			score = inter / union if union > 0 else 0.0
			all_matches.append((digit, score, tmpl))
			if score > max_score:
				max_score = score
				best_template_digit = digit
				best_template = tmpl
		
		# Сортируем и берем топ-3
		all_matches.sort(key=lambda x: x[1], reverse=True)
		top3_matches = [(digit, score) for digit, score, _ in all_matches[:3]]
		
		# Сохраняем все шаблоны из топ-3
		for rank, (digit, score, tmpl) in enumerate(all_matches[:3], start=1):
			norm_tmpl = normalize_crop(tmpl)
			img_tmpl = PILImage.fromarray((1 - norm_tmpl) * 255).convert('L')
			img_tmpl.save(f'debug_output/{name}_top{rank}_template_{digit}_normalized_score{score:.2f}.png')
			
			img_tmpl_orig = PILImage.fromarray((1 - tmpl) * 255).convert('L')
			img_tmpl_orig.save(f'debug_output/{name}_top{rank}_template_{digit}_original_score{score:.2f}.png')
	
	digit_final = digit_template if digit_template is not None else digit_heuristic
	total_number += digit_final * mul
	quadrant_results[name] = {
		'digit': digit_final,
		'heuristic': digit_heuristic,
		'template': digit_template,
		'score': best_score,
		'best_match_digit': best_template_digit if best_template_digit is not None else None,
		'best_match_score': max_score if best_template_digit is not None else 0.0,
		'top3_matches': top3_matches,
		'desc': desc
	}
	
	print(f"\n{name} ({desc}):")
	print(f"  Эвристика: {digit_heuristic}")
	if templates:
		if digit_template is not None:
			print(f"  Шаблон: {digit_template} (score={best_score:.2f})")
		else:
			if best_template_digit is not None:
				print(f"  Шаблон: не найден (лучший match={best_template_digit}, score={max_score:.2f}, порог=0.30)")
			else:
				print(f"  Шаблон: не найден (лучший score={best_score:.2f})")
		if top3_matches:
			print(f"  Топ-3 совпадений: {', '.join([f'{d}({s:.2f})' for d, s in top3_matches])}")
	print(f"  Финальный результат: {digit_final}")
	print(f"  Границы: x=[{xs.min() if len(xs) else 0}:{xs.max() if len(xs) else 0}], y=[{ys.min() if len(ys) else 0}:{ys.max() if len(ys) else 0}]")
	print(f"  Черных пикселей: {black_pixels}/{total_pixels}")
	print(f"  Признаки:")
	print(f"    - density (плотность): {feat['density']:.4f}")
	print(f"    - components (компонент): {feat['components']}")
	print(f"    - v_near_axis (вертикаль у оси): {feat['v_near_axis']:.4f}")
	print(f"    - h_near_axis (горизонталь у оси): {feat['h_near_axis']:.4f}")
	print(f"    - diag (диагональ): {feat['diag']:.4f}")

print(f"\n{'='*50}")
print(f"ИТОГОВОЕ РАСПОЗНАННОЕ ЧИСЛО: {total_number}")
# Обновим график с результатами распознавания
fig2, axes2 = plt.subplots(2, 2, figsize=(14, 12))

# Исходное изображение с осями и результатами
ax = axes2[0, 0]
ax.imshow(1-bw, cmap='gray')
ax.axvline(x=axis_x, color='r', linewidth=2, label='Вертикальная ось')
ax.axhline(y=axis_y, color='b', linewidth=2, label='Горизонтальная ось')

# Добавим аннотации с результатами распознавания
for name, result in quadrant_results.items():
	if name == 'TL':
		x_pos, y_pos = axis_x//2, axis_y//2
	elif name == 'TR':
		x_pos, y_pos = axis_x + (w-axis_x)//2, axis_y//2
	elif name == 'BL':
		x_pos, y_pos = axis_x//2, axis_y + (h-axis_y)//2
	else:  # BR
		x_pos, y_pos = axis_x + (w-axis_x)//2, axis_y + (h-axis_y)//2
	
	method = "T" if result['template'] is not None else "H"
	score_text = f"({result['score']:.2f})" if result['template'] is not None else ""
	
	# Если score < 0.9 и есть топ-3, добавляем их
	top3_text = ""
	if result['score'] < 0.9 and result.get('top3_matches'):
		top3_text = "\nTop-3:\n" + "\n".join([f"{d}: {s:.2f}" for d, s in result['top3_matches']])
	
	text = f"{name}\n{result['desc']}\n═══\nЦифра: {result['digit']}\n[{method}]{score_text}{top3_text}"
	ax.text(x_pos, y_pos, text, ha='center', va='center',
	        color='darkgreen' if result['template'] is not None else 'darkred',
	        fontsize=8, fontweight='bold',
	        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax.set_title(f'Файл: {image_filename}\nРаспознанное число: {total_number}', fontsize=14, fontweight='bold', color='black')
ax.legend()
ax.set_title(f'Распознанное число: {total_number}', fontsize=14, fontweight='bold', color='black')
ax.legend()

# Таблица с результатами
ax = axes2[0, 1]
ax.axis('off')
table_data = [['Квадрант', 'Метод', 'Цифра', 'Score']]
for name in ['BL', 'BR', 'TL', 'TR']:
	result = quadrant_results[name]
	method = 'Template' if result['template'] is not None else 'Heuristic'
	score = f"{result['score']:.3f}" if result['template'] is not None else "N/A"
	table_data.append([f"{name} ({result['desc']})", method, str(result['digit']), score])

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.25, 0.15, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)

# Стилизуем заголовок таблицы
for i in range(4):
	cell = table[(0, i)]
	cell.set_facecolor('#4CAF50')
	cell.set_text_props(weight='bold', color='white')

ax.set_title('Результаты распознавания', fontsize=12, fontweight='bold')

# Вертикальная проекция
ax = axes2[1, 0]
ax.plot(col_sums)
ax.axvline(x=axis_x, color='r', linewidth=2, label=f'Ось: x={axis_x}')
ax.set_title('Вертикальная проекция')
ax.set_xlabel('x (пиксели)')
ax.set_ylabel('Количество черных пикселей')
ax.legend()
ax.grid(True, alpha=0.3)

# Горизонтальная проекция
ax = axes2[1, 1]
ax.plot(row_sums, range(len(row_sums)))
ax.axhline(y=axis_y, color='b', linewidth=2, label=f'Ось: y={axis_y}')
ax.set_title('Горизонтальная проекция')
ax.set_ylabel('y (пиксели)')
ax.set_xlabel('Количество черных пикселей')
ax.legend()
ax.grid(True, alpha=0.3)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('debug_output/analysis_detailed.png', dpi=150, bbox_inches='tight')
print("Детальный анализ сохранен в debug_output/analysis_detailed.png")

print(f"\n✓ Результаты сохранены в debug_output/")
