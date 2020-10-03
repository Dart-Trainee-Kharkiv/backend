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

@app.route('/img', methods=['POST'])
def post_img():

    #mount image object
    j = request.get_json()
    s = j['frame']

    #encoding json into bytes
    s_bytes = s.encode()

    #show transfered image
    f = io.BytesIO(base64.b64decode(s_bytes))
    pil_img=Image.open(f).convert('RGB')

    #detecting vehicles on the img
    vr = VehicleRecognition(pil_img)
    vehicles = vr.DetectVehicles()

    #return array with vehicles
    return jsonify(vehicles=vehicles), 201
    

#http post request for /tracking
@app.route('/tracking', methods=['POST'])
def post_frame():

    #mount image object
    j = request.get_json()
    frames = j['frames']
    point = j['point']

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
    result = vr.TrackVehicle(pil_imgs, point)
    
    #print(result)
    startBoxes = result[0]
    finishBoxes = result[1]
    coords = result[2]
    #return array with vehicles
    print(result)
    return jsonify(startBoxes=startBoxes,finishBoxes=finishBoxes,coords=coords), 201

    

#http post request for /multitracking
@app.route('/multitracking', methods=['POST'])
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
    
    #print(result)
    startBoxes = result[0]
    finishBoxes = result[1]
    coords = result[2]
    #return array with vehicles
    return jsonify(startBoxes=startBoxes,finishBoxes=finishBoxes,coords=coords), 201

if __name__ == '__main__':
    app.run(debug=True)

