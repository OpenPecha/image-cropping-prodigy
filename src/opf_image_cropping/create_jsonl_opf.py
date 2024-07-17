import csv
import json
import os

def create_jsonl(csv_file, jsonl_ga, jsonl_gb):
    unique_characters = set()
    jsonl_entries = []

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            char = row[0]
            reference = json.loads(row[4])
            line_info = []
            image_url = ""

            for image_name, lines in reference.items():
                image_name_without_ext = os.path.splitext(image_name)[0]
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

    def write_jsonl(entries, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for entry in entries:
                    json.dump(entry, f, ensure_ascii=False)
                    f.write('\n')
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")

    write_jsonl(jsonl_entries[:split_point], jsonl_ga)
    write_jsonl(jsonl_entries[split_point:], jsonl_gb)

if __name__ == "__main__":
    csv_file_path = '../../data/mapping_csv/derge_char_mapping.csv'
    jsonl_file_ga_path = '../../data/output_jsonl/derge_opf_ga.jsonl'
    jsonl_file_gb_path = '../../data/output_jsonl/derge_opf_gb.jsonl'

    create_jsonl(csv_file_path, jsonl_file_ga_path, jsonl_file_gb_path)
