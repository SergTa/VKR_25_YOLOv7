import json
import os
import shutil
from pathlib import Path

def convert_json_to_yolo(json_file, images_dir, output_dir):
    with open(json_file) as f:
        data = json.load(f)

    # Создаем выходные директории
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    labels_dir = os.path.join(output_dir, 'labels')
    images_output_dir = os.path.join(output_dir, 'images')
    Path(labels_dir).mkdir(parents=True, exist_ok=True)
    Path(images_output_dir).mkdir(parents=True, exist_ok=True)

    for image_info in data['images']:
        img_id = image_info['id']
        img_file = image_info['file_name']
        img_path = os.path.join(images_dir, img_file)

        # Копируем изображение в выходную директорию
        shutil.copy(img_path, os.path.join(images_output_dir, img_file))

        # Нахождение аннотаций для текущего изображения
        label_file_path = os.path.join(labels_dir, f"{Path(img_file).stem}.txt")
        with open(label_file_path, 'w') as label_file:
            for annotation in data['annotations']:
                if annotation['image_id'] == img_id:
                    category_id = annotation['category_id']-1
                    bbox = annotation['bbox']
                    # Размеры Yolo
                    x_center = (bbox[0] + bbox[2] / 2) / image_info['width']
                    y_center = (bbox[1] + bbox[3] / 2) / image_info['height']
                    width = bbox[2] / image_info['width']
                    height = bbox[3] / image_info['height']
                    # Запись в файл
                    label_file.write(f"{category_id} {x_center} {y_center} {width} {height}\n")
                    
    print("Конвертация завершена")

# Пример использования
convert_json_to_yolo('./data/annotations/instances_default.json', './data/images/', './yolov7/yolo_dataset/')