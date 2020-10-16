import os
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import PIL.Image
import json
import threading
import numpy as np
import deblur
from os import system
UPLOAD_FOLDER = 'input/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#python deblur.py --apply --file-path='input/input1.jpeg'

def im2json(im):
    """Convert a Numpy array to JSON string"""
    imdata = pickle.dumps(im)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
    return jstr

def json2im(jstr):
    """Convert a JSON string back to a Numpy array"""
    load = json.loads(jstr)
    imdata = base64.b64decode(load['image'])
    im = pickle.loads(imdata)
    return im

def deblur_fun(img_path):
    deblur.use_the_model(img_path)

@app.route('/', methods=['GET', 'POST'])
def index():
     img_json = request.form['message']
     img = json2im(img_json)
     filename = secure_filename(img.filename)
     input_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

     filename, file_extension = os.path.splitext(input_img_path)
             
     if file_extension == '.png':
         rgba_image = PIL.Image.open(input_img_path)
         rgb_image = rgba_image.convert('RGB')
         rgb_image.save(input_img_path)
     else:
         img.save(input_img_path)
             
     system('python deblur.py --apply --file-path='+input_img_path)
     return "it works"

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
             img = request.files["image"]
             filename = secure_filename(img.filename)
             input_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

             filename, file_extension = os.path.splitext(input_img_path)
             
             if file_extension == '.png':
                 rgba_image = PIL.Image.open(input_img_path)
                 rgb_image = rgba_image.convert('RGB')
                 rgb_image.save(input_img_path)
             else:
                 img.save(input_img_path)
             
             system('python deblur.py --apply --file-path='+input_img_path)
              
             #deblur.use_the_model(UPLOAD_FOLDER)
             #print('im here 00000000000000000000000000000000000000000000000000000000')
             #t1 = threading.Thread(target= deblur_fun, args=[input_img_path])
             #t1.start()
             #t1.join()
             return str('bbom')
    return render_template("upload.html")
    


if __name__ == '__main__':
    app.run(debug=True) heroku
   #app.run(host="0.0.0.0", port=5000, debug=True) #local host

