"""
Простой распознаватель цистерцианских цифр на изображении.

Как пользоваться:
	python tools.py path/to/image.png

Программа:
- Загружает изображение с помощью Pillow
- Преобразует в ч/б (бинаризация)
- Находит основную вертикальную ось (колонка с максимальной проекцией)
- Делит изображение на 4 квадранта относительно этой оси и средней горизонтали
- Для каждого квадранта вычисляет простые геометрические признаки и по эвристике пытается
  сопоставить их с цифрой 0..9
- Складывает итоговое число как: тысячи*1000 + сотни*100 + десятки*10 + единицы

Ограничения:
- Классификатор прост и эвристичен — может потребоваться тонкая настройка под ваши изображения.
- Для более надёжной работы рекомендую добавить набор эталонов/шаблонов и сравнение по корреляции. 
"""

from PIL import Image
# pip install Pillow (~4.7 мб)

import numpy as np
# pip install numpy (~12.8 мб)
from collections import deque


def load_and_binarize(path, thresh=128):
	im = Image.open(path).convert('L')
	a = np.array(im)
	bw = (a < thresh).astype(np.uint8)  # 1 — черное (штрих), 0 — фон
	return bw


def find_vertical_axis(bw):
	"""Находит X вертикальной оси как центр вертикальной основной черты.

	Предыдущее поведение брало просто столбец с максимумом проекции (argmax),
	что давало смещение к левому краю толстой вертикальной линии. Здесь мы:
	1. Строим сумму по столбцам.
	2. Находим пик максимума (peak).
	3. Расширяемся влево и вправо, пока столбцы находятся выше порога
	   (доля от максимума), чтобы определить фактическую ширину вертикальной
	   опорной линии.
	4. Возвращаем центр этого интервала.

	Если чёрных пикселей нет — возвращаем середину изображения.
	"""
	col_sums = bw.sum(axis=0)
	max_val = col_sums.max()
	if max_val == 0:
		return bw.shape[1] // 2
	peak = int(np.argmax(col_sums))
	# Порог: столбец считается частью вертикальной оси, если его сумма
	# >= frac * max_val. frac подобран эмпирически.
	frac = 0.6
	left = peak
	while left > 0 and col_sums[left-1] >= max_val * frac:
		left -= 1
	right = peak
	W = bw.shape[1]
	while right < W-1 and col_sums[right+1] >= max_val * frac:
		right += 1
	axis_x = (left + right) // 2
	return axis_x


def find_horizontal_axis(bw):
	# Аналогично по строкам
	row_sums = bw.sum(axis=1)
	if row_sums.max() == 0:
		return bw.shape[0] // 2
	axis_y = int(np.argmax(row_sums))
	return axis_y


def quadrant_mask(bw, axis_x, axis_y, quadrant):
	h, w = bw.shape
	mask = np.zeros_like(bw)
	if quadrant == 'TR':
		mask[0:axis_y, axis_x+1:w] = 1
	elif quadrant == 'BR':
		mask[axis_y+1:h, axis_x+1:w] = 1
	elif quadrant == 'TL':
		mask[0:axis_y, 0:axis_x] = 1
	elif quadrant == 'BL':
		mask[axis_y+1:h, 0:axis_x] = 1
	return mask.astype(bool)


def connected_components_count(bin_img):
	# простой BFS для подсчёта связных компонент в бинарном изображении (1 — объект)
	h, w = bin_img.shape
	seen = np.zeros_like(bin_img, dtype=bool)
	dirs = [(1,0),(-1,0),(0,1),(0,-1)]
	comps = 0
	for y in range(h):
		for x in range(w):
			if bin_img[y,x] and not seen[y,x]:
				comps += 1
				# BFS
				dq = deque()
				dq.append((y,x))
				seen[y,x] = True
				while dq:
					cy,cx = dq.popleft()
					for dy,dx in dirs:
						ny,nx = cy+dy, cx+dx
						if 0 <= ny < h and 0 <= nx < w and bin_img[ny,nx] and not seen[ny,nx]:
							seen[ny,nx] = True
							dq.append((ny,nx))
	return comps


