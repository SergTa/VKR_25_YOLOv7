import os
import shutil
import random

# Параметры
data_dir = './yolo_dataset'
train_image_dir = './dataset/images/train'
val_image_dir = './dataset/images/val'
train_label_dir = './dataset/labels/train'
val_label_dir = './dataset/labels/val'
split_ratio = 0.8  # Доля для тренировочной выборки

# Создаем папки для тренировочной и валидационной выборок, если они не существуют
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# Получаем списки изображений и аннотаций
image_files = [f for f in os.listdir(os.path.join(data_dir, 'images')) if f.endswith('.png')]
annotation_files = [f for f in os.listdir(os.path.join(data_dir, 'labels')) if f.endswith('.txt')]

# Проверяем, что количество изображений и аннотаций совпадает
assert len(image_files) == len(annotation_files), "Количество изображений и аннотаций должно совпадать."

# Перемешиваем файлы
random.shuffle(image_files)

# Определяем количество файлов для тренировочной выборки
split_index = int(len(image_files) * split_ratio)

# Разбиваем на тренировочную и валидационную выборки
train_images = image_files[:split_index]
val_images = image_files[split_index:]

# Копируем файлы в соответствующие папки
for image_file in train_images:
    shutil.copy(os.path.join(data_dir, 'images', image_file), os.path.join(train_image_dir, image_file))
    shutil.copy(os.path.join(data_dir, 'labels', image_file.replace('.png', '.txt')), os.path.join(train_label_dir, image_file.replace('.png', '.txt')))

for image_file in val_images:
    shutil.copy(os.path.join(data_dir, 'images', image_file), os.path.join(val_image_dir, image_file))
    shutil.copy(os.path.join(data_dir, 'labels', image_file.replace('.png', '.txt')), os.path.join(val_label_dir, image_file.replace('.png', '.txt')))

print("Разделение на тренировочную и валидационную выборки завершено.")