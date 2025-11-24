def to_json(v, lvl=0):
	"""
	Конвертация объекта в json
	"""
	# v - сам объект
	# lvl - отступы в начале 
	indent = '  '*lvl
	if not v:
		return '{}' # пусто
	if isinstance(v, dict): # например день (с событиями)
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
	- v: объект для конвертации (dict, list, str, числа итд)
	- lvl: уровень отступа (используется рекурсивно)
	- tag: имя текущего тега для обёртки значения
	"""
	indent = '  ' * lvl
	# Пустые / ложные значения — представляем как самозакрывающийся тег
	if not v:
		return f"{indent}<{tag}/>"
	
	# Объект (словарь) — каждый ключ становится вложенным тегом
	if isinstance(v, dict): # например день с событиями
		parts = []
		for k in v:
			parts.append('\n' + to_xml(v[k], lvl+1, tag=k))
		return f"{indent}<{tag}>" + ''.join(parts) + '\n' + indent + f"</{tag}>"
	
	# Список — каждый элемент в отдельном <item>
	if isinstance(v, list): # список дней или событий
		parts = []
		for x in v:
			parts.append('\n' + to_xml(x, lvl+1, tag='item'))
		return f"{indent}<{tag}>" + ''.join(parts) + '\n' + indent + f"</{tag}>"
	
	# Строка — эскейпим спецсимволы
	if isinstance(v, str): # значения по ключам
		return indent + f"<{tag}>" + _xml_escape(v) + f"</{tag}>"
	
	# Прочие типы — приводим к строке
	return indent + f"<{tag}>" + _xml_escape(str(v)) + f"</{tag}>" # например числа 


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
	Парсер TOML из строкового списка lines.
	
	Поддерживает:
	- Массивы таблиц [[table]]
	- Простые таблицы [table]
	- Строки в кавычках "value"
	- Числа (целые и float)
	- Булевы значения (true/false)
	- Массивы ["a", "b", 123]
	- Комментарии #
	"""
	data = {}
	current = None  # текущая таблица для ключей
	
	for raw in lines:
		line = del_comment(raw).strip()
		if not line:
			continue
		
		# массив таблиц [[table.name]]
		if line.startswith('[[') and line.endswith(']]'):
			path = line[2:-2].strip()
			parts = path.split('.')
			ctx = data
			
			# проход по промежуточным частям
			for part in parts[:-1]:
				if part in ctx:
					v = ctx[part]
					if isinstance(v, list) and v:
						ctx = v[-1]
					elif isinstance(v, dict):
						ctx = v
				else:
					ctx[part] = {}
					ctx = ctx[part]
			
			name = parts[-1]
			if name not in ctx or not isinstance(ctx.get(name), list):
				ctx[name] = []
			new_tbl = {}
			ctx[name].append(new_tbl)
			current = new_tbl
			continue
		
		# простая таблица [table.name]
		if line.startswith('[') and line.endswith(']'):
			path = line[1:-1].strip()
			parts = path.split('.')
			ctx = data
			
			# создаем вложенную структуру
			for part in parts:
				if part not in ctx:
					ctx[part] = {}
				ctx = ctx[part]
			
			current = ctx
			continue
		
		# ключ = значение
		if '=' in line:
			k, v = line.split('=', 1)
			k = k.strip()
			v = v.strip()
			
			# парсим значение
			parsed_value = parse_value(v)
			
			# записываем в текущую таблицу или корень
			target = current if current is not None else data
			target[k] = parsed_value
	
	return data


def parse_value(v):
	"""
	Парсит значение TOML: строка, число, булево, массив.
	Возвращает Python-объект.
	"""
	v = v.strip()
	
	# строка в двойных кавычках
	if v.startswith('"') and v.endswith('"'):
		return v[1:-1]
	
	# строка в одинарных кавычках (literal string)
	if v.startswith("'") and v.endswith("'"):
		return v[1:-1]
	
	# булево значение
	if v == 'true':
		return True
	if v == 'false':
		return False
	
	# массив [...]
	if v.startswith('[') and v.endswith(']'):
		return parse_array(v)
	
	# число (целое или float)
	if is_number(v):
		if '.' in v or 'e' in v.lower():
			return float(v)
		else:
			return int(v)
	
	# если ничего не подошло, возвращаем как строку
	return v


def parse_array(s):
	"""
	Парсит массив вида ["a", "b", 123, true].
	Возвращает список Python.
	"""
	s = s[1:-1].strip()  # убираем [ ]
	if not s:
		return []
	
	result = []
	current = ""
	in_string = False
	quote_char = None
	
	for c in s:
		if c in ('"', "'") and not in_string:
			in_string = True
			quote_char = c
			current += c
		elif c == quote_char and in_string:
			in_string = False
			current += c
			quote_char = None
		elif c == ',' and not in_string:
			# конец элемента
			item = current.strip()
			if item:
				result.append(parse_value(item))
			current = ""
		else:
			current += c
	
	# последний элемент
	item = current.strip()
	if item:
		result.append(parse_value(item))
	
	return result


def is_number(s):
	"""
	Проверяет, является ли строка числом (int или float).
	"""
	s = s.strip()
	if not s:
		return False
	
	# убираем знак +/-
	if s[0] in ('+', '-'):
		s = s[1:]
	
	# проверяем на float с точкой или экспонентой
	if 'e' in s.lower():
		parts = s.lower().split('e')
		if len(parts) != 2:
			return False
		# проверяем мантиссу и экспоненту
		return is_simple_number(parts[0]) and is_simple_number(parts[1].lstrip('+-'))
	
	return is_simple_number(s)


def is_simple_number(s):
	"""
	Проверяет простое число (может содержать одну точку).
	"""
	if not s:
		return False
	
	dot_count = 0
	for c in s:
		if c == '.':
			dot_count += 1
			if dot_count > 1:
				return False
		elif not c.isdigit():
			return False
	
	return True

# ====== Варианты с готовыми библиотеками (минимум кода) ======
import tomllib # встроенный в Python 3.11+
import orjson # pip install orjson

def parse_toml_lib(path):
	"""
	Прочитать TOML через tomli. Возвращает dict
	"""
	with open(path, 'rb') as f:
		data = tomllib.load(f)
	return data

def to_json_lib(data, path, pretty=True):
	"""
	Сохранить структуру в JSON через orjson
	"""
	if pretty:
		text = orjson.dumps(data, option=orjson.OPT_INDENT_2).decode('utf-8')
	else:
		text = orjson.dumps(data).decode('utf-8')
	with open(path, 'w', encoding='utf-8') as f:
		f.write(text)
	return text

def toml_to_json_fast(toml_path, json_path, pretty=True):
	"""
	Скомбинировать: прочитать TOML и сразу сохранить JSON готовыми библиотеками
	"""
	data = parse_toml_lib(toml_path)
	text = to_json_lib(data, json_path, pretty=pretty)
	return text



