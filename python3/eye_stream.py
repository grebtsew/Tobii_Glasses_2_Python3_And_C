
import cv2


cap = cv2.VideoCapture("rtsp://192.168.71.50:8554/live/eyes")

while True:
    if cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.resize(frame, (480, 640))
        cv2.imshow('rtsp stream',frame)
        cv2.waitKey(1)

        k = cv2.waitKey(5) & 0xFF
        if k == ord('e'):
            cv2.destroyWindow('rtsp stream')
            break

    else:
        print("No Stream opened")
