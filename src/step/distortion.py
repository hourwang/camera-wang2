# -*- coding: utf-8 -*-
# @Time    : 2019/10/11
# @Author  : WangMengfan
# @File    : distortion.py
# @Software: PyCharm
import numpy as np

# 返回畸变矫正系数k0,k1


def get_distortion(intrinsic_param, extrinsic_param, pic_coor, real_coor):
    D = []
    d = []
    for i in range(len(pic_coor)):
        for j in range(len(pic_coor[i])):
            # 转换为齐次坐标
            single_coor = np.array([(real_coor[i])[j, 0], (real_coor[i])[j, 1], 0, 1])

            # 利用现有内参及外参求出估计图像坐标
            u = np.dot(np.dot(intrinsic_param, extrinsic_param[i]), single_coor)
            [u_estim, v_estim] = [u[0]/u[2], u[1]/u[2]]

            coor_norm = np.dot(extrinsic_param[i], single_coor)
            coor_norm /= coor_norm[-1]

            # r = np.linalg.norm((real_coor[i])[j])
            r = np.linalg.norm(coor_norm)
            D.append(np.array([(u_estim - intrinsic_param[0, 2]) * r ** 2,
                               (u_estim - intrinsic_param[0, 2]) * r ** 4]))
            D.append(np.array([(v_estim - intrinsic_param[1, 2]) * r ** 2,
                               (v_estim - intrinsic_param[1, 2]) * r ** 4]))

            # 求出估计坐标与真实坐标的残差
            d.append(pic_coor[i][j, 0] - u_estim)
            d.append(pic_coor[i][j, 1] - v_estim)

    D = np.array(D)
    temp = np.dot(np.linalg.inv(np.dot(D.T, D)), D.T)
    k = np.dot(temp, d)

    return k