def to_json(v, lvl=0):
	"""
	Конвертация объекта в json-подобную строку
	"""
	# v - объект для конвертации в json
	# lvl - отступы в начале 
	indent = '  '*lvl
	if not v:
		return '{}' # пусто
	if isinstance(v, dict): # для словаря
		parts = []
		for k in v:
			#print(f'key: {k},\t value: {v[k]}')
			parts.append('\n'+indent+'  '+'"'+k+'": '+to_json(v[k], lvl+1))
		return '{' + ','.join(parts) + '\n'+indent+'}'
	if isinstance(v, list): # список дней или событий
		parts = []
		for x in v:
			parts.append('\n'+indent+'  '+to_json(x, lvl+1))
		return '[' + ','.join(parts) + '\n'+indent+']'
	if isinstance(v, str): # значения по ключам
		return '"' + v.replace('\\','\\\\').replace('"','\\"') + '"'
	return '"'+str(v)+'"'


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
	return data

# ====== Варианты с готовыми библиотеками (минимум кода) ======
import tomllib  # используем tomli (Python <3.11) как tomllib
import orjson

def parse_toml_lib(path):
	"""Прочитать TOML через tomli. Возвращает dict."""
	with open(path, 'rb') as f:
		return tomllib.load(f)

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
	data = parse_toml_lib(toml_path)
	return to_json_lib(data, json_path, pretty=pretty)



