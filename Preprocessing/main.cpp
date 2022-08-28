#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>

#include <chrono>
using namespace std::chrono;

using namespace cv;

struct BGR {
    uchar blue;
    uchar green;
    uchar red;
};

int main() {
    auto start = high_resolution_clock::now();
    std::string image_path = "/Users/b_arsick/Documents/Melanoma-Detector/Preprocessing/example.jpg";
    Mat img = imread(image_path, IMREAD_COLOR);

    //imshow("Original", img);

    for(int y = 0; y < img.rows; y++) {
        for (int x = 0; x < img.cols; x++) {
            BGR& bgr = img.ptr<BGR>(y)[x];
            bgr.blue = 255 - bgr.blue;
            bgr.green = 255 - bgr.green;
            bgr.red = 255 - bgr.red;
        }
    }
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    std::cout << duration.count() * 0.000001 << '\n';
    //imshow("Result", img);

    waitKey(0);
    return 0;
}