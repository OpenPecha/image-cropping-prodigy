import os
import json
import requests
from io import BytesIO
from PIL import Image

def crop_image(image_url, json_data, save_path):
    id_from_json = json_data['id']
    save_filename = os.path.join(save_path, f"{id_from_json}")

    # Check if the file already exists
    if os.path.exists(save_filename):
        print(f"Skipping {id_from_json} because it is already processed.")
        return

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    if 'spans' not in json_data:
        print(f"Skipping {id_from_json} because it has no spans.")
        return

    for span in json_data['spans']:
        x, y = span['x'], span['y']
        width, height = span['width'], span['height']

        left = int(x)
        top = int(y)
        right = int(x + width)
        bottom = int(y + height)

        cropped_img = img.crop((left, top, right, bottom))

        grayscale_img = cropped_img.convert("L")
        bw_img = grayscale_img.point(lambda p: p > 128 and 255)

        # resizing the image to 2x
        new_size = (bw_img.width * 2, bw_img.height * 2)
        resized_img = bw_img.resize(new_size, Image.LANCZOS)

        resized_img.save(save_filename)

def process_jsonl_directory(directory, save_path):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                json_data = json.loads(line)
                image_url = json_data['image']
                answer = json_data.get('answer', '')

                if answer.lower() == 'reject':
                    continue
                crop_image(image_url, json_data, save_path)

def main():
    jsonl_directory = "../../data/annotated_crop_data/"
    save_directory = "../../data/cropped_images"
    process_jsonl_directory(jsonl_directory, save_directory)

if __name__ == "__main__":
    main()
