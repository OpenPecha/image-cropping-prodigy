import csv
import json
import os
from collections import defaultdict


def create_jsonl(csv_file, jsonl_file):
    jsonl_entries = []
    char_counter = defaultdict(int)

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            char = row[0]
            reference = json.loads(row[4])
            image_url = ""

            for image_name, lines in reference.items():
                image_name_without_ext = os.path.splitext(image_name)[0]
                image_url = f"glyph/glyph-source-images/derge/{image_name_without_ext}.jpg"

                for line in lines:
                    line_info = [line[1]]
                    char_counter[char] += 1
                    jsonl_entry = {
                        "id": f"{char}_{char_counter[char]}.jpg",
                        "image": image_url,
                        "text": char,
                        "line_info": line_info
                    }
                    jsonl_entries.append(jsonl_entry)

    # for sorting the entries by char
    jsonl_entries.sort(key=lambda entry: entry['text'])

    write_jsonl(jsonl_entries, jsonl_file)


def write_jsonl(entries, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


def main():
    csv_file_path = '../../data/mapping_csv/derge_opf_char_mapping.csv'
    jsonl_file_path = '../../data/output_jsonl/10_glyphs_derge_opf.jsonl'

    create_jsonl(csv_file_path, jsonl_file_path)


if __name__ == "__main__":
    main()
