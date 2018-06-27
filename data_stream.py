'''
    Example for how to create a project, participant, calibration and recording.
    In order to make the calibration pass the keep-alive messages needs to be sent.

    Note: This example program is tested with Python 3 on Windows 10 (precise),

'''

import requests
import json
import time
import threading
import socket
import cv2
import numpy as np
from threading import Thread

GLASSES_IP = "192.168.71.50"  # IPv4 address
PORT = 49152
base_url = 'http://' + GLASSES_IP
timeout = 1

# Keep-alive message content used to request live data and live video streams
KA_DATA_MSG = "{\"type\": \"live.data.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}"
KA_VIDEO_MSG = "{\"type\": \"live.video.unicast\", \"key\": \"some_other_GUID\", \"op\": \"start\"}"


# Create UDP socket
def mksock(peer):
    iptype = socket.AF_INET
    if ':' in peer[0]:
        iptype = socket.AF_INET6
    return socket.socket(iptype, socket.SOCK_DGRAM)


# Callback function
def send_keepalive_msg(socket, msg, peer):
    global running
    while running:
        socket.sendto(msg.encode(), peer)
        time.sleep(timeout)


def post_request(api_action, data=None):
    url = base_url + api_action
    data = json.dumps(data)
    response = requests.post(url, data,headers={'Content-Type': 'application/json'})
    json_data = response.json()
    return json_data


def wait_for_status(api_action, key, values):
    url = base_url + api_action
    running = True
    while running:

        response = requests.get(url, data,headers={'Content-Type': 'application/json'})
        json_data = response.json()
        if json_data[key] in values:
            running = False
        time.sleep(1)

    return json_data[key]


def create_project():
    json_data = post_request('/api/projects')
    return json_data['pr_id']


def create_participant(project_id):
    data = {'pa_project': project_id}
    json_data = post_request('/api/participants', data)
    return json_data['pa_id']


def create_calibration(project_id, participant_id):
    data = {'ca_project': project_id, 'ca_type': 'default', 'ca_participant': participant_id}
    json_data = post_request('/api/calibrations', data)
    return json_data['ca_id']


def start_calibration(calibration_id):
    post_request('/api/calibrations/' + calibration_id + '/start')


def create_recording(participant_id):
    data = {'rec_participant': participant_id}
    json_data = post_request('/api/recordings', data)
    return json_data['rec_id']


def start_recording(recording_id):
    post_request('/api/recordings/' + recording_id + '/start')


def stop_recording(recording_id):
    post_request('/api/recordings/' + recording_id + '/stop')

def data_stream_loop(args):
    '''
    Loop and print datavalues
    See Developerguide Appendix C for value information.
    '''
    while(True):
        data, address = args.recvfrom(1024)
        #if (str(data).__contains__("ac")): #accelerometer
        #if (str(data).__contains__("pd")):  #pupil-diameter
        #if (str(data).__contains__("gd")):  #gaze-direction
        #if (str(data).__contains__("gp\"")):  #gaze-position
        #if (str(data).__contains__("gp3")):  #gaze-position-3d
        #if (str(data).__contains__("gy")):  #gyro-scope
        if(str(data).__contains__("\"pts")):

        #    if (str(data).__contains__("left"):  #left eye
        #    if (str(data).__contains__("right"):  #right eye

            '''
            We also have several sync packages to use to know
            time-differences between video and data streams
            '''
            print (data)

    print("Ending datastream Thread")


if __name__ == "__main__":
    global running
    running = True
    peer = (GLASSES_IP, PORT)

    try:
        # Create socket which will send a keep alive message for the live data stream
        data_socket = mksock(peer)
        td = threading.Timer(0, send_keepalive_msg, [data_socket, KA_DATA_MSG, peer])
        td.start()

        # Create socket which will send a keep alive message for the live video stream
        video_socket = mksock(peer)
        tv = threading.Timer(0, send_keepalive_msg, [video_socket, KA_VIDEO_MSG, peer])
        tv.start()

        input_var = input("Press enter to calibrate")

        print("Starting data_stream thread")
        data_stream_loop(data_socket)

    except:
        print("Error")

    running = False
