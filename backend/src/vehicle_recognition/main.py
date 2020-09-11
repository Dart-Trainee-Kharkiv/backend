import cv2
import numpy as np

class VehicleRecognition(object):

    def __init__(self, pil_img = None, names_object="obj.names", weights_file="./weights/yolov3-tiny_last_now.weights", config_file="./weights/yolov3-tiny_last_cfg.cfg"):#names_object="/Users/illia/speed_est/backend/src/vehicle_recognition/obj.names", weights_file="/Users/illia/speed_est/backend/src/vehicle_recognition/weights/yolov3-tiny_last_now.weights", config_file="/Users/illia/speed_est/backend/src/vehicle_recognition/weights/yolov3-tiny_last_cfg.cfg"): 

        #fieldds
        self.__weights = weights_file
        self.__config = config_file
        self.__names = names_object

        #image that will be analyzed
        self.pil_img = pil_img

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
            print(self.__weights, self.__config)
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
                        vehicles.append([x, y, w, h])

            return vehicles
        return None
