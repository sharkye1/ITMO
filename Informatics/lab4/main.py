# Простая программа: читает schedule.toml, парсит минимум синтаксиса,
# сохраняет schedule.json и schedule.bin без сторонних библиотек.

def read_file(path):
	with open(path, "r", encoding="utf-8") as f:
		return f.read().splitlines()

def strip_comment(line):
	s = ""
	q = False
	for c in line:
		if c == '"':
			q = not q
			s += c
		elif c == '#' and not q:
			break
		else:
			s += c
	return s.strip()

def to_json(v, lvl=0):  # простой pretty принтер
	ind = '  '*lvl
	if isinstance(v, dict):
		if not v:
			return '{}'
		parts = []
		for k in v:
			parts.append('\n'+ind+'  '+'"'+k+'": '+to_json(v[k], lvl+1))
		return '{' + ','.join(parts) + '\n'+ind+'}'
	if isinstance(v, list):
		if not v:
			return '[]'
		parts = []
		for x in v:
			parts.append('\n'+ind+'  '+to_json(x, lvl+1))
		return '[' + ','.join(parts) + '\n'+ind+']'
	if isinstance(v, str):
		return '"' + v.replace('\\','\\\\').replace('"','\\"') + '"'
	return '"'+str(v)+'"'

def parse(lines):
	data = {}
	current = None  # текущая таблица для ключей
	for raw in lines:
		line = strip_comment(raw)
		if not line:
			continue
		if line.startswith('[[') and line.endswith(']]'):
			path = line[2:-2].strip()
			parts = path.split('.')
			ctx = data
			# пройти промежуточные части
			for p in parts[:-1]:
				if p in ctx:
					v = ctx[p]
					if isinstance(v, list) and v:
						ctx = v[-1]
					elif isinstance(v, dict):
						ctx = v
				else:
					ctx[p] = {}
					ctx = ctx[p]
			name = parts[-1]
			if name not in ctx or not isinstance(ctx.get(name), list):
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
				if v.startswith('"') and v.endswith('"'):
					v = v[1:-1]
				target = current if current is not None else data
				target[k] = v
	return data

def main():	
	# только для вин
	script_dir = __file__.replace('\\','/').rsplit('/',1)[0] 
	lines = read_file(script_dir + '/schedule.toml')
	
	data = parse(lines)
	json_text = to_json(data)
	with open(script_dir + '/schedule.json', 'w', encoding='utf-8') as f:
		f.write(json_text)
	with open(script_dir + '/schedule.bin', 'wb') as f:
		f.write(str(data).encode('utf-8'))

if __name__ == '__main__':
	main()
