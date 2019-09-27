# Tobii_Glasses_2_Python3_And_C++
Example showing how to get and visualize data_stream, scene camera stream and eye camera stream.
![alt text](https://www.tobiipro.com/imagevault/publishedmedia/02lhuuvawcqhy19glrmp/TobiiPro_Glasses_2_Eye_Tracker_side_3_1.jpg)

# Start
1. Clone or download this repo.
2. Connect to your glasses.
3. Change ip and port in all files, if you are not using default.
4. Run:
```
python starter.py
```

# Motivation
If you prefer Python3 over Python2 there are no examples published by Tobii Pro of how to connect to Tobii glasses 2. Therefore I made this implementation for python3 where we use requests instead of urllib2. If you prefer C++ over Python you can check out the C++ implementation.


# Requirements Python3
These are the required imports for python3:
* requests
* cv2

# Requirements C++
The C++ implementation is developed in Visual Studio 2017 on Windows 10.
These NuGet Packages are used:
* cpprestsdk.v.141 version v2.10.7 (for rest api calls)
* opencv.win.native version v320.1.1-vs141 (require build to be in x64 and in release)
* opencv.win.native.redist v320.1.1-vs141
Some security settings had to be changed in visual studio 2017:
Project -> Project Properties -> C/C++ -> Preprocessors -> Add Preprocessor Definitions :
 `_WINSOCK_DEPRECATED_NO_WARNINGS; _CRT_SECURE_NO_WARNINGS;`


# About
Tobii Glasses 2 is a nifty device produced by Tobii Pro. The product is full of useful components and intresting functions. Such as eye tracking, gyroscope, pupil size and 3d directions. Data from Tobii Glasses 2 is received using udp sockets. From the incoming json objects data can be received and filtered by using these conditions:
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
A great example (python2):
https://github.com/ddetommaso/TobiiProGlasses2_PyCtrl

This code assume from example files in Tobii Glasses 2 API examples:
https://www.tobiipro.com/product-listing/tobii-pro-glasses-2-sdk/

With the download above follows a developers documentation which helps alot!
