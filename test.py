import cv2
from flask import Flask, Response

from models.car_manager import CarManager

app = Flask(__name__)

webcamid = 0
fps = 30
frame_width = 320
frame_height = 240
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
face_cascade = cv2.CascadeClassifier(face_cascade_path)

def getCarManager():
    return CarManager()

def getFrames():
    while True:
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1) # horizontal flip
        # ret, jpg = cv2.imencode("test.jpg", frame)
        src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(src_gray, 1.3, 5)

        for x, y, w, h in faces:
            # print(x,y,w,h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
            # face = jpg[y: y + h, x: x + w]
            # face_gray = src_gray[y: y + h, x: x + w]
            faceCenterX = x + (w/2)
            faceCenterY = y + (h/2)
            faceArea = w * h
            percentFace = faceArea / frame_area
            diffX = frame_centerX - faceCenterX
            diffY = frame_centerY - faceCenterY
            carManager = getCarManager()
            if diffX < -30:
                carManager.left()
            elif diffX < 30:
                carManager.right()
            elif percentFace > 0.3:
                carManager.back()
            elif percentFace < 0.02:
                carManager.forward()
            else:
                carManager.stop()

        ret, jpg = cv2.imencode("test.jpg", frame)
        yield b'--boundary\r\nContent-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n\r\n'

@app.route('/')
def video_feed():
    return Response(getFrames(), mimetype='multipart/x-mixed-replace; boundary=boundary')

# import webbrowser
# webbrowser.get().open("192.168.0.101:5001")

app.run(host = '192.168.0.101', port = 5001, threaded = False) # only 1 client