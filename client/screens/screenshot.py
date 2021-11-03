from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6 import QtGui
import struct
import pickle
import cv2
import ctypes


class Screenshot(QWidget):

    def __init__(self, socket):
        super().__init__()

        self.initUI()
        self.socket = socket


    def initUI(self):

        user32 = ctypes.windll.user32

        desktop_width = user32.GetSystemMetrics(0)
        desktop_height = user32.GetSystemMetrics(1)

        width = int(desktop_width / 3)
        height = int(desktop_height / 5)

        self.resize(width, height)

        vbox1 = QVBoxLayout()
        self.image_label = QLabel()

        hbox1 = QHBoxLayout()

        take_picture_button = QPushButton('Chụp')
        take_picture_button.clicked.connect(self.take_picture)
        save_button = QPushButton('Lưu')
        save_button.clicked.connect(self.save)

        hbox1.addWidget(take_picture_button)
        hbox1.addWidget(save_button)

        vbox1.addWidget(self.image_label)
        vbox1.addLayout(hbox1)

        self.setLayout(vbox1)
        self.show()

    def take_picture(self):
        self.socket.send(bytes('take_screenshot', 'utf-8'))

        data = b""
        payload_size = struct.calcsize("Q")

        while len(data) < payload_size:
            packet = self.socket.recv(4*1024)
            if not packet: break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]

        while len(data) < msg_size:
            data += self.socket.recv(4*1024)

        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        height, width, _ = frame.shape

        image = QtGui.QImage(frame, width, height, width * 3, QtGui.QImage.Format.Format_BGR888)

        self.pixmap = QtGui.QPixmap(image)

        self.pixmap.detach()

        self.image_label.setPixmap(self.pixmap)

        self.image_label.resize(self.pixmap.width(), self.pixmap.height())


    def save(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Open a file',
            '',
            '(*.PNG)'
        )

        if path:
            path = path.split(".")[0]
            self.pixmap.save(f"{path}.png")
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Lưu thành công")
            msg.exec()

