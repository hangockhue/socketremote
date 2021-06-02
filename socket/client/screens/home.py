import sys
import socket
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)

from .screenshot import Screenshot
from .process import Process
from .app_running import AppRunning
from .keystroke import Keystroke
from .registry import Registry


class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def initUI(self):

        desktop_rect = QApplication.desktop().screen().rect()

        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        width = int(desktop_width * 0.187)
        height = int(desktop_height * 0.167)

        self.setGeometry(
            int(desktop_width / 2 - width / 2),
            int(desktop_height / 2 - height / 2),
            width,
            height
        )

        vbox1 = QVBoxLayout()

        hbox1 = QHBoxLayout()

        self.ip_line_edit = QLineEdit()
        connect_button = QPushButton('Kết Nối')
        connect_button.clicked.connect(self.connect)

        hbox1.addWidget(self.ip_line_edit)
        hbox1.addWidget(connect_button)

        vbox1.addLayout(hbox1)

        process_running_button = QPushButton('Process Running')
        process_running_button.clicked.connect(self.open_process_running)
        app_running_button = QPushButton('App Running')
        app_running_button.clicked.connect(self.open_app_running)
        shut_down_button = QPushButton('Tắt máy')
        shut_down_button.clicked.connect(self.shutdown)
        screenshot_button = QPushButton('Chụp màn hình')
        screenshot_button.clicked.connect(self.open_screenshot)
        keystroke_button = QPushButton('Keystroke')
        keystroke_button.clicked.connect(self.open_keystroke)
        edit_registry = QPushButton('Sửa Registry')
        edit_registry.clicked.connect(self.open_registry)
        exit_button = QPushButton('Thoát')
        exit_button.clicked.connect(self.exit)

        items = [
            process_running_button,
            app_running_button,
            shut_down_button,
            screenshot_button,
            keystroke_button,
            edit_registry,
            '',
            exit_button,
        ]

        positions = [(i, j) for i in range(5) for j in range(2)]

        grid = QGridLayout()
        for position, item in zip(positions, items):
            if isinstance(item, QPushButton):
                grid.addWidget(item, *position)

        vbox1.addLayout(grid)

        self.setLayout(vbox1)
        self.setWindowTitle('Client')
        self.show()

    def connect(self):
        
        try:
            self.socket.connect((self.ip_line_edit.text(), 1234))
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Kết nối thành công")
            msg.exec()
        except TimeoutError:
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Kết nối thất bại")
            msg.exec()

    def shutdown(self):
        self.socket.send(bytes('shutdown', 'utf-8'))

    def open_process_running(self):
        self.small = Process(self.socket)

    def open_app_running(self):
        self.small = AppRunning()

    def open_keystroke(self):
        self.small = Keystroke(self.socket)

    def open_registry(self):
        self.small = Registry(self.socket)

    def open_screenshot(self):
        self.small = Screenshot(self.socket)

    def exit(self):
        sys.exit()