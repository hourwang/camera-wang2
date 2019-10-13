Homework1
• 1. 用自己的手机采集棋盘板定标数据；
• 2. 实现或调用角点检测、局部特征提取、局部特征匹配算法，标
定自己手机的内参；
• 3. 改变外参，生成不同视角的新图像。

 1. 自定义函数
 ## pic文件夹中存放着29张棋盘图像
 ## 运行main.py即可输出得到自己手机的内参、外参等参数信息
 ##  标定步骤主要分为求单应矩阵，求相机内参，求每幅图相应的外参，求畸变矫正系数，微调所有参数等五个步骤，
     每个步骤对应一个py文件，放置于src\step文件夹下。
     其中，step中包含的文件主要有自定义函数distortion.py、extrinsics.py、homography.py、
      intrinsics.py以及refine_all.py
 ## 运行perspective_transform.py即可生成并显示不同视角的新图像。
 2. 其中，chessTest.py是调用函数实现的，运行即可得到一系列手机参数，以及改变参数后，生成的新视角
    生成的新视角图片存在outputphoto文件夹中