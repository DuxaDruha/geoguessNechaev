from flask import Flask, render_template
from flask import Flask
import random
from flask import request
import os
from flask import jsonify
import tempfile
import cv2
import base64

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html", title='Main page')


@app.route("/play")
def playRandomMode():
    random_coordinate1 = random.randint(55692711, 55868057)
    random_coordinate2 = random.randint(37544543, 37718527)
    random_coordinate1 /= 10 ** 6
    random_coordinate2 /= 10 ** 6
    random_coordinate = [random_coordinate1, random_coordinate2]
    
    random_coordinate_copy = list(str(elem) for elem in random_coordinate)
    chosen_file = open("static/coordinates/chosen.txt", 'w')
    chosen_file.write(', '.join(random_coordinate_copy))
    chosen_file.close()
    
    return render_template("play.html",
                           title='Play NechaevGuess',
                           data=random_coordinate,
                           yandex_api_key=os.getenv('YANDEX_MAPS_API_KEY'))

# PLAY CODE END


# Nechaev
@app.route('/nechaev')
def nechaev_page():
    return render_template('nechaev.html')


@app.route('/process-nechaev', methods=['POST'])
def process_nechaev():
    try:
        file = request.files['image']
        
        # Сохраняем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            file.save(temp_file.name)
            input_path = temp_file.name

        # Динамически импортируем скрипт
        import importlib.util
        spec = importlib.util.spec_from_file_location("nechaev", "static/scripts/nechaevImgProcess.py")
        nechaev_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(nechaev_module)
        
        # Обрабатываем изображение
        photo = nechaev_module.Photos(input_path)
        
        # Сначала проверяем есть ли лица
        face_result = photo.face_check()
        if "нет людей" in face_result or "а где лица" in face_result:
            os.unlink(input_path)
            return jsonify({'success': False, 'error': 'На изображении не найдено лиц'})
        
        # Если лица есть - обрабатываем
        result_img = photo.nechaev("static/img/nechaev.jpg")

        if result_img is not None:
            # Конвертируем в base64
            _, buffer = cv2.imencode('.jpg', result_img)
            processed_image_str = base64.b64encode(buffer).decode()
            
            os.unlink(input_path)
            return jsonify({
                'success': True,
                'image': f"data:image/jpeg;base64,{processed_image_str}"
            })
        else:
            os.unlink(input_path)
            return jsonify({'success': False, 'error': 'Ошибка обработки'})
            
    except Exception as e:
        if 'input_path' in locals() and os.path.exists(input_path):
            os.unlink(input_path)
        return jsonify({'success': False, 'error': str(e)})



def main():
    app.run(port=8080)
    print()


if __name__ == '__main__':
    main()