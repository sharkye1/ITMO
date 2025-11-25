from tools import *
import argparse
import os


def main():
	parser = argparse.ArgumentParser(description='Распознавание цистерцианского числа из изображения')
	parser.add_argument('image', help='/photo_2025.png', type=str)
	parser.add_argument('--debug', action='store_true', help='сохранить квадранты и показать признаки')
	parser.add_argument('--dump-dir', type=str, default=None, help='папка для дампа (если задана, создаётся)')
	parser.add_argument('--template-dir', type=str, default=None, help='папка с шаблонами (имена: TR_1.png, BR_9.png и т.д.)')
	args = parser.parse_args()
	if args.dump_dir:
		os.makedirs(args.dump_dir, exist_ok=True)
	# load templates if requested
	templates = None
	if args.template_dir:
		from tools import load_templates
		templates = load_templates(args.template_dir)

	total, axis_x, axis_y, details = recognize(args.image, debug=args.debug, dump_dir=args.dump_dir, templates=templates)
	print(f"Detected vertical axis x = {axis_x}, horizontal axis y = {axis_y}")
	print("Quadrant results:")
	# Порядок вывода: Тысячи, Сотни, Десятки, Единицы (для удобства чтения)
	ordering = [('BL', 1000), ('TL', 100), ('BR', 10), ('TR', 1)]
	for q, mul in ordering:
		info = details.get(q, {})
		d = info.get('digit', 0)
		print(f"- {q}: digit={d}, contrib={d*mul}")
	print(f"Total: {total}")


if __name__ == '__main__':
	main()

