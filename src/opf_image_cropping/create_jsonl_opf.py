import csv
import json


def create_jsonl(csv_file, jsonl_ga, jsonl_gb):
    unique_characters = set()
    jsonl_entries = []

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            char = row[0]
            reference = json.loads(row[4])
            line_info = []

            for image_name, lines in reference.items():
                image_name_without_ext = image_name.split('.')[0]
                image_url = f"glyph/glyph-source-images/derge/{image_name_without_ext}.jpg"
                line_info.extend(line[1] for line in lines)

            if char not in unique_characters:
                unique_characters.add(char)
                jsonl_entry = {
                    "id": f"{char}.jpg",
                    "image_url": image_url,
                    "text": char,
                    "line_info": line_info
                }
                jsonl_entries.append(jsonl_entry)

    split_point = len(jsonl_entries) // 2

    with open(jsonl_ga, 'w', encoding='utf-8') as f1:
        for entry in jsonl_entries[:split_point]:
            json.dump(entry, f1, ensure_ascii=False)
            f1.write('\n')

    with open(jsonl_gb, 'w', encoding='utf-8') as f2:
        for entry in jsonl_entries[split_point:]:
            json.dump(entry, f2, ensure_ascii=False)
            f2.write('\n')


csv_file_path = '../../data/mapping_csv/derge_char_mapping.csv'
jsonl_file_ga_path = '../../data/output_jsonl/derge_opf_ga.jsonl'
jsonl_file_gb_path = '../../data/output_jsonl/derge_opf_gb.jsonl'

create_jsonl(csv_file_path, jsonl_file_ga_path, jsonl_file_gb_path)
