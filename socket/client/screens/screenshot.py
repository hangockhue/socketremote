import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
)


class Screenshot(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


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
        # self.image_label.setPixmap(None) Hàm đổi ảnh

        hbox1 = QHBoxLayout()

        take_picture_button = QPushButton('Chụp')
        save_button = QPushButton('Lưu')
        save_button.clicked.connect(self.save)

        hbox1.addWidget(take_picture_button)
        hbox1.addWidget(save_button)

        vbox1.addWidget(self.image_label)
        vbox1.addLayout(hbox1)

        self.setLayout(vbox1)
        self.show()

    def save(self):
        path = QFileDialog.getSaveFileName(
            self,
            'Open a file',
            '',
            '*'
        )

        print(path)
