def to_json(v, lvl=0):
	"""
	Конвертация объекта в json
	"""
	# v - сам объект
	# lvl - отступы в начале 
	indent = '  '*lvl
	if not v:
		return '{}' # пусто
	if isinstance(v, dict): # для словаря
		parts = []
		for k in v:
			#print(f'ключ: {k},\t значение: {v[k]}')
			parts.append('\n'+indent+'  '+'"'+k+'": '+to_json(v[k], lvl+1))
		return '{' + ','.join(parts) + '\n'+indent+'}'
	
	if isinstance(v, list): # список дней или событий
		parts = []
		for x in v:
			# например для списка событий внутри дня
			parts.append('\n'+indent+'  '+to_json(x, lvl+1)) 
		return '[' + ','.join(parts) + '\n'+indent+']'
	
	if isinstance(v, str): # значения по ключам
		return '"' + v.replace('\\','\\\\').replace('"','\\"') + '"'
	
	return '"'+str(v)+'"'

import time

# Словарь для хранения измерений: ключ = имя функции, значение = список длительностей в секундах
PARSE_TIMINGS = {}

def _record_timing(name: str, duration: float):
	"""Записать измерение в глобальный словарь"""
	PARSE_TIMINGS.setdefault(name, []).append(duration)

def get_timings():
	"""Вернуть текущие измерения (словарь)"""
	return PARSE_TIMINGS

def reset_timings():
	"""Очистить все накопленные измерения"""
	PARSE_TIMINGS.clear()


def _xml_escape(s: str) -> str:
	"""
	Экранирует специальные символы в строке для XML
	Заменяет &, <, >, " и ' на соответствующие сущности
	"""
	return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')


def to_xml(v, lvl=0, tag='root'):
	"""
	Конвертация объекта в простую XML-подобную строку
	Поведение похожее на to_json: используются отступы, словари превращаются в вложенные теги,
	списки — в повторяющиеся элементы с тегом `item`
	Параметры:
	- v: объект для конвертации (dict, list, str, числа и т.д.)
	- lvl: уровень отступа (используется рекурсивно)
	- tag: имя текущего тега для обёртки значения
	"""
	indent = '  ' * lvl
	# Пустые / ложные значения — представляем как самозакрывающийся тег
	if not v:
		return f"{indent}<{tag}/>"
	# Объект (словарь) — каждый ключ становится вложенным тегом
	if isinstance(v, dict):
		parts = []
		for k in v:
			parts.append('\n' + to_xml(v[k], lvl+1, tag=k))
		return f"{indent}<{tag}>" + ''.join(parts) + '\n' + indent + f"</{tag}>"
	# Список — каждый элемент в отдельном <item>
	if isinstance(v, list):
		parts = []
		for x in v:
			parts.append('\n' + to_xml(x, lvl+1, tag='item'))
		return f"{indent}<{tag}>" + ''.join(parts) + '\n' + indent + f"</{tag}>"
	# Строка — эскейпим спецсимволы
	if isinstance(v, str):
		return indent + f"<{tag}>" + _xml_escape(v) + f"</{tag}>"
	# Прочие типы — приводим к строке
	return indent + f"<{tag}>" + _xml_escape(str(v)) + f"</{tag}>"


def del_comment(line):
	"""
	Удаляет комментарии из строки
	"""
	s = ""
	in_q = False
	for c in line:
		if c == '"':
			in_q = not in_q # переключаем состояние в кавычках или не
			s += c
		elif c == '#' and not in_q:
			break
			# комментарий вне кавычек - всем пока
		else:
			s += c
	
	return s.strip()


def parse(lines):
	"""
	Парсит массив строк TOML в структуру данных Python
	"""
	t0 = time.perf_counter()
	data = {}
	current = None  # NONE когда мы в корне
	for raw in lines:
		line = del_comment(raw)
		if not line:
			continue
		if line[0:2] == '[[' and line[-2:] == ']]':
			path = line[2:-2].strip() # путь к структуре в томле
			parts = path.split('.')
			ctx = data
            
			# проход по вложенным структурам
			for part in parts[:-1]:
				if part in ctx:
					v = ctx[part]
					if isinstance(v, list) and v:
						# если уже есть список, последний элемент = текущий контекст
						ctx = v[-1]
					elif isinstance(v, dict):
						ctx = v
						# иначе создаем новую вложенную структуру
				else: 
					ctx[part] = {} 
					ctx = ctx[part]
			name = parts[-1] # имя конечной структуры
			if name not in ctx or not isinstance(ctx.get(name), list):
				# создаем новый список, если его нет
				ctx[name] = []
			new_tbl = {}
			ctx[name].append(new_tbl)
			current = new_tbl
			continue
		if '="' in line or '"' in line:  # ключ = "значение"
			if '=' in line:
				k, v = line.split('=', 1)
				k = k.strip()
				v = v.strip()
				# убрать кавычки
				if v[0] == '"' and v[-1] == '"':
					v = v[1:-1] 
				current = current if current is not None else data 
				current[k] = v
			continue        
	t1 = time.perf_counter()
	_record_timing('parse', t1 - t0)
	return data

# ====== Варианты с готовыми библиотеками (минимум кода) ======
import tomllib 
import orjson

def parse_toml_lib(path):
	"""Прочитать TOML через tomli. Возвращает dict."""
	t0 = time.perf_counter()
	with open(path, 'rb') as f:
		data = tomllib.load(f)
	t1 = time.perf_counter()
	_record_timing('parse_toml_lib', t1 - t0)
	return data

def to_json_lib(data, path, pretty=True):
	"""Сохранить структуру в JSON через orjson."""
	if pretty:
		text = orjson.dumps(data, option=orjson.OPT_INDENT_2).decode('utf-8')
	else:
		text = orjson.dumps(data).decode('utf-8')
	with open(path, 'w', encoding='utf-8') as f:
		f.write(text)
	return text

def toml_to_json_fast(toml_path, json_path, pretty=True):
	"""Скомбинировать: прочитать TOML и сразу сохранить JSON готовыми библиотеками."""
	t0 = time.perf_counter()
	data = parse_toml_lib(toml_path)
	text = to_json_lib(data, json_path, pretty=pretty)
	t1 = time.perf_counter()
	_record_timing('toml_to_json_fast', t1 - t0)
	return text



