from opf_image_cropping.create_jsonl_opf import create_jsonl
import unittest
import csv
import json
import os
from tempfile import TemporaryDirectory
from collections import defaultdict
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestCreateJSONL(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.csv_file_path = os.path.join(self.temp_dir.name, 'test.csv')
        self.jsonl_file_path = os.path.join(self.temp_dir.name, 'output.jsonl')

        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['char', 'col2', 'col3', 'col4', 'reference'])
            writer.writerow(['ཀ', '', '', '', json.dumps({"image1.jpg": [["line", 1]]})])
            writer.writerow(['ཁ', '', '', '', json.dumps({"image2.jpg": [["line", 2]]})])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_jsonl(self):
        create_jsonl(self.csv_file_path, self.jsonl_file_path)
        with open(self.jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
            lines = jsonl_file.readlines()

        expected_output = [
            {"id": "ཀ_1.jpg", "image": "glyph/glyph-source-images/derge/image1.jpg", "text": "ཀ", "line_info": [1]},
            {"id": "ཁ_1.jpg", "image": "glyph/glyph-source-images/derge/image2.jpg", "text": "ཁ", "line_info": [2]},
        ]

        output = [json.loads(line) for line in lines]

        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
