import numpy as np
import cv2
import paho.mqtt.client as mqtt
import time
import datetime
#import requests

count = 0

cap = cv2.VideoCapture(0)  # 640,480
w = 640
h = 480
start = 0


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_disconnect(client, userdata, rc):
    print("Disconnected from server (i.e., broker) with result code "+str(rc))


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
client.loop_start()

while(True):
    ret, frame = cap.read()
    if ret == True:
        # detect face
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = cv2.CascadeClassifier('eye.xml')
        detected = faces.detectMultiScale(frame, 1.3, 5)

        pupilFrame = frame
        pupilO = frame
        windowClose = np.ones((5, 5), np.uint8)
        windowOpen = np.ones((2, 2), np.uint8)
        windowErode = np.ones((2, 2), np.uint8)

        irises = []

        for (ex, ey, ew, eh) in detected:
            iris_w = int(ex + float(ew / 2))
            iris_h = int(ey + float(eh / 2))
            irises.append([np.float32(iris_w), np.float32(iris_h)])

        if (len(irises) < 2):
            # print(start)
            start += 1
            if (start == 15):
                client.publish("waker/sleep_status","SLEEP_ON")
                pass
        else:
            client.publish("waker/sleep_status","SLEEP_OFF")
            start = 0

        # draw square
        for (x, y, w, h) in detected:
            cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 0, 255), 1)
            cv2.line(frame, (x, y), ((x+w, y+h)), (0, 0, 255), 1)
            cv2.line(frame, (x+w, y), ((x, y+h)), (0, 0, 255), 1)
            pupilFrame = cv2.equalizeHist(frame[(y+(h*25//100)):(y+h), x:(x+w)])
            pupilO = pupilFrame
            ret, pupilFrame = cv2.threshold(pupilFrame, 55, 255, cv2.THRESH_BINARY) 
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)

            threshold = cv2.inRange(pupilFrame, 250, 255) 
            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) >= 2:
                maxArea = 0
                MAindex = 0  
                distanceX = []  # delete the left most (for right eye)
                currentIndex = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt, True)
                    center = cv2.moments(cnt)
                    if (center['m00'] != 0):
                        cx, cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                        distanceX.append(cx)
                        if area > maxArea:
                            maxArea = area
                            MAindex = currentIndex
                        currentIndex = currentIndex + 1

                del contours[MAindex]  # remove the picture frame contour
                del distanceX[MAindex]

            eye = 'right'

            if len(contours) >= 2:  # delete the left most blob for right eye
                if eye == 'right':
                    edgeOfEye = distanceX.index(min(distanceX))
                else:
                    edgeOfEye = distanceX.index(max(distanceX))
                del contours[edgeOfEye]
                del distanceX[edgeOfEye]

            if len(contours) >= 1:  # get largest blob
                maxArea = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > maxArea:
                        maxArea = area
                        largeBlob = cnt

            if len(largeBlob) > 0:
                center = cv2.moments(largeBlob)
                cx, cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                cv2.circle(pupilO, (cx, cy), 5, 255, -1)

        cv2.imshow('frame', pupilO)
        # show picture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
