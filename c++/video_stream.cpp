#include<opencv2/opencv.hpp>
#include <iostream>


int video_stream_main()

{

cv::VideoCapture capture("rtsp://192.168.71.50:8554/live/scene");

if (!capture->isOpened()) {
    //Error
}

cv::namedWindow("scene", CV_WINDOW_AUTOSIZE);

cv::Mat frame;

while(m_enable) {
    if (!capture->read(frame)) {
        //Error
    }
    cv::imshow("scene", frame);

    cv::waitKey(30);
}
}
