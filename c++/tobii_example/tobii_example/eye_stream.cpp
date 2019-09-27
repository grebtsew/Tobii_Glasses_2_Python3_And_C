#include "stdafx.h"
#include<opencv2/opencv.hpp>
#include <opencv/cv.h>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

int eye_stream_main()

{
	const std::string videoStreamAddress = "rtsp://192.168.71.50:8554/live/eyes";
	cv::VideoCapture capture(videoStreamAddress);

	if (!capture.open(videoStreamAddress)) {
		//Error
	}

	cv::namedWindow("eyes", CV_WINDOW_AUTOSIZE);

	cv::Mat frame;

	while (true) {
		if (!capture.read(frame)) {
			//Error
		} else { 
			cv::imshow("eyes", frame);

			cv::waitKey(30);
		}
	}
}

