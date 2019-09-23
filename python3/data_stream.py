'''
    Calibrate and get data_stream from Tobii Glasses 2

    Code in this file i inspired by Tobii Glasses 2 API example code and the
     following repo :
     https://github.com/ddetommaso/TobiiProGlasses2_PyCtrl

    Note: This example program is tested with Python 3 on Windows 10 and Ubuntu 16.04 (precise),
'''

import requests
import json
import time
import threading
import socket
import cv2
import numpy as np
from threading import Thread
import os
import sys

class Data_Stream():

    GLASSES_IP = "192.168.71.50"  # IPv4 address
    PORT = 49152
    base_url = 'http://' + GLASSES_IP
    timeout = 1
    pr_id = None
    pr_name = "project_name"
    pa_id = None
    pa_name = "participant_name"
    ca_id = None
    ca_name = "calibration_name"


    # Keep-alive message content used to request live data and live video streams
    KA_DATA_MSG = "{\"type\": \"live.data.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}"
    #KA_EYES_MSG = "{\"type\": \"live.eyes.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}" # used to sync eyes
    KA_VIDEO_MSG = "{\"type\": \"live.video.unicast\", \"key\": \"some_other_GUID\", \"op\": \"start\"}"


    def mksock(self, peer):
        '''
        Create UDP Socket
        '''
        iptype = socket.AF_INET
        if ':' in peer[0]:
            iptype = socket.AF_INET6
        return socket.socket(iptype, socket.SOCK_DGRAM)

    def send_keepalive_msg(self, socket, msg, peer):
        '''
        Callback function
        '''
        while self.running:
            socket.sendto(msg.encode(), peer)
            time.sleep(self.timeout)

    def put_request(self, api_action, data, in_id, name ):
        url = self.base_url + api_action + "/" + project_name
        data = {"pr_info":{"name":pr_name}}
        json_data = json.dumps(data)
        response = requests.put(url, json_data,headers={'Content-Type': 'application/json'})
        json_data = response.json()
        return json_data

    def get_request(self, api_action):
        url = self.base_url + api_action
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        json_data = response.json()
        return json_data

    def post_request(self,api_action, data=None):
        url = self.base_url + api_action
        data = json.dumps(data)
        response = requests.post(url, data,headers={'Content-Type': 'application/json'})
        json_data = response.json()
        return json_data

    def wait_for_status(self,api_action, key, values):
        url = self.base_url + api_action
        running = True
        while running:

            response = requests.get(url, headers={'Content-Type': 'application/json'})
            json_data = response.json()

            print(" Status: " + json_data[key])

            if json_data[key] in values:
                running = False
            time.sleep(1)

        return json_data[key]


    def create_project(self,name):
        data = {'pr_info': {'Name':name}}
        json_data = self.post_request(api_action='/api/projects',data=data)
        return json_data['pr_id']


    def create_participant(self,project_id):
        data = {'pa_project': project_id, 'pa_info':{'Name': self.pa_name}}
        json_data = self.post_request('/api/participants', data)
        return json_data['pa_id']


    def create_calibration(self,project_id, participant_id):
        data = {'ca_project': project_id, 'ca_type': 'default', 'ca_participant': participant_id, 'ca_info':{'Name':self.ca_name}}
        json_data = self.post_request('/api/calibrations', data)
        return json_data['ca_id']


    def start_calibration(self,calibration_id):
        self.post_request('/api/calibrations/' + calibration_id + '/start')


    def create_recording(self,participant_id):
        data = {'rec_participant': participant_id}
        json_data = self.post_request('/api/recordings', data)
        return json_data['rec_id']

    def project_exists(self,new_id):
        url = self.base_url + "/api/projects"
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        data = json.loads(response.text)
        for projects in data:
            if (projects["pr_id"] == new_id):
                return True
        return False

    def is_not_Valid(self,s_val):
        return s_val!=0

    def get_jsonitem(self,json_id, end_url):
        url = self.base_url + self.end_url
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        data = json.loads(response.text)
        count = 0
        for projects in data:
            if (projects["pr_id"] == new_id):
                return data
            count += 1
        return

    def get_ids(self):
        '''
        Get all ids from rest api
        This is a startup routine
        '''
        '''
        Project
        '''
        # Get project id 'pr_id'
        all_projects = self.get_request(api_action='/api/projects')
        found_project = False
        # Loop and find our project
        print("Searching for Project...")
        for project in all_projects:
            if(str(project).__contains__("pr_info")):

                #print(str(project['pr_info']).__contains__("Name"))
                if(str(project['pr_info']).__contains__("Name")):
                    if(project['pr_info']['Name'] == self.pr_name):
                        self.pr_id = project['pr_id']
                        found_project = True
                        break

        if(not found_project):
            print("Project not found, creating new...")
            self.pr_id = self.create_project(self.pr_name)
            print("Project created!")
        else:
            print("Project found!")

        '''
        Participant
        '''
        all_participants = self.get_request(api_action='/api/participants/')
        found_participant = False

        print("Searching for Participant...")
        for participant in all_participants:
            if(str(participant).__contains__(self.pr_id)):
                if(str(participant).__contains__("pa_info")):
                    if(str(participant['pa_info']).__contains__('Name')):
                        if(participant['pa_info']['Name'] == self.pa_name):
                            self.pa_id = participant['pa_id']
                            found_participant = True
                            break

        if(not found_participant):
            print("Participant not found, creating new...")
            self.pa_id = self.create_participant(self.pr_id)
            print("Participant created!")
        else:
            print("Participant found!")

        '''
        Calibrations
        '''
        all_calibrations = self.get_request(api_action='/api/calibrations/')
        found_calibration = False

        print("Searching for Calibration...")
        for calibration in all_calibrations:

            if(str(calibration).__contains__(self.pa_id)):
                if(str(calibration).__contains__(self.pr_id)):
                    if(str(calibration).__contains__("ca_info")):
                        if(str(calibration['ca_info']).__contains__('Name')):
                            if(calibration['ca_info']['Name'] == self.pa_name):
                                self.ca_id = calibration['ca_id']
                                found_calibration = True
                                break
        if(not found_calibration):
            print("Calibration not found, creating new...")
            self.ca_id = self.create_calibration(self.pr_id, self.pa_id)
            print("Calibration created!")
        else:
            print("Calibration found!")

        return


    def data_stream_loop(self,args):
        '''
        Loop and post datavalues
        See Developerguide Appendix C for value information.
        '''
        sensor = ""
        data_gp = (0,[0.0, 0.0])
        data_pts = (0,0)
        while(True):
            raw_data, address = args.recvfrom(1024)
            raw_data = raw_data.decode('ascii')
            raw_data = raw_data.replace("\\n","")
            raw_data = raw_data.replace("b","")
            data = json.loads(raw_data)

            '''
            Save Synced Sensor data
            '''
            print(data)
            '''
            Save unsynced sensor data to shared variables
            '''
            """
            if (str(data).__contains__("ac")): #accelerometer
            if (str(data).__contains__("pd")):  #pupil-diameter
            if (str(data).__contains__("gd")):  #gaze-direction
            if (str(data).__contains__("gp3")):  #gaze-position-3d
            if (str(data).__contains__("gy")):  #gyro-scope
            """
            '''
            We also have several sync packages to use to know
            time-differences between video and data streams
            '''
            """
            if (str(data).__contains__("\"epts")):  #pts
            if (str(data).__contains__("\"vts")):  #vts
            if (str(data).__contains__("evts")):  #evts
            if (str(data).__contains__("sig")):  #sig
            if (str(data).__contains__("ets")):  #api
            """


    def run(self):
        self.running = True
        peer = (self.GLASSES_IP, self.PORT)
        project_id = None
        participant_id = None
        calibration_id = None

        try:
            # Create socket which will send a keep alive message for the live data stream
            self.data_socket = self.mksock(peer)

            td = threading.Timer(0, self.send_keepalive_msg, [self.data_socket, self.KA_DATA_MSG, peer])
            td.start()

            # Create socket which will send a keep alive message for the live video stream
            self.video_socket = self.mksock(peer)
            tv = threading.Timer(0, self.send_keepalive_msg, [self.video_socket, self.KA_VIDEO_MSG, peer])
            tv.start()

            #Get all id
            self.get_ids()

            # Show config data
            print ("Project: " + self.pr_id, ", Participant: ", self.pa_id, ", Calibration: ", self.ca_id, " ")


            # Start calibration
            print()
            input_var = input("Press enter to calibrate")

            print("Calibration started waiting for calibration...")
            print("Status polling...")
            self.start_calibration(self.ca_id)
            status = self.wait_for_status('/api/calibrations/' + self.ca_id + '/status', 'ca_state', ['failed', 'calibrated'])

            # Show calibration result
            if status == 'failed':
                print ('Calibration failed, using default calibration instead')
            else:
                print ('Calibration successful')

            # Start data_stream
            print("Starting data_stream thread")
            self.data_stream_loop(self.data_socket)

        except Exception as e:
            print(e)
        self.running = False

def main():
    Data_Stream().run()

if __name__ == "__main__":
    main()
