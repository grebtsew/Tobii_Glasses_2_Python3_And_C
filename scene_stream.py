
import cv2
import json

cap = cv2.VideoCapture("rtsp://192.168.71.50:8554/live/scene")

while True:
    if cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.resize(frame, (640, 480))
        frame_obj = {"TobiiCam" : frame}
        cv2.imshow('rtsp stream',frame)
        cv2.waitKey(1)

        k = cv2.waitKey(5) & 0xFF
        if k == ord('e'):
            cv2.destroyWindow('rtsp stream')
            break

    else:
        print("No Stream opened")
