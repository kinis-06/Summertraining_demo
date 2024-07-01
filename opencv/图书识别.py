import cv2
import numpy as np
import os

# 设置图像文件夹路径
folder_path = 'images/'

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 遍历文件夹中的所有文件
for file_name in file_names:
    # 读取图像
    image_path = os.path.join(folder_path, file_name)
    image = cv2.imread(image_path)

    # 检查图像是否成功读取
    if image is None:
        print(f"Failed to load image: {image_path}")
        continue

    cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('image', image)

    # 转换为 HSV 色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.namedWindow('hsv', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('hsv', hsv)

    # 定义绿色的范围
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # 创建掩码
    mask = cv2.inRange(hsv, lower_green, upper_green)
    cv2.namedWindow('mask', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('mask', mask)

    # 将绿色部分保留，其他部分变为黑色
    img = cv2.bitwise_and(image, image, mask=mask)
    cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('img', img)

    # 等待按键按下
    cv2.waitKey(0)
    cv2.destroyAllWindows()

