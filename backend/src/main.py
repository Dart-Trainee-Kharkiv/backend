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

vrs = {}

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
    
    #hash object
    hash_vr = hash(vr)
    
    #add to dict 
    vrs[hash_vr] =vr
    
    # detecting vehicles
    vehicles = vr.DetectVehicles()

    #return array with vehicles
    return jsonify(vehicles=vehicles, hash=hash_vr), 201
    

#http post request for /tracking
@app.route('/tracking', methods=['POST'])
def post_frame():

    #mount image object
    j = request.get_json()

    frame = j['frame']
    hash_vr = j['hash']

    #encoding json into bytes
    s_bytes = frame.encode()

    #show transfered image
    f = io.BytesIO(base64.b64decode(s_bytes))
    pil_img = Image.open(f).convert('RGB')
      
    #vr = VehicleRecognition(pil_imgs[0])
    vr = vrs[hash_vr]
    
    vr.AddImage(pil_img)
    
    return jsonify(0),201

@app.route('/result', methods=['POST'])
def get_result():

   #mount image object
   j = request.get_json()
   hash_vr = j['hash']
   point = j['point']
   
   vr = vrs[hash_vr]
   vrs.pop(hash_vr)

   result = vr.TrackVehicle(point)
   
   startBoxes = result[0]
   finishBoxes = result[1]
   coords = result[2]
   
   #return array with vehicles
   return jsonify(startBoxes=startBoxes,finishBoxes=finishBoxes,coords=coords), 201
         

if __name__ == '__main__':
    app.run(debug=True)

