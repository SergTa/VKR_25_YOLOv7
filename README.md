# Модель распознавания тепловизионного изображения объектов дорожной обстановки
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

Для запуска Инференса и соханения видеофайла используйте следующий скрипт

```bash
    python3 ./infer.py
```


Чтобы создать DVC хранилище на виртуальной машине с доступом по SSH и использовать его для хранения исходных датасетов и результатов обучения, выполните следующие шаги:

Шаг 1: Настройка виртуальной машины

Создайте виртуальную машину.
Подключитесь к виртуальной машине по SSH:

   
```bash
ssh serg@158.160.24.226
```

Шаг 2: Установка необходимых инструментов

Установите Python и pip, если они еще не установлены:

   
```bash
sudo apt update
   sudo apt install python3 python3-pip
```
Установите DVC:
   
```bash
pip install dvc
```
Шаг 3: Инициализация DVC в проекте

Создайте новый каталог для вашего проекта или перейдите в существующий:
   
```bash

mkdir my_dvc_project
   cd my_dvc_project
```
Инициализируйте Git репозиторий:

   
```bash
git init
```
Инициализируйте DVC:

   
```bash
dvc init
```

Шаг 4: Настройка удаленного хранилища DVC

Создайте каталог для хранения данных на вашей виртуальной машине:

   
```bash
mkdir /data_input
```

Настройте удаленное хранилище DVC:
   
```bash

dvc remote add -d myremote ssh://serg@158.160.24.226/home/serg/data_input
```

Настройте аутентификацию (если необходимо):

   Если вы используете SSH-ключи, убедитесь, что они настроены правильно. Если требуется, вы можете указать путь к SSH-ключу:
   
```bash

dvc remote modify myremote ssh_key /path/to/your/private/key
```
Шаг 5: Добавление данных и весов модели

Добавьте ваши данные и веса модели в DVC:

   
```bash
dvc add data/
   dvc add runs/detect/
   dvc add datasets/
```
Коммит изменений в Git:

   
```bash

git add data.dvc datasets.dvc .gitignore runs/.gitignore runs/detect.dvc
   git commit -m "Добавлены данные и веса модели с использованием DVC"
```

Шаг 6: Пуш данных в удаленное хранилище

Пуш данных в удаленное хранилище:

   
```bash
dvc push
```
Шаг 7: Проверка статуса DVC

```bash
dvc status
```
