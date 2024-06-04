import json
from urllib import request

from flask import Flask, flash, request, redirect, render_template, url_for, Response
from werkzeug.utils import secure_filename

import net.predict
from parse import parse_data
import os

app = Flask(__name__, template_folder='D:/DSTU/практика ИИ/PokemonNet/net/templates')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
OUTPUT_SIZE = 3

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
@app.route('/upload', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print(file)
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(filepath)
        file.save(filepath)
        # Предикт keras по картинке
        prediction = net.predict.Predict(filepath)
        # Выдача результата как массива из вероятностей
        result = prediction.predict()
        # Парсим данные
        result = parse_data(result)
        result["name"] = file.filename.split('.')[0]
        print(result["name"])
        os.remove(filepath)
        # Записываем результат в текстовый файл
        with open('predictions/predictions.txt', 'w') as f:
            f.write(str(result))
        return Response(status=200)

@app.route('/upload', methods=['GET'])
def show_predict():
    # Если еще не было предикта
    if os.stat('predictions/predictions.txt').st_size == 0:
        return redirect(request.url)
    with open('predictions/predictions.txt', 'r+') as f:
        result = f.read()
    json_acceptable_string = result.replace("'", "\"")
    result = json.loads(json_acceptable_string)  # DICTIONARY
    return render_template("prediction.html",
                           label=result["name"],
                           generation=result["generation"],
                           type1=result["type1"],
                           type2=result["type2"])


if __name__ == '__main__':
    app.run(debug=True)
