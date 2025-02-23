import cv2
from ultralytics import YOLO

def process_video_with_tracking(model, input_video_path, output_video_path):
    # Открываем видеофайл
    cap = cv2.VideoCapture(input_video_path)
    
    # Получаем параметры видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Создаем объект для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для mp4
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Выполняем инференс
        results = model(frame)

        # Обрабатываем результаты
        for result in results:
            boxes = result.boxes.xyxy  # Координаты боксов
            confidences = result.boxes.conf  # Уверенность
            class_ids = result.boxes.cls  # Идентификаторы классов

            for box, conf, class_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = map(int, box)  # Преобразуем координаты в целые числа
                label = f'Class: {int(class_id)}, Conf: {conf:.2f}'
                
                # Рисуем бокс и текст на кадре
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Записываем обработанный кадр в выходное видео
        out.write(frame)

    # Освобождаем ресурсы
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model = YOLO('runs/detect/train3/weights/best.pt')  # Замените на путь к вашей модели
    input_video_path = "data/VID-20250129-WA0013.mp4"  # Путь к вашему видеофайлу
    output_video_path = "output_video.mp4"  # Путь для сохранения выходного видео

    process_video_with_tracking(model, input_video_path, output_video_path)