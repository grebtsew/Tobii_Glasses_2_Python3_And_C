#include<opencv2/opencv.hpp>
#include<iostream>
using namespace std;
using namespace cv;
int main()
{
  Mat img = imread("lena.jpg");
  namedWindow("image", WINDOW_NORMAL);
  imshow("image", img);
  waitKey(0);
  return 0;
}
