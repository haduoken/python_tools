import sys
import random, cv2
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QLabel, QPushButton
from PySide2.QtGui import QImage, QPixmap


class CheckWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.total_layout = QtWidgets.QVBoxLayout()
        self.total_layout.addWidget(QLabel('hello world'))
        self.setLayout(self.total_layout)
        self.is_open = True


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        self.cap = cv2.VideoCapture(0)
        
        self.label = QLabel("")
        
        self.checkWindow = CheckWindow()
        
        # 1 logo 和 按钮 按钮操作区设计 Layout
        self.row1_layout = QtWidgets.QHBoxLayout()
        self.label_logo = QLabel("")
        self.label_logo.setPixmap('logo.png')
        self.btn_history_data = QPushButton('历史信息')
        self.btn_history_data.clicked.connect(self.on_btn_history)
        self.row1_layout.addWidget(self.label_logo)
        self.row1_layout.addWidget(self.btn_history_data)
        
        # 2 检测结果显示和可见光画面
        self.row2_layout = QtWidgets.QHBoxLayout()
        # 2.1 设置为当前检测到的数据
        self.row2_1_layout = QtWidgets.QVBoxLayout()
        self.labels_detect = []
        for i in range(5):
            label = QLabel("")
            label.setPixmap('1.png')
            self.row2_1_layout.addWidget(label)
            self.labels_detect.append(label)
        self.row2_layout.addLayout(self.row2_1_layout)
        # 2.2 可见光画面
        self.row2_layout.addWidget(self.label)
        
        # 总体布局设计 Layout
        self.total_layout = QtWidgets.QVBoxLayout()
        self.total_layout.addLayout(self.row1_layout)
        self.total_layout.addLayout(self.row2_layout)
        
        # 将布局添加到window
        self.setLayout(self.total_layout)
        self.show()
       .timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.refresh_image)  # 计时结束调用operate()方法
        self.timer.start(100)  # 设置计时间隔并启动
    
    def refresh_image(self):
        ok, image = self.cap.read()
        if ok:
            pic = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(pic)
            self.label.setPixmap(pix)
    
    def on_btn_history(self):
        if self.checkWindow.isVisible():
            self.checkWindow.setVisible(False)
        else:
            self.checkWindow.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    widget = MainWindow()
    sys.exit(app.exec_())
