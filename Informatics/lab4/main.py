# Простая программа: читает schedule.toml, парсит минимум синтаксиса,
# сохраняет schedule.json и schedule.bin без сторонних библиотек.
# По тз: toml -> json (+ bin? но он у всех)

from tools import to_json, parse

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
	
	

if __name__ == '__main__':
	main()
