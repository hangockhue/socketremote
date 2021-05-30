from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
)


class Keystroke(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        desktop_rect = QApplication.desktop().screen().rect()

        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        width = int(desktop_width * 0.187)
        height = int(desktop_height * 0.127)

        self.setGeometry(
            int(desktop_width / 2 - width / 2),
            int(desktop_height / 2 - height / 2),
            width,
            height
        )

        vbox1 = QVBoxLayout()

        hbox1 = QHBoxLayout()

        hook_button = QPushButton('Hook')
        unhook_button = QPushButton('Unhook')
        print_button = QPushButton('In Phím')
        delete_button = QPushButton('Xóa')

        hbox1.addWidget(hook_button)
        hbox1.addWidget(unhook_button)
        hbox1.addWidget(print_button)
        hbox1.addWidget(delete_button)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.textEdit)

        self.setLayout(vbox1)
        self.setWindowTitle('Keystroke')
        self.show()
