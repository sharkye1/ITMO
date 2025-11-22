# простой парсер TOML без библиотек
# читает schedule.toml, создает schedule.json и schedule.bin

# функция для парсинга TOML
def parse_toml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    data = {}
    current_table = []
    
    for line in lines:
        line = line.strip()
        
        # пропускаем пустые строки
        if not line:
            continue
        
        # убираем комментарии
        if "#" in line:
            # проверяем, не внутри ли строки комментарий
            in_string = False
            for i in range(len(line)):
                if line[i] == '"':
                    in_string = not in_string
                elif line[i] == "#" and not in_string:
                    line = line[:i].strip()
                    break
        
        # пропускаем строки, которые стали пустыми после удаления комментариев
        if not line:
            continue
        
        # обрабатываем таблицы [[name]]
        if line.startswith("[[") and line.endswith("]]"):
            table_name = line[2:-2].strip()
            parts = table_name.split(".")
            current_table = parts
            
            # создаем структуру
            if len(parts) == 1:
                # простая таблица [[days]]
                if parts[0] not in data:
                    data[parts[0]] = []
                data[parts[0]].append({})
            else:
                # вложенная таблица [[days.events]]
                parent = parts[0]
                child = parts[1]
                if parent not in data:
                    data[parent] = []
                if len(data[parent]) == 0:
                    data[parent].append({})
                if child not in data[parent][-1]:
                    data[parent][-1][child] = []
                data[parent][-1][child].append({})
        
        # обрабатываем ключ = "значение"
        elif "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            # убираем кавычки из значения
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            # определяем, куда записать значение
            if not current_table:
                # корневой уровень
                data[key] = value
            elif len(current_table) == 1:
                # простая таблица
                table_name = current_table[0]
                if table_name in data and len(data[table_name]) > 0:
                    data[table_name][-1][key] = value
            elif len(current_table) == 2:
                # вложенная таблица
                parent = current_table[0]
                child = current_table[1]
                if parent in data and len(data[parent]) > 0:
                    if child in data[parent][-1] and len(data[parent][-1][child]) > 0:
                        data[parent][-1][child][-1][key] = value
    
    return data

# функция для создания JSON вручную
def to_json(obj, indent=0):
    spaces = "  " * indent
    
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        result = "{\n"
        items = list(obj.items())
        for i, (k, v) in enumerate(items):
            result += spaces + "  " + '"' + str(k) + '": '
            result += to_json(v, indent + 1)
            if i < len(items) - 1:
                result += ","
            result += "\n"
        result += spaces + "}"
        return result
    elif isinstance(obj, list):
        if not obj:
            return "[]"
        result = "[\n"
        for i, item in enumerate(obj):
            result += spaces + "  " + to_json(item, indent + 1)
            if i < len(obj) - 1:
                result += ","
            result += "\n"
        result += spaces + "]"
        return result
    elif isinstance(obj, str):
        return '"' + obj + '"'
    else:
        return str(obj)

# основная программа
if __name__ == "__main__":
    # читаем и парсим TOML
    data = parse_toml("schedule.toml")
    
    # сохраняем JSON
    json_content = to_json(data)
    with open("schedule.json", "w", encoding="utf-8") as f:
        f.write(json_content)
    print("Файл schedule.json создан")
    
    # сохраняем бинарный файл
    bin_content = bytes(str(data), "utf-8")
    with open("schedule.bin", "wb") as f:
        f.write(bin_content)
    print("Файл schedule.bin создан")
