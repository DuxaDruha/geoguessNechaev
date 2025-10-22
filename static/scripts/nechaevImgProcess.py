import cv2
import os
import numpy as np
import face_recognition 

class Photos:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = None
        self.face_locations = []  # Координаты найденных лиц

        self.load_image()

    def load_image(self):
        if not os.path.exists(self.img_path):
            raise FileNotFoundError(f"Файл '{self.img_path}' не найден(")
        
        self.img = cv2.imread(self.img_path)
        if self.img is None:
            raise ValueError(f"Ошибка загрузки изображения '{self.img_path}'")

    def face_check(self):
        if self.img is None:
            return "Изображение не найдено"

        # Конвертируем BGR в RGB (ну короче библа работает ток с форматом RGB)
        rgb_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        self.face_locations = face_recognition.face_locations(rgb_img, model="hog") 
        # HOG: (Histogram of Oriented Gradients) - это метод cv

        if len(self.face_locations) == 0:
            return "нет людей"
        else:
            return f"найдено лиц: {len(self.face_locations)}"

    def coord(self):
        coords = []
        for top, right, bottom, left in self.face_locations:
            w = right - left
            h = bottom - top
            coords.append((left, top, w, h))  # x, y, width, height (x - верхний левый угол, y - нижний правый)
        if len(coords) == 0:
            return "а где лица?"
        return coords

    def nechaev(self, nechaev_face_path="static/img/nechaev.jpg"):
        if self.img is None:
            print("Изображение не загружено!")
            return None

        if not os.path.exists(nechaev_face_path):
            raise FileNotFoundError(f"Файл не найден")

        nechaev_face = cv2.imread(nechaev_face_path)
        if nechaev_face is None:
            raise ValueError(f"Ошибка загрузки изображения")

        result_img = self.img.copy()

        for i, (left, top, w, h) in enumerate(self.coord()):
            resized_nechaev = cv2.resize(nechaev_face, (w, h))
            result_img[top:top + h, left:left + w] = resized_nechaev

        base_name = os.path.splitext(self.img_path)[0]
        output_path = f"{base_name}_nechaev.jpg"
        cv2.imwrite(output_path, result_img)
        print(f"Изображение сохранено как: {output_path}")

        return result_img


    def show_image(self):
        if self.img is None:
            print("Изображение не загружено!")
            return

        img_copy = self.img.copy()
        for (x, y, w, h) in self.coord():
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_copy, 'Face', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Face Detection', img_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()