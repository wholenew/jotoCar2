#!/usr/bin/env python3

import cv2
from flask import Flask, Response

from models.car_manager import CarManager

# import picamera
# import picamera.array

app = Flask(__name__)

webcamid = 0
fps = 30
frame_width = 320 #320 640
frame_height = 240 #240 360
frame_area = frame_width * frame_height
frame_centerX = frame_width / 2
frame_centerY = frame_height / 2

cap = cv2.VideoCapture(webcamid)
cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

print(cap.get(cv2.CAP_PROP_FPS))
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("fps: " + str(cap.get(cv2.CAP_PROP_FPS)))

face_cascade_path = './haarcascade_frontalface_default.xml'
#face_cascade_path = './haarcascade_eye_tree_eyeglasses.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)

def getCarManager():
    return CarManager()

def getFrames():
    while True:
        ret, frame = cap.read()
        src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(src_gray, (9,9), 0)
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp = 1, minDist = 1, param1 = 20, param2 = 35, minRadius = 1, maxRadius = 30)
        carManager = getCarManager()
        if circles is not None:
            # print(len(circles[0]))
            for i in circles[0]:
                if i[0] == 0.0:
                    break
                cv2.circle(frame, (i[0], i[1]), i[2], (0,0,255), 2)
                print('x:{},y:{},r:{}'.format(i[0], i[1], i[2]))
                if i[2] < 10:
                    carManager.forward()
                elif i[2] > 25:
                    carManager.back()
                elif i[0] > 280:
                    carManager.left()
                elif i[0] < 50:
                    carManager.right()
                else:
                    carManager.stop()
                break
        else:
            carManager.stop()
        #print(frame)

        # frame = cv2.flip(frame, 1) # horizontal flip
        # ret, jpg = cv2.imencode("test.jpg", frame)
        # src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(src_gray, 1.3, 5)

        # if len(faces) > 0:
        #     for x, y, w, h in faces:
                # print(x,y,w,h)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
                # face = jpg[y: y + h, x: x + w]
                # face_gray = src_gray[y: y + h, x: x + w]
                # faceCenterX = x + (w/2)
                # faceCenterY = y + (h/2)
                # faceArea = w * h
                # percentFace = faceArea / frame_area
                # diffX = frame_centerX - faceCenterX
                # diffY = frame_centerY - faceCenterY
                #print(percentFace)
                #print(diffX)
        #         if percentFace > 0.1:
        #             carManager.back()
        #         elif percentFace < 0.05:
        #             carManager.forward()
        #
        #         elif diffX < -80:
        #             carManager.right()
        #         elif diffX > 80:
        #             carManager.left()
        #         else:
        #             carManager.stop()


        ret, jpg = cv2.imencode("test.jpg", frame)
        yield b'--boundary\r\nContent-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n\r\n'

@app.route('/')
def video_feed():
    return Response(getFrames(), mimetype='multipart/x-mixed-replace; boundary=boundary')

# import webbrowser
# webbrowser.get().open("192.168.0.101:5001")
if __name__ == '__main__':
    app.run(host = '192.168.0.103', port = 5001, threaded = False) # only 1 client
    #app.run(host='192.168.0.101', port=5001, threaded=False)  # only
