# Простая программа: читает schedule.toml, парсит минимум синтаксиса,
# сохраняет schedule.json и schedule.bin без сторонних библиотек.
# По тз: toml -> json (+ bin? но он у всех)

from tools import (to_json, parse, to_json_lib,
				parse_toml_lib, to_xml,
				toml_to_json_fast)
import tools
import time

def read_file(path):
	with open(path, "r", encoding="utf-8") as f:
		return f.read().splitlines()


def main():	
	# только для вин
	script_dir = __file__.replace('\\','/').rsplit('/',1)[0]
	# зач rsplit = ['c:/Users/тест/Documents/ITMO/Informatics/lab4', 'main.py'] 
	
	lines = read_file(script_dir + '/schedule.toml')
	
	# Основное задание
	data = parse(lines)
	with open(script_dir + '/schedule.bin', 'wb') as f:
		f.write(str(data).encode('utf-8')) 
	#print(data)

	# Доп. задание 1: bin в json
	json_text = to_json(data)
	with open(script_dir + '/schedule.json', 'w', encoding='utf-8') as f:
		f.write(json_text)
	
	# Доп. задание 2: готовые библиотеки
	data_lib = parse_toml_lib(script_dir + '/schedule.toml')
	to_json_lib(data_lib, script_dir + '/schedule_lib.json', pretty=True)

	# Доп. задание 3: bin в xml 
	xml_text = to_xml(data)
	with open(script_dir + '/schedule.xml', 'w', encoding='utf-8') as f:
		f.write(xml_text)

	# Доп. задание 4: сравнение по времени — измеряем один запуск и масштабируем на 100
	SCALE = 100
	tools.reset_timings()

	# 1) Мой парсер (parse)
	t0 = time.perf_counter()
	data_my = parse(lines)
	t1 = time.perf_counter()
	my_parser_time = t1 - t0

	# 2) Мой конвертер (to_json)
	t0 = time.perf_counter()
	_ = to_json(data_my)
	t1 = time.perf_counter()
	my_converter_time = t1 - t0

	# 3) Мой парсер + готовая сериализация (to_json_lib) — записываем один файл
	t0 = time.perf_counter()
	to_json_lib(data_my, script_dir + '/schedule_lib_from_myparser.json', pretty=True)
	t1 = time.perf_counter()
	my_plus_lib_time = t1 - t0

	# 4) Готовый парсер (tomllib)
	t0 = time.perf_counter()
	data_lib_only = parse_toml_lib(script_dir + '/schedule.toml')
	t1 = time.perf_counter()
	lib_parser_time = t1 - t0

	# 5) Готовая связка (toml_to_json_fast)
	t0 = time.perf_counter()
	toml_to_json_fast(script_dir + '/schedule.toml', script_dir + '/schedule_fast.json', pretty=True)
	t1 = time.perf_counter()
	lib_chain_time = t1 - t0

	# Внутренние замеры, записанные в tools
	internal = tools.get_timings()

	report_lines = []
	report_lines.append(f'Сравнение времени x{SCALE} (секунды)')
	report_lines.append('-----------------------------------------')
	report_lines.append(f"Мой парсер x{SCALE}: \t {my_parser_time * SCALE:.6f}")
	report_lines.append(f"Мой конвертер (to_json) x{SCALE}: \t {my_converter_time * SCALE:.6f}")
	report_lines.append(f"Мой парсер + orjson (to_json_lib) x{SCALE}: \t {my_plus_lib_time * SCALE:.6f}")
	report_lines.append(f"Готовый парсер (tomllib) x{SCALE}: \t {lib_parser_time * SCALE:.6f}")
	report_lines.append(f"Готовая связка (toml_to_json_fast) x{SCALE}: \t {lib_chain_time * SCALE:.6f}")
	report_lines.append('')
	report_lines.append('Internal timings recorded in tools.PARSE_TIMINGS (scaled x{0}, first 10 shown per key):'.format(SCALE))
	for k, v in internal.items():
		vals = v[:10]
		report_lines.append(f"  {k}: {', '.join(f'{(x * SCALE):.6f}' for x in vals)}")

	# Записываем в файл compare.txt
	with open(script_dir + '/compare.txt', 'w', encoding='utf-8') as f:
		f.write('\n'.join(report_lines))

	print('Comparison written to', script_dir + '/compare.txt')

if __name__ == '__main__':
	main()
