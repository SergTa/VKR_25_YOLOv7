# VKR_25_YOLOv7
Предварительные требования

Установите PyTorch в зависимости от вашей системы: инструкция по установке.

Установите дополнительные зависимости:
```bash
    python3 -m venv venv
    source ./venv/bin/activate
    pip install opencv-python matplotlib
    pip install -r requirements.txt
```

Необязательно: 
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
    python3 ./scripts/conver.py
```

Шаг 2: Обучение модели YOLO

Файл конфигурации data.yaml

Для запуска обучения используйте следующий скрипт:

```bash
    python3 ./train_yolo.ipynb
```

Шаг 3: Инференс

Для запуска Инференса используйте следующий скрипт

```bash
    python3 ./inference.ipynb
```

