# VKR_25_YOLOv7
Предварительные требования

Установите PyTorch в зависимости от вашей системы: инструкция по установке.

Установите дополнительные зависимости:
```bash
    python3 -m venv venv
    source ./venv/bin/activate
    pip install opencv-python matplotlib
```

Клонируйте репозиторий YOLOv5:
```bash
git clone https://github.com/ultralytics/yolov5.git
   cd yolov5
   pip install -r requirements.txt
```
Клонируйте репозиторий YOLOv5:
```bash
git clone https://github.com/WongKinYiu/yolov7.git
    cd yolov7
    pip install -r requirements.txt
```


Шаг 1: Подготовка данных
Реорганизуйте данные, чтобы они соответствовали формату YOLO. Для этого вам нужно будет конвертировать аннотации из JSON в формат YOLO (txt файлы).

``` bash
    python3 ./scripts/conv_json2txt.py
```

Автоматическое разделение на тренировочную и валидационную выборки 80/20

``` bash
    python ./scripts/split.py
```
Шаг 2: Обучение модели YOLOv5

Файл конфигурации data.yaml

Для запуска обучения используйте следующий скрипт:

```bash
    !python train.py --img 640 --batch 16 --epochs 50 --data data.yaml --weights yolov5s.pt --cache
```

запустите main.py
