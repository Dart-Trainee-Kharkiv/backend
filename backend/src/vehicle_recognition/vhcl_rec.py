from __future__ import print_function
import numpy as np
import sys
import cv2
import random
import os
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
    
    def TrackVehicles(self, pil_imgs):
      # Set video to load
      #videoPath = "src/vehicle_recognition/videos/cars2.mp4"

      # Create a video capture object to read videos
      #cap = cv2.VideoCapture(videoPath)
 
      # Read first frame
      #success, frame = cap.read()
      frame = cv2.cvtColor(np.array(self.pil_img), cv2.COLOR_RGB2BGR)
      

      ## Select boxes
      bboxes = []
      colors = [] 
      resultBoxes = []
  
      #vr = VehicleRecognition(frame)
  
      #bboxesFromApp= vr.DetectVehicles()
  
  
      #bboxesFromApp = [(363, 213, 152, 108), (124, 226, 52, 41), (114, 222, 71, 52), (178, 233, 13, 24), (207, 232, 20, 19), (201, 230, 34, 25), (233, 230, 16, 28), (227, 228, 32, 31), (255, 231, 63, 40), (249, 229, 75, 44), (524, 232, 48, 30), (551, 230, 36, 35)]
      #bboxes = bboxesFromApp
      bboxes = self.bboxes;
      resultBoxes.append(self.bboxes);
      
      for bbox in bboxes:
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
      
      print('Selected bounding boxes {}'.format(bboxes))
      print(colors)

      ## Initialize MultiTracker
      # There are two ways you can initialize multitracker
      # 1. tracker = cv2.MultiTracker("CSRT")
      # All the trackers added to this multitracker
      # will use CSRT algorithm as default
      # 2. tracker = cv2.MultiTracker()
      # No default algorithm specified

      # Initialize MultiTracker with tracking algo
      # Specify tracker type
  
      # Create MultiTracker object
      multiTracker = cv2.MultiTracker_create()

      # Initialize MultiTracker 
      for bbox in bboxes:
        multiTracker.add(cv2.TrackerKCF_create(), frame, bbox)


      # # Process video and track objects
      # while cap.isOpened():
        # success, frame = cap.read()
        
        # # get updated location of objects in subsequent frames
        # success, boxes = multiTracker.update(frame)   

        # # draw tracked objects
        # for i, newbox in enumerate(boxes):
           # p1 = (int(newbox[0]), int(newbox[1]))
           # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
           # cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        # # show frame
        # cv2.imshow('MultiTracker', frame)  

        # # quit on ESC button
        # if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
          # break
          
        
      for frame in pil_imgs:
        
        #
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        
        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)  
        
        resultBoxes.append(boxes.tolist())
        
        # draw tracked objects
        for i, newbox in enumerate(boxes):
           p1 = (int(newbox[0]), int(newbox[1]))
           p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
           cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        # show frame
        #cv2.imshow('MultiTracker', frame)  

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
          break            

      return resultBoxes
    

