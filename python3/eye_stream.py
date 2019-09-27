
import cv2


cap = cv2.VideoCapture("rtsp://192.168.71.50:8554/live/eyes")

while True:
    if cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.resize(frame, (480, 640))
        cv2.imshow('rtsp eye stream',frame)
        cv2.waitKey(1)

        k = cv2.waitKey(5) & 0xFF
        if k == ord('e'):
            cv2.destroyWindow('rtsp eye stream')
            break

    else:
        pass
        #print("No Stream opened")
