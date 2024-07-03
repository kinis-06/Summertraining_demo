import cv2
import numpy as np
import os

class ImageProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_names = os.listdir(folder_path)

    def process_images(self):
        for file_name in self.file_names:
            image_path = os.path.join(self.folder_path, file_name)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            self.display_image(image, 'image')

            # 转换为HSV图像
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            self.display_image(hsv, 'hsv')

            # 设置绿色的范围
            lower_green = np.array([35, 100, 100])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            self.display_image(mask, 'mask')

            # 使用掩膜提取绿色区域
            img = cv2.bitwise_and(image, image, mask=mask)
            self.display_image(img, 'img')

            # 查找绿色区域的轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cropped_image = image[y:y+h, x:x+w]
            self.display_image(cropped_image, f'{x}')

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def display_image(self, image, window_name):
        cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
        cv2.imshow(window_name, image)

if __name__ == "__main__":
    folder_path = 'images/'
    processor = ImageProcessor(folder_path)
    processor.process_images()
