import csv
import json


def create_jsonl(csv_file, jsonl_file):
    unique_characters = set()
    jsonl_entries = []

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            char = row[0]
            reference = json.loads(row[4])

            for image_name, lines in reference.items():
                image_name_without_ext = image_name.split('.')[0]
                image_url = f"glyph/glyph-source-images/derge/{image_name_without_ext}.tif"

            line_info = []
            for image_name, lines in reference.items():
                for line in lines:
                    line_info.append(line[1])

            if char not in unique_characters:
                unique_characters.add(char)

                jsonl_entry = {
                    "id": f"{char}.tif",
                    "image_url": image_url,
                    "text": char,
                    "line_info": line_info
                }

                jsonl_entries.append(jsonl_entry)

    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for entry in jsonl_entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


csv_file_path = '../../data/mapping_csv/derge_char_mapping.csv'
jsonl_file_path = '../../data/output_jsonl/derge_opf.jsonl'

create_jsonl(csv_file_path, jsonl_file_path)
