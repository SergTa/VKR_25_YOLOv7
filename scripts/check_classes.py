import os

annotations_dir = './yolov5/yolo_dataset/labels/'

invalid_classes = []

for filename in os.listdir(annotations_dir):
       if filename.endswith('.txt'):
           with open(os.path.join(annotations_dir, filename), 'r') as f:
               for line in f:
                   class_index = int(line.split()[0])
                   if class_index == 3:
                       invalid_classes.append(filename)

if invalid_classes:
       print("Ошибочные аннотации с классом 9 обнаружены в следующих файлах:")
       print("\n".join(invalid_classes))
else:
       print("Ошибочные классы не найдены.")