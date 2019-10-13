# -*- coding: utf-8 -*-
# @Time    : 2019/10/11
# @Author  : WangMengfan
# @File    : chessTest.py
# @Software: PyCharm
import cv2
import numpy as np
import glob
'''
1. Calibrated internal reference
2. Change parameters to generate new images
3. Compute total error
'''
'''
1. Calibrated internal reference
'''
i = 1  # for output images's name
cross_corners = [12, 8]  # the size of chessboard
total_error = 0
# The stopping criterion adopted is the maximum number of cycles 30 and the maximum error tolerance 0.001.
criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

# Obtaining the position of corners of calibration plate
objp = np.zeros((cross_corners[0] * cross_corners[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:12, 0:8].T.reshape(-1, 2)

obj_points = []  # 3D
img_points = []  # 2D
images = glob.glob("../pic/*.jpg")  # the Location of data sets
# img_root='C:/Users/Dell/Pictures/Test/chess/'
# img_names=os.listdir(img_root)
# img_paths=[os.path.join(img_root,f) for f in img_names]
# print('images len:{}'.format(len(images)))

for image in images:
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # change to gray
    size = gray.shape[::-1]
    gray = gray.astype(np.uint8)

    # Find corners, store them in corners, RET is flag that finds corners.
    ret, corners = cv2.findChessboardCorners(gray, (cross_corners[0], cross_corners[1]), None)
    # print(test)
    # print(corners)

    if ret:
        obj_points.append(objp)
        # Perform sub-pixel corner detection,
        # criteria: Termination condition of corner precision iteration process
        corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
        # Finding sub-pixel corner based on original corner
        # print(corners2)

        if [corners2]:
            img_points.append(corners2)
        else:
            img_points.append(corners)

        cv2.drawChessboardCorners(img, (cross_corners[0], cross_corners[1]), corners, ret)
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('img', 300, 300)
        cv2.imshow('img', img)
        cv2.waitKey(1)

print("data size:", len(img_points))  # data set
cv2.destroyAllWindows()

# 标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)

# Reprojection error
print("ret:", ret)
# Internal parameter matrix
print("mtx:", mtx)
# Distortion coefficient   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
print("dist:", dist)
# Rotation Vector # External Parameters
print("rvecs:", rvecs)
# Translational Vector  # External Parameters
print("tvecs:", tvecs)
print("-----------------------------------------------------")
'''
2. Change parameters to generate new images
'''
'''
 start to do distortion
'''
for change in images:
    changeimg = cv2.imread(change)
    h, w = changeimg.shape[:2]
    # Free proportional parameter
    newCameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (cross_corners[0], cross_corners[1]), 1, (w, h))
    dst = cv2.undistort(changeimg, mtx, dist, None, newCameramtx)
    # cv2.imwrite('D:/code/python/camera/changeparamphoto/'+str(i)+".jpg", dst)
    cv2.imwrite('../outputphoto/' + str(i) + ".jpg", dst)
    i = i+1
    print("newCameramtx:\n", newCameramtx)
    print("dist:\n", dist)
'''
3. Compute total error
'''
'''
Backprojection error
'''
for i in range(len(obj_points)):
    imgpoints2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    total_error += error
print("total error: ", total_error/len(obj_points))



