from tools import *
import argparse
import os


def main():
	"""
	Главная функция для распознавания цистерцианского числа из изображения
	"""
	parser = argparse.ArgumentParser(description='Распознавание цистерцианского числа из изображения')
	parser.add_argument('image', help='/photo_2025.png', type=str)
	parser.add_argument('--debug', action='store_true', help='сохранить квадранты и показать признаки')
	parser.add_argument('--dump-dir', type=str, default=None, help='папка для дампа (если задана, создаётся)')
	parser.add_argument('--template-dir', type=str, default=None, help='папка с шаблонами (имена: TR_1.png, BR_9.png и т.д.)')
	args = parser.parse_args()
	if args.dump_dir:
		os.makedirs(args.dump_dir, exist_ok=True)
	# загрузка шаблонов, если указана папка
	templates = None
	if args.template_dir:
		from tools import load_templates
		templates = load_templates(args.template_dir)

	total, axis_x, axis_y, details = recognize(args.image, debug=args.debug, dump_dir=args.dump_dir, templates=templates)
	print(f"Обнаружена вертикальная ось x = {axis_x}, горизонтальная ось y = {axis_y}")
	print("Результаты по квадрантам:")
	# Порядок вывода: Тысячи (BL), Сотни (BR), Десятки (TL), Единицы (TR)
	ordering = [('BL', 1000), ('BR', 100), ('TL', 10), ('TR', 1)]
	for q, mul in ordering:
		info = details.get(q, {})
		d = info.get('digit', 0)
		print(f"- {q}: цифра={d}, вклад={d*mul}")
	print(f"Итого: {total}")
	
	return total  # Возвращаем результат для возможности тестирования


if __name__ == '__main__':
	main()

