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
# pip install numpy (~5.1 мб)
from collections import deque


def load_and_binarize(path, thresh=128):
	im = Image.open(path).convert('L')
	a = np.array(im)
	bw = (a < thresh).astype(np.uint8)  # 1 — черное (штрих), 0 — фон
	return bw


def find_vertical_axis(bw):
	# Сумма по строкам: количество чёрных пикселей в каждом столбце
	col_sums = bw.sum(axis=0)
	# Если много шума, берём медиану максимумов — но сначала ищем глобальный максимум
	if col_sums.max() == 0:
		# нет черных пикселей
		return bw.shape[1] // 2
	axis_x = int(np.argmax(col_sums))
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
		return {'density':0.0, 'components':0, 'v_near_axis':0.0, 'h_near_axis':0.0, 'diag':0.0}
	y0, y1 = ys.min(), ys.max()
	x0, x1 = xs.min(), xs.max()
	crop = bw[y0:y1+1, x0:x1+1] * mask[y0:y1+1, x0:x1+1]
	area = crop.size
	density = crop.sum() / area
	comps = connected_components_count(crop)

	# проекции: вертикальная полоса рядом с вертикальной осью (если она в пределах квадранта)
	v_near_axis = 0.0
	# Если вертикальная ось внутри crop — измеряем вокруг неё
	if x0 <= axis_x <= x1:
		ax = axis_x - x0
		strip = crop[:, max(0, ax-2):min(crop.shape[1], ax+3)]
		v_near_axis = strip.sum() / strip.size
	else:
		# Если ось находится сразу за границей квадранта, измеряем столбцы у границы
		if x0 > axis_x:
			# crop справа от оси -> левый край
			strip = crop[:, :min(5, crop.shape[1])]
			if strip.size:
				v_near_axis = strip.sum() / strip.size
		elif x1 < axis_x:
			# crop слева от оси -> правый край
			strip = crop[:, max(0, crop.shape[1]-5):]
			if strip.size:
				v_near_axis = strip.sum() / strip.size

	# горизонтальная проекция рядом с горизонтальной осью
	h_near_axis = 0.0
	if y0 <= axis_y <= y1:
		ay = axis_y - y0
		strip = crop[max(0, ay-2):min(crop.shape[0], ay+3), :]
		h_near_axis = strip.sum() / strip.size
	else:
		if y0 > axis_y:
			# crop ниже оси -> верхний край
			strip = crop[:min(5, crop.shape[0]), :]
			if strip.size:
				h_near_axis = strip.sum() / strip.size
		elif y1 < axis_y:
			# crop выше оси -> нижний край
			strip = crop[max(0, crop.shape[0]-5):, :]
			if strip.size:
				h_near_axis = strip.sum() / strip.size

	# диагональная активность: вдоль линии от центра (axis) к внешнему углу квадранта
	diag = 0.0
	cy = axis_y - y0
	cx = axis_x - x0
	H, W = crop.shape
	# определим внешний угол
	corner_y = 0 if cy > H/2 else H-1
	corner_x = 0 if cx > W/2 else W-1
	# пробуем взять 20 точек вдоль диагонали
	samples = 0
	hits = 0
	for t in range(1, 21):
		fy = int(round(cy + (corner_y - cy) * (t/20)))
		fx = int(round(cx + (corner_x - cx) * (t/20)))
		if 0 <= fy < H and 0 <= fx < W:
			samples += 1
			if crop[fy,fx]:
				hits += 1
	if samples:
		diag = hits / samples

	return {'density':density, 'components':comps, 'v_near_axis':v_near_axis, 'h_near_axis':h_near_axis, 'diag':diag}


