import sys
import os
import unittest
import json
import tempfile
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from opf_image_cropping.create_jsonl_opf import create_jsonl

class TestCreateJsonl(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.test_dir.cleanup)

        self.csv_file_path = os.path.join(self.test_dir.name, 'test.csv')
        self.jsonl_file_paths = [
            os.path.join(self.test_dir.name, 'test_part1.jsonl'),
            os.path.join(self.test_dir.name, 'test_part2.jsonl')
        ]

        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['char', 'col2', 'col3', 'col4', 'reference'])
            writer.writerow(['ཀ', 'data', 'data', 'data', '{"image1.jpg": [[0, 1], [1, 2]]}'])
            writer.writerow(['ཁ', 'data', 'data', 'data', '{"image2.jpg": [[0, 1], [1, 2]]}'])
            writer.writerow(['ག', 'data', 'data', 'data', '{"image3.jpg": [[0, 1], [1, 2]]}'])
            writer.writerow(['ང', 'data', 'data', 'data', '{"image4.jpg": [[0, 1], [1, 2]]}'])

    def test_create_jsonl(self):
        create_jsonl(self.csv_file_path, self.jsonl_file_paths, group_num=2)

        with open(self.jsonl_file_paths[0], 'r', encoding='utf-8') as f:
            part1_entries = [json.loads(line) for line in f]
        
        with open(self.jsonl_file_paths[1], 'r', encoding='utf-8') as f:
            part2_entries = [json.loads(line) for line in f]

        expected_entries_part1 = [
            {
                "id": "ཀ.jpg",
                "image": "glyph/glyph-source-images/derge/image1.jpg",
                "text": "ཀ",
                "line_info": [1, 2]
            },
            {
                "id": "ཁ.jpg",
                "image": "glyph/glyph-source-images/derge/image2.jpg",
                "text": "ཁ",
                "line_info": [1, 2]
            }
        ]
        expected_entries_part2 = [
            {
                "id": "ག.jpg",
                "image": "glyph/glyph-source-images/derge/image3.jpg",
                "text": "ག",
                "line_info": [1, 2]
            },
            {
                "id": "ང.jpg",
                "image": "glyph/glyph-source-images/derge/image4.jpg",
                "text": "ང",
                "line_info": [1, 2]
            }
        ]

        self.assertEqual(part1_entries, expected_entries_part1)
        self.assertEqual(part2_entries, expected_entries_part2)

if __name__ == "__main__":
    unittest.main()