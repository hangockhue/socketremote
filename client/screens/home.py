import sys
import socket
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)
import ctypes

from .screenshot import Screenshot
from .process import Process
from .app_running import AppRunning
from .keystroke import Keystroke
from .registry import Registry
from .video_streaming import streaming_video
from .mac_address import show_mac_address
from .treeview import TreeViewScreen


class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connected = False


    def initUI(self):

        user32 = ctypes.windll.user32

        desktop_width = user32.GetSystemMetrics(0)
        desktop_height = user32.GetSystemMetrics(1)

        width = int(desktop_width * 0.187)
        height = int(desktop_height * 0.167)

        self.setFixedWidth(width)
        self.setFixedHeight(height)

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
        shutdown_button = QPushButton('Tắt máy')
        shutdown_button.clicked.connect(self.shutdown)
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.logout)
        screenshot_button = QPushButton('Chụp màn hình')
        screenshot_button.clicked.connect(self.open_screenshot)
        keystroke_button = QPushButton('Keystroke')
        keystroke_button.clicked.connect(self.open_keystroke)
        edit_registry = QPushButton('Sửa Registry')
        edit_registry.clicked.connect(self.open_registry)
        video_streaming_button = QPushButton('Xem live màn hình')
        video_streaming_button.clicked.connect(self.streaming)
        mac_getting_button = QPushButton('Xem địa chỉ Mac')
        mac_getting_button.clicked.connect(self.get_mac_address)
        folder_tree_button = QPushButton('Xem Folder')
        folder_tree_button.clicked.connect(self.show_folder_tree)

        self.block_keyboard_button = QPushButton('Khoá bàn phím')
        self.block_keyboard_button.clicked.connect(self.block_keyboard)
        self.is_blocked_keyboard = False

        exit_button = QPushButton('Thoát')
        exit_button.clicked.connect(self.exit)

        items = [
            process_running_button,
            app_running_button,
            shutdown_button,
            logout_button,
            screenshot_button,
            keystroke_button,
            edit_registry,
            video_streaming_button,
            mac_getting_button,
            folder_tree_button,
            self.block_keyboard_button,
            exit_button,
        ]

        positions = [(i, j) for i in range(6) for j in range(2)]

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
            self.socket.connect((self.ip_line_edit.text(), 8000))
            self.socket.settimeout(3)
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Kết nối thành công")
            msg.exec()
            self.ip_line_edit.setReadOnly(True)
            self.connected = True
            
        except TimeoutError:
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Kết nối thất bại")
            msg.exec()

    def check_connnected(self):
        if not self.connected:
            msg = QMessageBox()
            msg.setWindowTitle("IP")
            msg.setText("Chưa kết nối")
            msg.exec()
            return False
        return True

    def shutdown(self):
        if self.check_connnected():
            self.socket.send(bytes('shutdown', 'utf-8'))

    def logout(self):
        if self.check_connnected():
            self.socket.send(bytes('logout', 'utf-8'))

    def open_process_running(self):
        if self.check_connnected():
            self.small = Process(self.socket)

    def open_app_running(self):
        if self.check_connnected():
            self.small = AppRunning(self.socket)

    def open_keystroke(self):
        if self.check_connnected():
            self.small = Keystroke(self.socket)

    def open_registry(self):
        if self.check_connnected():
            self.small = Registry(self.socket)

    def open_screenshot(self):
        if self.check_connnected():
            self.small = Screenshot(self.socket)

    def streaming(self):
        if self.check_connnected():
            streaming_video(self.socket)

    def get_mac_address(self):
        if self.check_connnected():
            show_mac_address(self.socket)

    def show_folder_tree(self):
        if self.check_connnected():
            self.small = TreeViewScreen(self.socket, self.ip_line_edit.text())

    def block_keyboard(self):
        if self.check_connnected():
            if self.is_blocked_keyboard:
                self.socket.send(bytes('unblock_keyboard', 'utf-8'))
                self.block_keyboard_button.setText('Khoá bàn phím')
            else:
                self.socket.send(bytes('block_keyboard', 'utf-8'))
                self.block_keyboard_button.setText('Mở khoá bàn phím')

            self.is_blocked_keyboard = not self.is_blocked_keyboard

    def exit(self):
        sys.exit()