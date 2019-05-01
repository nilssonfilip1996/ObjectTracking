# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 14:26:28 2019

@author: nilss
"""
import numpy as np
import cv2
import sys
# You should replace these 3 lines with the output in calibration step
#DIM=XXX
#K=np.array(YYY)
#D=np.array(ZZZ)
DIM=(1920, 1080)
K=np.array([[1075.207197320511, 0.0, 968.3921124809665], [0.0, 1067.4445501585058, 602.7138416764186], [0.0, 0.0, 1.0]])
D=np.array([[0.3098634728377196], [0.43437112283829443], [-1.3172273960310377], [1.6533357151911663]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    #undistorted_img = cv2.resize(undistorted_img, (605,360))
    cv2.imshow("undistorted", undistorted_img)
    cv2.imwrite("test.jpg", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)