def classify_quadrant(feat):
	# Эвристический классификатор: преобразует признаки в цифру 0..9
	d = feat['density']
	c = feat['components']
	v = feat['v_near_axis']
	h = feat['h_near_axis']
	diag = feat['diag']

	# игнорируем очень слабые квадранты как нули
	if d < 0.02:
		return 0

	# Базовая логика: чем больше компонентов и плотность — тем больше сложность цифры
	# Эти правила — эвристические и требуют настройки под конкретные изображения.
	# Скорректированные пороги для большей чувствительности
	if c == 1:
		# tie-break: если вертикаль и горизонталь почти равны, предпочитаем вертикаль (устойчивее)
		if abs(v - h) < 0.04 and max(v, h) > 0.18:
			return 1
		if v >= max(h, diag) and v > 0.20:
			return 1
		if h >= max(v, diag) and h > 0.20:
			return 2
		if diag >= max(v, h) and diag > 0.20:
			return 3
		# небольшая плотность с одной компонентой — обычно 1
		return 1
	if c == 2:
		if v > 0.18 and h > 0.18:
			return 4
		if v > 0.18 and diag > 0.18:
			return 5
		if h > 0.18 and diag > 0.18:
			return 6
		# две компоненты, но признаки не явные -> 7
		return 7
	if c == 3:
		if d > 0.08:
			return 8
		return 7
	if c >= 4:
		# много компонент — похоже на сложную форму/шум
		if d < 0.05:
			return 0
		return 9

	# fallback: возвращаем 8 при достаточно плотном заполнении, иначе 1
	if d > 0.12:
		return 8
	return 1


def recognize(path, debug=False, dump_dir=None, templates=None, template_threshold=0.35):
	bw = load_and_binarize(path)
	h, w = bw.shape
	axis_x = find_vertical_axis(bw)
	axis_y = find_horizontal_axis(bw)

	# квадранты: TR=Единицы, BR=Десятки, TL=Сотни, BL=Тысячи
	quads = [('TR', 1), ('BR', 10), ('TL', 100), ('BL', 1000)]
	total = 0
	details = {}
	for name, mul in quads:
		mask = quadrant_mask(bw, axis_x, axis_y, name)
		feat = analyze_quadrant(bw, mask, axis_x, axis_y)
		# prepare crop for optional template matching
		ys, xs = np.where(mask)
		if len(ys):
			y0, y1 = ys.min(), ys.max()
			x0, x1 = xs.min(), xs.max()
			crop = bw[y0:y1+1, x0:x1+1]
		else:
			crop = np.zeros((10,10), dtype=np.uint8)

		digit = classify_quadrant(feat)
		# try template matching if templates provided for this quad
		if templates and name in templates:
			best_digit, score = match_template_to_crop(crop, templates.get(name, []))
			if best_digit is not None and score >= template_threshold:
				if debug:
					print(f"Template match for {name}: {best_digit} (score={score:.2f}) overrides heuristic {digit}")
				digit = best_digit
		details[name] = {'digit': digit, 'feat': feat}
		total += digit * mul

		# debug/dump
		if debug or dump_dir:
			# create a small visualization: crop + mask outline
			ys, xs = np.where(mask)
			if len(ys):
				y0, y1 = ys.min(), ys.max()
				x0, x1 = xs.min(), xs.max()
				crop = bw[y0:y1+1, x0:x1+1]
			else:
				crop = np.zeros((10,10), dtype=np.uint8)

			if dump_dir:
				from PIL import Image as PILImage
				img = (1 - crop) * 255  # invert for visual: 0->255 background, 1->0 stroke
				im = PILImage.fromarray(img.astype(np.uint8), mode='L')
				fname = f"quad_{name}.png"
				im.save(f"{dump_dir}/{fname}")

			if debug:
				print(f"Debug {name}: digit={digit}, feat={feat}")

	return total, axis_x, axis_y, details


def load_templates(template_dir, thresh=128):
	"""Load templates from `template_dir`. Expected filenames: QUAD_DIGIT.png, e.g. TR_1.png"""
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
		# expect format like TR_1 or BL_9
		parts = name.split('_')
		if len(parts) != 2:
			continue
		quad, digit_s = parts
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
	"""Return best-matching digit and IoU score, or (None,0) if no templates."""
	if not templates_for_quad:
		return None, 0.0
	from PIL import Image as PILImage
	H, W = crop.shape
	best_digit = None
	best_score = 0.0
	for digit, tmpl in templates_for_quad:
		# resize template to crop size
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


