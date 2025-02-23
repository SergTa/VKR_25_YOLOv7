import os
import json
import zipfile
import random
import shutil
from pathlib import Path

def unique_filename(directory, filename):
    """Generate a unique filename by appending a counter if needed."""
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
    return new_filename

def convert_coco_to_yolo(zip_file_path, output_dir, train_split=0.8):
    # Create output directories
    images_train_dir = os.path.join(output_dir, 'train/images/')
    labels_train_dir = os.path.join(output_dir, 'train/labels/')
    images_val_dir = os.path.join(output_dir, 'val/images/')
    labels_val_dir = os.path.join(output_dir, 'val/labels/')

    os.makedirs(images_train_dir, exist_ok=True)
    os.makedirs(labels_train_dir, exist_ok=True)
    os.makedirs(images_val_dir, exist_ok=True)
    os.makedirs(labels_val_dir, exist_ok=True)

    # Unzip the archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    # Path to the annotation file
    annotation_file = os.path.join(output_dir, 'annotations/', 'instances_default.json')

    # Load annotations
    with open(annotation_file, 'r') as f:
        coco_data = json.load(f)

    # Create a category mapping
    category_map = {category['id']: category['name'] for category in coco_data['categories']}

    # List to store image and annotation data
    images_annotations = []

    # Process images
    for image in coco_data['images']:
        image_id = image['id']
        image_file_name = image['file_name']
        image_width = image['width']
        image_height = image['height']
        original_image_path = os.path.join(output_dir, 'images/', image_file_name)

        temp_image_path = os.path.join(output_dir, 'images/', image_file_name)
        if os.path.exists(original_image_path):
            if not os.path.exists(temp_image_path):
                shutil.copy(original_image_path, temp_image_path)

            # Ensure the labels directory exists
            temp_label_dir = os.path.dirname(os.path.join(output_dir, 'labels/', f"{Path(image_file_name).stem}.txt"))
            os.makedirs(temp_label_dir, exist_ok=True)  # Create labels directory if it does not exist
            
            temp_label_file_path = os.path.join(output_dir, 'labels/', f"{Path(image_file_name).stem}.txt")
            with open(temp_label_file_path, 'w') as label_file:
                # Find annotations for the current image
                for annotation in coco_data['annotations']:
                    if annotation['image_id'] == image_id:
                        category_id = annotation['category_id']
                        bbox = annotation['bbox']  # [x, y, width, height]

                        # Convert bbox to YOLO format
                        x_center = (bbox[0] + bbox[2] / 2) / image_width
                        y_center = (bbox[1] + bbox[3] / 2) / image_height
                        width = bbox[2] / image_width
                        height = bbox[3] / image_height

                        # Write the annotation to the file
                        label_file.write(f"{category_id - 1} {x_center} {y_center} {width} {height}\n")  # category_id - 1 for 0-indexing
                        
                images_annotations.append((temp_image_path, temp_label_file_path))

    # Shuffle and split data into train and validation sets
    random.shuffle(images_annotations)
    split_index = int(len(images_annotations) * train_split)

    train_data = images_annotations[:split_index]
    val_data = images_annotations[split_index:]

    # Move files to respective directories
    for img_path, label_path in train_data:
        unique_image_name = unique_filename(images_train_dir, Path(img_path).name)
        target_image_path = os.path.join(images_train_dir, unique_image_name)

        if img_path != target_image_path:
            shutil.move(img_path, target_image_path)

        label_file_name = Path(label_path).name
        target_label_path = os.path.join(labels_train_dir, label_file_name)

        if label_path != target_label_path:
            shutil.move(label_path, target_label_path)

    for img_path, label_path in val_data:
        unique_image_name = unique_filename(images_val_dir, Path(img_path).name)
        target_image_path = os.path.join(images_val_dir, unique_image_name)

        if img_path != target_image_path:
            shutil.move(img_path, target_image_path)

        label_file_name = Path(label_path).name
        target_label_path = os.path.join(labels_val_dir, label_file_name)

        if label_path != target_label_path:
            shutil.move(label_path, target_label_path)

if __name__ == "__main__":
    zip_files = ['data/job_1313_dataset_2024_12_02_17_14_57_coco.zip', 
                 './data/job_1314_dataset_2024_12_05_17_06_51_coco.zip', 
                 './data/job_1315_dataset_2024_12_11_16_06_58_coco.zip', 
                 './data/job_1326_dataset_2024_12_17_15_42_23_coco.zip', 
                 './data/job_1327_dataset_2024_12_20_15_19_37_coco.zip', 
                 './data/job_1328_dataset_2024_12_25_07_32_23_coco.zip', 
                 './data/job_1329_dataset_2024_12_25_08_17_19_coco.zip'   
                ]  # Укажите пути к вашим zip-архивам
    output_directory = 'datasets'  # Укажите выходную директорию

    for zip_file in zip_files:
        convert_coco_to_yolo(zip_file, output_directory)