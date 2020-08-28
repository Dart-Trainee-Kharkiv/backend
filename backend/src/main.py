from flask import Flask, jsonify, request
from PIL import Image
import numpy as np
import io
import json
import base64
import codecs

# creating the Flask application
app = Flask(__name__)

# http get request for /
@app.route('/')
def get_img():

    # encode image as a base64 string
    with open("test_movie/test1.jpeg", "rb") as img:
        b64s = base64.b64encode(img.read())

    f = io.BytesIO(base64.b64decode(b64s))
    pilImg = Image.open(f) # show that image {.show()}

    # dumping image string and size in json
    return jsonify(size=pilImg.size,
                   image=b64s.decode('utf-8'))

# http post request for /
@app.route('/', methods=['POST'])
def post_img():
    # mount image object
    j = request.get_json()
    _size = j['size']
    s = j['image']

    # encoding json into bytes
    s_bytes = s.encode()

    # show transfered image
    f = io.BytesIO(base64.b64decode(s_bytes))
    pilimage = Image.open(f).show()

    # return image string
    return str(s), 201