def analyze_quadrant(bw, mask, axis_x, axis_y):
	# выделяем подизображение квадранта и вычисляем признаки
	h, w = bw.shape
	# bounding box
	ys, xs = np.where(mask)
	if len(ys) == 0:
		return {'density':0.0, 'components':0, 'v_near_axis':0.0, 'h_near_axis':0.0, 'diag':0.0, 
		        'corner':0.0, 'edge_v':0.0, 'edge_h':0.0, 'center':0.0}
	y0, y1 = ys.min(), ys.max()
	x0, x1 = xs.min(), xs.max()
	crop = bw[y0:y1+1, x0:x1+1] * mask[y0:y1+1, x0:x1+1]
	area = crop.size
	density = crop.sum() / area
	comps = connected_components_count(crop)

	H, W = crop.shape
	
	# Определим локальные координаты оси в crop
	axis_in_crop_x = axis_x - x0
	axis_in_crop_y = axis_y - y0
	
	# Проекции: вертикальная полоса рядом с вертикальной осью
	v_near_axis = 0.0
	if 0 <= axis_in_crop_x < W:
		# Берем узкую полосу (±2-3 пикселя) вокруг оси
		strip = crop[:, max(0, axis_in_crop_x-2):min(W, axis_in_crop_x+3)]
		if strip.size > 0:
			v_near_axis = strip.sum() / strip.size
	else:
		# Ось за пределами crop - берем край
		if axis_in_crop_x < 0:
			strip = crop[:, :min(5, W)]
		else:
			strip = crop[:, max(0, W-5):]
		if strip.size > 0:
			v_near_axis = strip.sum() / strip.size

	# Горизонтальная проекция рядом с горизонтальной осью
	h_near_axis = 0.0
	if 0 <= axis_in_crop_y < H:
		strip = crop[max(0, axis_in_crop_y-2):min(H, axis_in_crop_y+3), :]
		if strip.size > 0:
			h_near_axis = strip.sum() / strip.size
	else:
		if axis_in_crop_y < 0:
			strip = crop[:min(5, H), :]
		else:
			strip = crop[max(0, H-5):, :]
		if strip.size > 0:
			h_near_axis = strip.sum() / strip.size

	# Диагональная активность: от оси к дальнему углу
	diag = 0.0
	# Определяем дальний угол относительно оси
	corner_y = H-1 if axis_in_crop_y < H/2 else 0
	corner_x = W-1 if axis_in_crop_x < W/2 else 0
	
	start_y = max(0, min(H-1, axis_in_crop_y))
	start_x = max(0, min(W-1, axis_in_crop_x))
	
	samples = 0
	hits = 0
	for t in range(1, 21):
		fy = int(round(start_y + (corner_y - start_y) * (t/20)))
		fx = int(round(start_x + (corner_x - start_x) * (t/20)))
		if 0 <= fy < H and 0 <= fx < W:
			samples += 1
			if crop[fy,fx]:
				hits += 1
	if samples > 0:
		diag = hits / samples

	# Новые признаки: плотность в разных зонах квадранта
	
	# Угол (дальний от оси) - последняя четверть квадранта
	corner_region = crop[corner_y - H//4 if corner_y == H-1 else 0:corner_y + 1 if corner_y == H-1 else H//4,
	                     corner_x - W//4 if corner_x == W-1 else 0:corner_x + 1 if corner_x == W-1 else W//4]
	corner = corner_region.sum() / corner_region.size if corner_region.size > 0 else 0.0
	
	# Вертикальный край (дальний от оси)
	edge_x = W-1 if axis_in_crop_x < W/2 else 0
	edge_v_region = crop[:, max(0, edge_x-3):min(W, edge_x+4)]
	edge_v = edge_v_region.sum() / edge_v_region.size if edge_v_region.size > 0 else 0.0
	
	# Горизонтальный край (дальний от оси)
	edge_y = H-1 if axis_in_crop_y < H/2 else 0
	edge_h_region = crop[max(0, edge_y-3):min(H, edge_y+4), :]
	edge_h = edge_h_region.sum() / edge_h_region.size if edge_h_region.size > 0 else 0.0
	
	# Центр квадранта
	cy_start, cy_end = H//4, 3*H//4
	cx_start, cx_end = W//4, 3*W//4
	center_region = crop[cy_start:cy_end, cx_start:cx_end]
	center = center_region.sum() / center_region.size if center_region.size > 0 else 0.0

	return {
		'density': density, 
		'components': comps, 
		'v_near_axis': v_near_axis, 
		'h_near_axis': h_near_axis, 
		'diag': diag,
		'corner': corner,
		'edge_v': edge_v,
		'edge_h': edge_h,
		'center': center
	}


def classify_quadrant(feat):
	"""
	Классификатор цистерцианских цифр 0-9.
	
	В цистерцианской системе для каждого квадранта:
	1 = короткая горизонтальная черта от оси
	2 = короткая вертикальная черта от оси вверх/вниз (к краю квадранта)
	3 = диагональ от оси к дальнему углу
	4 = горизонталь + вертикаль у края (угол)
	5 = горизонталь от оси + диагональ
	6 = вертикаль от оси + диагональ  
	7 = вертикаль у края + диагональ
	8 = горизонталь + вертикаль у края + диагональ
	9 = сложная фигура (обычно перевернутая форма из предыдущих)
	"""
	d = feat['density']
	v = feat['v_near_axis']
	h = feat['h_near_axis']
	diag = feat['diag']
	corner = feat.get('corner', 0.0)
	edge_v = feat.get('edge_v', 0.0)
	edge_h = feat.get('edge_h', 0.0)
	center = feat.get('center', 0.0)

	# Порог для определения "пустоты"
	if d < 0.015:
		return 0
	
	# Специальное правило для квадрантов с только осью (без цифры)
	# Если density умеренная, components = 1 (только ось), и очень малая активность 
	# на горизонтальной оси (что указывает на отсутствие горизонтальных штрихов)
	if feat.get('components', 0) == 1 and h < 0.10 and d < 0.06:
		# Это скорее всего только вертикальная ось без цифры
		return 0

	# Определим, какие элементы присутствуют
	has_h_axis = h > 0.15  # горизонталь у оси
	has_v_axis = v > 0.20  # вертикаль у оси
	has_diag = diag > 0.15  # диагональ
	has_edge_v = edge_v > 0.15  # вертикаль у дальнего края
	has_edge_h = edge_h > 0.15  # горизонталь у дальнего края
	has_corner = corner > 0.15  # заполнение угла
	has_center = center > 0.10  # заполнение центра квадранта
	
	# Дополнительные "мягкие" признаки для более точного распознавания
	has_h_weak = h > 0.10
	has_v_weak = v > 0.15

	# Цифра 1: только горизонталь от оси (короткая черта вправо/влево)
	# Цифра 1 должна иметь заметную горизонталь, но вертикаль может быть от центральной оси
	if has_h_axis and not has_diag:
		# Если горизонталь доминирует или вертикаль примерно равна (из-за оси)
		# НО: если density и center высокие И вертикаль высокая, это может быть 9, а не 1
		# Ужесточим условие для 9: нужна и высокая плотность И высокая вертикаль И высокий center
		if d > 0.058 and v > 0.35 and center > 0.08:
			# Высокая плотность + умеренная вертикаль + заполненный центр = скорее 9
			return 9
		if h >= v * 0.9 or (h > 0.15 and not has_v_axis):
			return 1
	
	# Цифра 9: очень высокая вертикальная активность + значительная плотность
	# Цифра 9 часто имеет сильную вертикаль от оси и заполненную область
	if v > 0.65 and d > 0.055:
		return 9
	# Более мягкое правило для 9: высокая вертикаль + умеренная плотность
	if v > 0.7 and d > 0.045:
		return 9
	# Ещё одно правило для 9: если вертикаль умеренно высока и центр заполнен
	# НО не применяем, если есть диагональ или edge активность (может быть 8)
	if v > 0.35 and d > 0.055 and has_center and not has_diag and edge_v < 0.1 and edge_h < 0.1:
		return 9
	
	# Цифра 2: только вертикаль от оси (короткая черта вверх/вниз)
	# Вертикаль должна быть заметно сильнее горизонтали для цифры 2 и при этом не слишком высокая плотность
	if has_v_axis and not has_diag:
		if v > h * 1.4 and d < 0.05:
			return 2
	
	# Цифра 3: диагональ от оси к углу
	if has_diag and not has_h_axis and not has_v_axis:
		return 3
	
	# Цифра 4: угол (вертикаль у края + горизонталь у края или угла)
	# Цифра 4 имеет вертикальную и горизонтальную составляющие одновременно
	if not has_diag and not has_edge_v and not has_edge_h:
		# Цифра 4: обе оси присутствуют примерно одинаково
		if has_v_weak and has_h_weak:
			# Убедимся, что оба направления примерно равны (характерно для угла)
			if v > 0.14 and h > 0.10:
				# Дополнительно: разница между v и h не должна быть слишком большой
				# И вертикаль не должна быть слишком сильной (тогда это 2)
				# И горизонталь не должна быть слишком сильной (тогда это 1)
				ratio = max(v, h) / min(v, h)
				if ratio < 1.4 and v < 0.25:
					return 4
	
	# Цифра 5: горизонталь от оси + диагональ
	if has_h_axis and has_diag and not has_v_axis:
		return 5
	
	# Цифра 6: вертикаль от оси + диагональ
	if has_v_axis and has_diag and not has_h_axis:
		return 6
	
	# Цифра 7: вертикаль у края + диагональ (или все три элемента)
	if has_diag and has_edge_v:
		return 7
	
	# Цифра 8: сложная комбинация (угол + диагональ)
	if has_diag and ((has_edge_v and has_edge_h) or (has_h_axis and has_v_axis)):
		return 8
	
	# Цифра 9: очень высокая плотность или специфический паттерн
	# Часто имеет заполнение в центре и высокую общую плотность
	if (d > 0.055 and v > 0.30) or (d > 0.045 and has_center and v > 0.35):
		return 9
	
	# Fallback логика на основе доминирующего направления
	max_feat = max(v, h, diag)
	
	if max_feat == h and h > 0.12:
		return 1
	elif max_feat == v and v > 0.15:
		return 2
	elif max_feat == diag and diag > 0.10:
		return 3
	
	# Если ничего не подошло, но есть плотность
	if d > 0.03:
		# По умолчанию возвращаем на основе самого сильного признака
		if v > max(h, diag):
			return 2
		elif h > max(v, diag):
			return 1
		else:
			return 3
	
	return 0


def recognize(path, debug=False, dump_dir=None, templates=None, template_threshold=0.30):
	bw = load_and_binarize(path)
	h, w = bw.shape
	axis_x = find_vertical_axis(bw)
	# Горизонтальную ось берём как середину изображения для стабильных одинаковых квадрантов
	axis_y = h // 2

	# Схема цистерцианских квадрантов:
	# BL=Тысячи, BR=Сотни, TL=Десятки, TR=Единицы
	quads = [('TR', 1), ('TL', 10), ('BR', 100), ('BL', 1000)]
	total = 0
	details = {}
	for name, mul in quads:
		mask = quadrant_mask(bw, axis_x, axis_y, name)
		feat = analyze_quadrant(bw, mask, axis_x, axis_y)
		ys, xs = np.where(mask)
		if len(ys):
			y0, y1 = ys.min(), ys.max()
			x0, x1 = xs.min(), xs.max()
			crop = bw[y0:y1+1, x0:x1+1]
		else:
			crop = np.zeros((10,10), dtype=np.uint8)

		# Если есть шаблоны — пытаемся классифицировать только ими.
		if templates:
			# Очень пустой квадрант (только центральная ось, без штрихов) -> принудительно 0
			if feat['density'] < 0.006:
				digit = 0
			else:
				# Снач��ла пробуем шаблоны текущего квадранта
				best_digit, score = template_classify(crop, templates.get(name, []), min_score=template_threshold)
				
				if debug and templates.get(name):
					print(f"Template match {name}: best_digit={best_digit}, score={score:.2f}")
				
				# Если не нашли совпадение, пробуем шаблоны из других квадрантов (cross-quadrant matching)
				if best_digit is None:
					for other_quad in ['TR', 'TL', 'BR', 'BL']:
						if other_quad != name and other_quad in templates:
							temp_digit, temp_score = template_classify(crop, templates.get(other_quad, []), min_score=template_threshold * 0.7)
							if temp_digit is not None and temp_score > score:
								best_digit, score = temp_digit, temp_score
								if debug:
									print(f"Cross-quadrant match {name} from {other_quad}: {best_digit} (score={score:.2f})")
				
				if best_digit is not None:
					if debug:
						print(f"Template classify {name}: {best_digit} (score={score:.2f})")
					digit = best_digit
				else:
					# fallback на эвристику если шаблонов нет подходящих
					# Дополнительная проверка на ноль: низкая плотность + нет активных признаков
					if feat['density'] < 0.015 and feat['diag'] < 0.1 and feat['corner'] < 0.1:
						digit = 0
					else:
						digit = classify_quadrant(feat)
		else:
			# без шаблонов только эвристика
			digit = classify_quadrant(feat)

		details[name] = {'digit': digit, 'feat': feat}
		total += digit * mul

		# debug/dump
		if debug or dump_dir:
			# небольшая визуализация: кроп + контур маски
			ys, xs = np.where(mask)
			if len(ys):
				y0, y1 = ys.min(), ys.max()
				x0, x1 = xs.min(), xs.max()
				crop = bw[y0:y1+1, x0:x1+1]
			else:
				crop = np.zeros((10,10), dtype=np.uint8)

			if dump_dir:
				from PIL import Image as PILImage
				img = (1 - crop) * 255  # инверсия для визуализации: 0->255 фон, 1->0 штрих
				im = PILImage.fromarray(img.astype(np.uint8), mode='L')
				fname = f"quad_{name}.png"
				im.save(f"{dump_dir}/{fname}")

			if debug:
				print(f"Debug {name}: digit={digit}, feat={feat}")

	return total, axis_x, axis_y, details


def load_templates(template_dir, thresh=128):
	"""Load templates from `template_dir`. Expected filenames: QUAD_DIGIT.png or QUAD_DIGIT_*.png, e.g. TR_1.png or TR_1_1492.png"""
	import os
	templates = {}
	if not template_dir:
		return templates
	if not os.path.exists(template_dir):
		return templates
	for fn in os.listdir(template_dir):
		path = os.path.join(template_dir, fn)
		if not os.path.isfile(path):
			continue
		name = os.path.splitext(fn)[0]
		# ожидаемый формат: TR_1 или BL_9 или TR_1_1492
		parts = name.split('_')
		if len(parts) < 2:
			continue
		quad = parts[0]
		digit_s = parts[1]
		if quad not in ('TR','BR','TL','BL'):
			continue
		try:
			digit = int(digit_s)
		except Exception:
			continue
		try:
			im = Image.open(path).convert('L')
			a = np.array(im)
			mask = (a < thresh).astype(np.uint8)
		except Exception:
			continue
		templates.setdefault(quad, []).append((digit, mask))
	return templates


def match_template_to_crop(crop, templates_for_quad):
	"""
	Возвращает цифру с наилучшим совпадением и IoU, или (None,0), если шаблонов нет
	"""
	if not templates_for_quad:
		return None, 0.0
	from PIL import Image as PILImage
	H, W = crop.shape
	best_digit = None
	best_score = 0.0
	for digit, tmpl in templates_for_quad:
		# изменение размера шаблона под размер кропа
		try:
			im = PILImage.fromarray((1 - tmpl) * 255).convert('L')
			im2 = im.resize((W, H), resample=PILImage.NEAREST)
			t = (np.array(im2) < 128).astype(np.uint8)
		except Exception:
			continue
		inter = np.logical_and(crop, t).sum()
		union = np.logical_or(crop, t).sum()
		if union == 0:
			score = 0.0
		else:
			score = inter / union
		if score > best_score:
			best_score = float(score)
			best_digit = digit
	return best_digit, best_score


def normalize_crop(crop, target_size=32):
	"""
	Нормализует кроп к фиксированному размеру.
	Сначала обрезает пустое пространство вокруг цифры,
	затем масштабирует с сохранением пропорций и центрирует.
	"""
	from PIL import Image as PILImage
	H, W = crop.shape
	if H == 0 or W == 0:
		return np.zeros((target_size, target_size), dtype=np.uint8)
	
	# Находим bounding box реального содержимого
	rows = np.any(crop > 0, axis=1)
	cols = np.any(crop > 0, axis=0)
	
	if not np.any(rows) or not np.any(cols):
		# Пустой кроп - возвращаем пустой массив
		return np.zeros((target_size, target_size), dtype=np.uint8)
	
	rmin, rmax = np.where(rows)[0][[0, -1]]
	cmin, cmax = np.where(cols)[0][[0, -1]]
	
	# Добавляем небольшой padding (5% от размера)
	pad_h = max(1, int((rmax - rmin) * 0.05))
	pad_w = max(1, int((cmax - cmin) * 0.05))
	
	rmin = max(0, rmin - pad_h)
	rmax = min(H - 1, rmax + pad_h)
	cmin = max(0, cmin - pad_w)
	cmax = min(W - 1, cmax + pad_w)
	
	# Обрезаем до bounding box
	cropped = crop[rmin:rmax+1, cmin:cmax+1]
	crop_h, crop_w = cropped.shape
	
	# Вычисляем масштаб для вписывания в target_size с сохранением пропорций
	scale = min(target_size / crop_h, target_size / crop_w)
	new_h = int(crop_h * scale)
	new_w = int(crop_w * scale)
	
	# Масштабируем
	img = PILImage.fromarray((1 - cropped) * 255).convert('L')
	img_resized = img.resize((new_w, new_h), resample=PILImage.LANCZOS)
	
	# Создаем canvas и центрируем изображение
	canvas = np.zeros((target_size, target_size), dtype=np.uint8)
	y_offset = (target_size - new_h) // 2
	x_offset = (target_size - new_w) // 2
	
	resized_array = (np.array(img_resized) < 128).astype(np.uint8)
	canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_array
	
	# Морфологическое утончение для нормализации толщины линий
	# Более мягкий подход чем полная скелетизация
	from scipy.ndimage import binary_erosion
	
	# Применяем 1-2 итерации erosion для нормализации толщины
	# Это убирает избыточную толщину, но сохраняет структуру лучше чем skeletonize
	normalized = canvas.copy()
	for _ in range(1):  # 1 итерация erosion
		eroded = binary_erosion(normalized)
		# Останавливаемся если эрозия удалила слишком много (защита от исчезновения тонких линий)
		if eroded.sum() < normalized.sum() * 0.3:
			break
		normalized = eroded.astype(np.uint8)
	
	return normalized


# Новый классификатор на основе только шаблонов
def template_classify(crop, templates_for_quad, min_score=0.5):
	"""Классифицировать кроп по набору шаблонов; если все IoU ниже порога — вернуть None."""
	if not templates_for_quad:
		return None, 0.0
	best_digit = None
	best_score = 0.0
	
	# Нормализуем кроп один раз
	norm_crop = normalize_crop(crop)
	
	for digit, tmpl in templates_for_quad:
		# Нормализуем шаблон
		norm_tmpl = normalize_crop(tmpl)
		
		# Считаем IoU на нормализованных изображениях
		inter = np.logical_and(norm_crop, norm_tmpl).sum()
		union = np.logical_or(norm_crop, norm_tmpl).sum()
		if union == 0:
			score = 0.0
		else:
			score = inter / union
		if score > best_score:
			best_score = float(score)
			best_digit = digit
	return (best_digit, best_score) if best_score >= min_score else (None, best_score)


