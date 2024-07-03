import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
import os
from 图书识别 import ImageProcessor

class ImageSelector(QWidget):  # 创建一个继承自QWidget的类
    def __init__(self):
        super().__init__()

        self.image_path = None

        # 设置窗口标题和大小
        self.setWindowTitle("图片选择器")  # 设置窗口标题
        self.setGeometry(100, 100, 1200, 600)  # 设置窗口位置和大小

        # 创建布局
        self.main_layout = QVBoxLayout()  # 创建一个垂直布局
        self.image_layout = QHBoxLayout()  # 创建一个水平布局

        # 创建选择图片按钮并连接到函数
        self.select_button = QPushButton("请选择你要识别的图片", self)  # 创建选择图片按钮
        self.select_button.clicked.connect(self.select_image)  # 将按钮点击事件连接到select_image函数

        # 创建处理图片按钮并连接到函数
        self.process_button = QPushButton("识别图片", self)  # 创建处理图片按钮
        self.process_button.clicked.connect(self.process_image)  # 将按钮点击事件连接到process_image函数

        # 创建一个标签用于显示选择的图片
        self.original_image_label = QLabel(self)  # 创建一个标签用于显示原始图片
        self.original_image_label.setFixedSize(600, 400)

        # 创建一个标签用于显示处理后的图片
        self.processed_image_label = QLabel(self)  # 创建一个标签用于显示处理后的图片
        self.processed_image_label.setFixedSize(600, 400)

        # 将按钮和标签添加到布局
        self.main_layout.addWidget(self.select_button)  # 将选择按钮添加到主布局
        self.main_layout.addWidget(self.process_button)  # 将处理按钮添加到主布局
        self.image_layout.addWidget(self.original_image_label)  # 将原始图片标签添加到图像布局
        self.image_layout.addWidget(self.processed_image_label)  # 将处理后图片标签添加到图像布局
        self.main_layout.addLayout(self.image_layout)  # 将图像布局添加到主布局

        # 设置窗口布局
        self.setLayout(self.main_layout)  # 设置窗口的主布局

    def select_image(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()  # 创建文件对话框选项
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.jpg *.png *.jpeg)", options=options)  # 打开文件选择对话框
        if file_name:
            # 保存选择的图片路径
            self.image_path = os.path.relpath(file_name)  # 将选择的文件路径转换为相对路径
            # 显示选择的图片
            pixmap = QPixmap(file_name)  # 创建QPixmap对象
            self.original_image_label.setPixmap(pixmap.scaled(self.original_image_label.size(), aspectRatioMode=True))  # 显示选择的图片
            print(f"选择的图片路径：{self.image_path}")  # 打印选择的图片路径

    def process_image(self):
        if self.image_path:
            # 检查文件是否存在
            if not os.path.exists(self.image_path):  # 检查图像路径是否存在
                QMessageBox.critical(self, "错误", f"文件不存在: {self.image_path}")  # 如果文件不存在，显示错误消息
                return

            # 使用 ImageProcessor 类处理图像
            folder_path = os.path.dirname(self.image_path)  # 获取图像所在文件夹路径
            processor = ImageProcessor(folder_path)  # 创建图像处理器实例
            processed_images = processor.process_images()  # 处理图像

            # 查找并显示处理后的图像
            for file_name, original_image, processed_image in processed_images:  # 遍历处理后的图像列表
                if file_name in self.image_path:  # 如果文件名匹配
                    height, width, channel = original_image.shape  # 获取原始图像的高度、宽度和通道数
                    bytes_per_line = 3 * width  # 每行的字节数
                    q_original_image = QImage(original_image.data, width, height, bytes_per_line, QImage.Format_RGB888)  # 创建QImage对象
                    original_pixmap = QPixmap.fromImage(q_original_image)  # 创建QPixmap对象
                    self.original_image_label.setPixmap(original_pixmap.scaled(self.original_image_label.size(), aspectRatioMode=True))  # 显示原始图像

                    height, width = processed_image.shape  # 获取处理后图像的高度和宽度
                    bytes_per_line = width  # 每行的字节数
                    q_processed_image = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)  # 创建QImage对象
                    processed_pixmap = QPixmap.fromImage(q_processed_image)  # 创建QPixmap对象
                    self.processed_image_label.setPixmap(processed_pixmap.scaled(self.processed_image_label.size(), aspectRatioMode=True))  # 显示处理后图像

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序实例
    selector = ImageSelector()  # 创建ImageSelector窗口实例
    selector.show()  # 显示窗口
    sys.exit(app.exec_())  # 运行应用程序事件循环
