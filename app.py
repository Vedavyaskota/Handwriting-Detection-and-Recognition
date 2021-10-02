import time
import os
from flask import Flask, render_template, request

from ocr_core import ocr_core
from model import hdr_predition
from model import hdr_accuracy
from model import hdr_img

UPLOAD_FOLDER = '/static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    start = time.time()
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            extracted_text = ocr_core(file)
            end = time.time()
            predition_time =round(end-start,3)
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   predition_time=predition_time,
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/digit', methods=['GET', 'POST'])
def digit_page():
    start = time.time()
    if request.method == 'POST':
        index = request.form['index']
        predition = hdr_predition(index)
        accuracy = hdr_accuracy()
        img_src=hdr_img(index)
        end = time.time()
        predition_time =round(end-start,3)
        return render_template('digit.html',
                                predition=predition,
                                accuracy=accuracy,
                                predition_time=predition_time,
                                img_src=img_src)
    elif request.method == 'GET':
        return render_template('digit.html')

if __name__ == '__main__':
	app.debug = True
	app.run()
