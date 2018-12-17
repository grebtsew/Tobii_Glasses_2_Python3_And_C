# Tobii_Glasses_2_Python3
Example showing how to get and visualize data_stream, scene camera stream and eye camera stream.
![alt text](https://www.tobiipro.com/imagevault/publishedmedia/02lhuuvawcqhy19glrmp/TobiiPro_Glasses_2_Eye_Tracker_side_3_1.jpg)

# Start
Clone or download this repo and run:
```
python starter.py
```

# Motivation
If you prefer Python3 over Python2 there are no examples of how to connect to Tobii glasses 2.
Here we use requests instead of urllib2.

# Requirements
These are the required imports for python3:
* requests
* cv2

# About
Tobii Glasses 2 is a nifty device produced by Tobii Pro. The product is full of useful components and intresting functions. Such as eye tracking, gyroscope, pupil size and 3d directions. Data from Tobii Glasses 2 is received using udp sockets. From the incoming json objects data can be received by filtered using these conditions:
```
# Data gathering
if (str(data).__contains__("ac")): #accelerometer
if (str(data).__contains__("pd")):  #pupil-diameter
if (str(data).__contains__("gd")):  #gaze-direction
if (str(data).__contains__("gp\"")):  #gaze-position
if (str(data).__contains__("gp3")):  #gaze-position-3d
if (str(data).__contains__("gy")):  #gyro-scope
if(str(data).__contains__("\"pts")):
if (str(data).__contains__("left"):  #left eye
if (str(data).__contains__("right"):  #right eye
```

# See also
A great example (python2): (See here how to sync data!)
https://github.com/ddetommaso/TobiiProGlasses2_PyCtrl

This code assume from example files in Tobii Glasses 2 API examples:
https://www.tobiipro.com/product-listing/tobii-pro-glasses-2-sdk/

With the download above follows a developers documentation which helps alot!
