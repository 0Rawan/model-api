from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
##################
#import cv2
import base64
import json
import pickle
from PIL import Image
## Sending OpenCV image in JSON ##

######################
from flask import Flask, jsonify, request, render_template
#import firebase_admin
#from firebase_admin import credentials, firestore, initialize_app
from flask_sqlalchemy import SQLAlchemy
########
import matplotlib.pyplot as plt
# Keras
import keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Initialize Firestore DB
#cred = credentials.Certificate('key.json')
#default_app = initialize_app(cred)
#db = firestore.client()
#todo_ref = db.collection('todos')

#fialed because I think I should use google colud service
 
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



model = keras.models.load_model( 'models/gen_model3000.h5', compile=False )
output = model.output
print(output)

''''
test on a dummy picture 
img_path = 'pics/Screenshot from 2019-03-11 15-35-39.png'
img = image.load_img(img_path, target_size=(96, 96))

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

x = preprocess_input(x, mode='caffe')

print('000000000000000000000000000')
preds = model.predict(x)
arr_ = np.squeeze(preds)
plt.imshow(arr_)
plt.savefig("mygraph.png")
print('here2222222222222222222222')

jstr = im2json(arr_)
print(len(jstr))
imj= json2im(jstr)
plt.imshow(imj)
plt.savefig("mygraph2.png")
'''



from flask import redirect, url_for, request, render_template, session
from werkzeug.utils import secure_filename
# Define a flask app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLAALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/img.db'
db = SQLAlchemy(app)

class Img (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text)
    
    def __init__(self,  img):
        slef.img = img
## 23 sep
@app.route('/', methods=['GET', 'POST'])
def handle_request():
    and_json = request.files["text/plain"] 
    return str(and_json)'
### meduim ahmad
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            jstr = im2json(image)
            session['my_var'] = str(len(jstr))

            my_img  = Img(jstr)      
            db.session.add(my_data)
            db.session.commit()
                                   
            return jsonify(jstr)
    return render_template("upload.html")

#  I think this is redanant
@app.route('/api')
def api():
   my_var = session.get('my_var', None)
   return jsonify({'output' : my_var})

if __name__ == '__main__':
    app.run(debug=True)





