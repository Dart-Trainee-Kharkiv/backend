from __future__ import print_function
import numpy as np
import sys
import cv2
import random
import os
import json
from random import randint

class VehicleRecognition(object):

    def __init__(self, pil_img = None, names_object="./src/vehicle_recognition/obj.names", weights_file="./src/vehicle_recognition/weights/yolov3-tiny_last_now.weights", config_file="./src/vehicle_recognition/weights/yolov3-tiny_last_cfg.cfg"):#names_object="/Users/illia/speed_est/backend/src/vehicle_recognition/obj.names", weights_file="/Users/illia/speed_est/backend/src/vehicle_recognition/weights/yolov3-tiny_last_now.weights", config_file="/Users/illia/speed_est/backend/src/vehicle_recognition/weights/yolov3-tiny_last_cfg.cfg"):


        #fields
        self.__weights = weights_file
        self.__config = config_file
        self.__names = names_object

        #image that will be analyzed
        self.pil_img = pil_img
        
        #bound boxes
        self.bboxes = None 

    #image source property
    @property
    def pil_img(self):
        return self.__pil_img

    @pil_img.setter
    def pil_img(self, var):
        self.__pil_img = var

    #returns vehicles location on the image
    def DetectVehicles(self, min_conf = 0.2):

        #if the image have been provided
        if self.pil_img != None:
            #array with vehicles locations on the frame
            vehicles = []
            
            #load YOLO pretrained weights and config file
            net = cv2.dnn.readNet(self.__weights, self.__config)

            #classes of the objects that will be located on the image (in our case vehicle only)
            classes = []
            with open(self.__names, "r") as f:
                classes = [line.strip() for line in f.readlines()]

            #loading layers of our neural network
            layer_names = net.getLayerNames()
            outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            #loading our img as cv2 img
            img = cv2.cvtColor(np.array(self.pil_img), cv2.COLOR_RGB2BGR)
            #loading size of our img
            height, width, channels = img.shape

            #detecting objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(outputlayers)

            self.bboxes = []

            #return vehicles location based on confidence level
            for out in outs:
                for detection in out:

                    #get what kind of object was detected and at what confidence
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    #if confidence in detected object is greater than minimum one
                    if confidence > min_conf:

                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)

                        #located vehicle rectangle size
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        #located rectangle co-ordinaters
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        #saving found vehicle locations

                        self.bboxes.append(tuple([x,y,w,h]))
                        vehicles.append([x, y, w, h])

            return vehicles
        return None
    
    def TrackVehicle(self, pil_imgs, point):
 
      # Read first frame
      frame = cv2.cvtColor(np.array(self.pil_img), cv2.COLOR_RGB2BGR)
      

      ## Select box
      bbox = [] 
  
      bboxes = self.bboxes;
      
      pointX = point[0]
      pointY = point[1]
      
      for box in bboxes:
        if (pointX > box[0] and pointX < box[0]+box[2] and pointY > box[1] and pointY < box[1]+box[3]):
            bbox=box
            break
      
      startBox = bbox
      # Create Tracker object
      tracker = cv2.TrackerCSRT_create()      
      ok = tracker.init(frame, tuple(bbox))
                  
      boxes=[]
      resultBoxes=[]
      for frame in pil_imgs:
        
        #
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        
        # get updated location of objects in subsequent frames
        success, bbox = tracker.update(frame)  
        
        resultBoxes.append(box)
        
        # # draw tracked objects
        # for i, newbox in enumerate(boxes):
           # p1 = (int(newbox[0]), int(newbox[1]))
           # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
           # cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        # #show frame
        # cv2.imshow('MultiTracker', frame)  
      vehiclesCoords = []
      

      startX = startBox[0] + startBox[2]/2
      startY = startBox[1] + startBox[3]/2
      endX = bbox[0] + bbox[2]/2
      endY = bbox[1] + bbox[3]/2
      vehiclesCoords.append([startX,startY,endX,endY])

      return [[startBox],[bbox],vehiclesCoords] 
    

