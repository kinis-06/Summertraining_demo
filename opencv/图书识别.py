import cv2
import numpy as np
import os

class ImageProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_names = os.listdir(folder_path)

    def process_images(self):
        processed_images = []
        for file_name in self.file_names:
            image_path = os.path.join(self.folder_path, file_name)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            # 转换为HSV图像
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # 设置绿色的范围
            lower_green = np.array([35, 100, 100])
            upper_green = np.array([85, 255, 255])

            # 创建掩膜
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # 查找绿色区域的轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # 计算最小外接矩形
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.array(box, dtype=np.int32)

                # 绘制最小外接矩形区域
                cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

                # 裁剪矩形区域并显示
                x, y, w, h = cv2.boundingRect(contour)
                cropped_image = image[y:y+h, x:x+w]

                # 使用另一个类进行处理
                processor = CroppedImageProcessor()
                processed_image = processor.process(cropped_image)
                processed_images.append((file_name, image, processed_image))

        return processed_images

class CroppedImageProcessor:
    def process(self, image):
        # 灰度化
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 二值化
        thresh_value = 50
        _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)

        # 腐蚀操作
        kernel = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(binary, kernel, iterations=1)

        return eroded
