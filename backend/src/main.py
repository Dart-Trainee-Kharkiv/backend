from flask import Flask, jsonify, request
from PIL import Image
import io
import json
import base64
import codecs
#our vehicle recognition mode

from vehicle_recognition.vhcl_rec import VehicleRecognition

#creating the Flask application
app = Flask(__name__)

#http get request for /img
@app.route('/img')
def get_img():

    #encode image as a base64 string
    with open("./src/test1.jpeg", "rb") as img:
        b64s = base64.b64encode(img.read())

    f = io.BytesIO(base64.b64decode(b64s))
    pilImg = Image.open(f) # show that image {.show()}

    #dumping image string and size in json
    return jsonify(size=pilImg.size,
                   image=b64s.decode('utf-8'))

#http post request for /img
@app.route('/img', methods=['POST'])
def post_img():

    #mount image object
    j = request.get_json()
    _size = j['size']
    s = j['image']

    #encoding json into bytes
    s_bytes = s.encode()

    #show transfered image
    f = io.BytesIO(base64.b64decode(s_bytes))

    #opening returned img
    pil_img = Image.open(f).convert('RGB')

    #detecting vehicles on the img
    vr = VehicleRecognition(pil_img)
    vehicles = vr.DetectVehicles()

    #return array with vehicles
    return jsonify(vehicles=vehicles), 201

    

#http post request for /tracking
@app.route('/tracking', methods=['POST'])
def post_frames():

    #mount image object
    j = request.get_json()
    frames = j['frames']

    #encoding json into bytes
    s_bytes = []
    for frame in frames:
      s_bytes.append(frame.encode())

    #show transfered image
    pil_imgs = []
    for bytes in s_bytes:
      f = io.BytesIO(base64.b64decode(bytes))
      pil_imgs.append(Image.open(f).convert('RGB'))
      
    #detecting vehicles on the img
    vr = VehicleRecognition(pil_imgs[0])
    vr.DetectVehicles()
    result = vr.TrackVehicles(pil_imgs)
    
    print(result)
    startBoxes = result[0]
    finishBoxes = result[1]
    coords = result[2]
    #return array with vehicles
    return jsonify(startBoxes=startBoxes,finishBoxes=finishBoxes,coords=coords), 201

if __name__ == '__main__':
    app.run(debug=True)

