import cv2
import numpy as np

# 读取图像
image = cv2.imread('images/81d7cdef4a6b821cc8740a0e3c98ffa.jpg')
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


cv2.waitKey(0)
cv2.destroyAllWindows()
