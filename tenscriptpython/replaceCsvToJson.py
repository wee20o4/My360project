import csv
import json

csv_file = 'data.csv'
json_file = 'data.json'

with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = list(reader)  # Mỗi dòng là một dict

# Ghi dữ liệu sang file JSON
with open(json_file, mode='w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f'Chuyển đổi {csv_file} thành {json_file} thành công!')

# Chuyển đổi data.csv thành data.json thành công!    