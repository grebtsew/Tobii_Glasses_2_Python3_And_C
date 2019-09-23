import os
from threading import Thread

'''
To solve 2 captures and a datastream from glasses we try seperate programs here

This program executes each program from own threads.

See data_stream.py, eye_stream.py and scene_stream.py!

Change command in this file if pythonpath is different!
'''

def start_data():
    print("Start data_stream")
    os.system("python data_stream.py")

def start_eye():
    print("Start eye_stream")
    os.system("python eye_stream.py")

def start_scene():
    print("Start scene_stream")
    os.system("python scene_stream.py")

# Start here!
thread1 = Thread(target = start_data)
thread1.start()
thread2 = Thread(target = start_eye)
thread2.start()
thread3 = Thread(target = start_scene)
thread3.start()
