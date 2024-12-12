import re

# Шаблон для сопоставления структурированных строк в логе


log_pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) - "
    r"(Sent____|Received) on (bus\d): ID: (0x[0-9a-f]{1,3})\s*"
    r"(Standard|Extended) Data: b'([0-9a-f ]+)'"
)
def parse_log_line(line):
    #print(line)
    match = log_pattern.match(line)
    if match:
        return {
            'timestamp': match.group(1),
            'action': match.group(2),
            'bus': match.group(3),
            'id': match.group(4),
            'type': match.group(5),
            'data': match.group(6).strip(),
        }
    print("error")
    return None

def test_log_sequence(log_lines):
    # Проверка на наличие строк "Created a socket"
    if not log_lines[0].strip() == "Created a socket" or not log_lines[1].strip() == "Created a socket":
        print("Ошибочные или отсутствующие строки 'Created a socket'")
        return False

    # Ожидаемая последовательность структурированных логов
    expected_sequence = [
        {'action': 'Sent____', 'bus': 'bus1', 'id': '0x150', 'type': 'Standard', 'data': '00 00 00 00 00 00 00 00'},
        {'action': 'Received', 'bus': 'bus2', 'id': '0x0', 'type': 'Extended', 'data': '10 04 00 00 00 00 00 01'},
        {'action': 'Sent____', 'bus': 'bus1', 'id': '0x150', 'type': 'Standard', 'data': '01 00 00 00 00 00 00 00'},
        {'action': 'Received', 'bus': 'bus2', 'id': '0x0', 'type': 'Extended', 'data': '10 04 00 00 00 00 00 00'},
    ]

    # Разбор и проверка структурированных строк начиная с третьей
    parsed_lines = [parse_log_line(line) for line in log_lines[2:]]
    parsed_lines = [line for line in parsed_lines if line is not None]
    #print(parsed_lines)



    for expected, actual in zip(expected_sequence, parsed_lines):
        actual_ts = actual.pop('timestamp', None)
        if expected != actual:
            print(f"{actual_ts} Несоответствие: ожидалось {expected}, но получили {actual}")
            print(f"Тест не пройден")
            return False

    print("Все последовательности соответствуют ожидаемому шаблону.")
    return True

# Путь к файлу журнала
file_path = 'can_logging.log'
# Открываем файл в режиме чтения
with open(file_path, 'r', encoding='utf-8') as file:
    # Читаем строки файла и сохраняем их в списке
    lines = file.readlines()

# Удаляем символы новой строки в конце каждой строки
lines = [line.strip() for line in lines]
test_log_sequence(lines)

