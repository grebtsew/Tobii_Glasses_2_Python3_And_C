int eye_stream_main()

{

str url = "rtsp://192.168.71.50:8554/live/eyes"
cv::VideoCapture capture(url);

if (!capture->isOpened()) {
    //Error
}

cv::namedWindow("eyes", CV_WINDOW_AUTOSIZE);

cv::Mat frame;

while(m_enable) {
    if (!capture->read(frame)) {
        //Error
    }
    cv::imshow("eyes", frame);

    cv::waitKey(30);
}

}
