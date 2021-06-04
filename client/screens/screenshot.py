from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt5 import QtGui
from PIL import Image
from PIL.ImageQt import ImageQt
from .helper import recv_timeout


class Screenshot(QWidget):

    def __init__(self, socket):
        super().__init__()

        self.initUI()
        self.socket = socket


    def initUI(self):

        desktop_rect = QApplication.desktop().screen().rect()

        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        width = int(desktop_width * 0.563)
        height = int(desktop_height * 0.5)

        self.setGeometry(
            int(desktop_width / 2 - width / 2),
            int(desktop_height / 2 - height / 2),
            width,
            height
        )


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

        size = int(self.socket.recv(10).decode('utf-8'))

        print(size)

        self.socket.send(bytes('get_image', 'utf-8'))

        the_photo = self.socket.recv(size)

        self.socket.send(bytes('get_screenshot_size', 'utf-8'))

        size = self.socket.recv(2048).decode('utf-8')

        # size = size.split(' ')


        # width = int(size[0])
        # height = int(size[1])

        try:
            image = Image.frombytes("RGB", (1920, 1080), the_photo)
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Ảnh quá lớn, hãy thử lại")
            msg.exec()
            return

        self.image = image

        qimage = ImageQt(self.image)

        gui_image = QtGui.QImage(qimage)

        pixmap = QtGui.QPixmap.fromImage(gui_image)

        pixmap.detach()

        self.image_label.setPixmap(pixmap)
        
        self.image_label.resize(pixmap.width(), pixmap.height())


    def save(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Open a file',
            '',
            '(*.PNG)'
        )

        if path:
            path = path.split(".")[0]
            self.image.save(f"{path}.png")
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Lưu thành công")
            msg.exec()

