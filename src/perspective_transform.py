# -*- coding: utf-8 -*-
# @Time    : 2019/10/11
# @Author  : WangMengfan
# @File    : perspective_transform.py
# @Software: PyCharm
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../pic/1.jpg')
rows, cols,_ = img.shape
# the four corners of the original image
points1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
# the target image four corners: left-up, right-up, left-botom, right-bottom
points2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
# generate the perspective transformation matrix
matrix = cv2.getPerspectiveTransform(points1,points2)
print(matrix)
# perspective transformation, the third param is target image size
dst = cv2.warpPerspective(img, matrix, (cols, rows))
plt.subplot(121), plt.imshow(img[:, :, ::-1]), plt.title('input')
plt.subplot(122), plt.imshow(dst[:, :, ::-1]), plt.title('output')
plt.show()