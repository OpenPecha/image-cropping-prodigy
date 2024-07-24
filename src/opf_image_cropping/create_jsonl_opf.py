import csv
import json
import os


def create_jsonl(csv_file, jsonl_files, group_num):
    unique_characters = set()
    jsonl_entries = []

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
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

    num_entries = len(jsonl_entries)
    entries_per_part = num_entries // group_num

    for part in range(group_num):
        start_idx = part * entries_per_part
        end_idx = start_idx + entries_per_part if part < group_num - 1 else num_entries

        part_entries = jsonl_entries[start_idx:end_idx]
        write_jsonl(part_entries, jsonl_files[part])


def write_jsonl(entries, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


def main():
    csv_file_path = '../../data/mapping_csv/derge_ocr_char_mapping.csv'
    jsonl_file_paths = [
        '../../data/output_jsonl/derge_opf_gb.jsonl'
    ]
    group_num = 1

    create_jsonl(csv_file_path, jsonl_file_paths, group_num)


if __name__ == "__main__":
    main()
