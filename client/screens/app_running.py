from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QInputDialog,
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

import ast
from .helper import recv_timeout


headers = [
    'Name Application',
    'ID Application',
    'count thread',
]


class AppRunning(QWidget):

    def __init__(self, socket):
        super().__init__()

        self.socket = socket

        self.initUI()


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

        kill_button = QPushButton('Kill')
        kill_button.clicked.connect(self.kill)
        select_button = QPushButton('Xem')
        select_button.clicked.connect(self.select)
        delete_button = QPushButton('Xóa')
        delete_button.clicked.connect(self.delete)
        start_button = QPushButton('Start')
        start_button.clicked.connect(self.start)

        hbox1.addWidget(kill_button)
        hbox1.addWidget(select_button)
        hbox1.addWidget(delete_button)
        hbox1.addWidget(start_button)

        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.table)

        self.setLayout(vbox1)
        self.setWindowTitle('List App')
        self.show()
    
    def kill(self):
        name, _ = QInputDialog.getText(self, '', 'Nhập ID:')
        
        if name:
            self.socket.send(bytes(f'kill_process_{name}', 'utf-8'))

            data = self.socket.recv(2048).decode("utf-8")
            
            msg = QMessageBox()
            msg.setWindowTitle("KILL")

            if data == '1':
                msg.setText("Kill thành công")
            else:
                msg.setText("Không tìm thấy chương trình")

            msg.exec()

    def start(self):
        name, _ = QInputDialog.getText(self, '', 'Nhập tên:')
        
        if name:
            self.socket.send(bytes(f'open_process`{name}', 'utf-8'))

            data = self.socket.recv(2048).decode("utf-8")

            msg = QMessageBox()
            msg.setWindowTitle("START")

            if data == '1':
                msg.setText("Mở thành công")
            else:
                msg.setText("Mở thất bại")

            msg.exec()

    def delete(self):
        self.table.clearContents()
        
    def select(self):
        
        self.table.clearContents()

        self.socket.send(bytes('get_application_running', 'utf-8'))

        result = recv_timeout(self.socket)

        result = ast.literal_eval(result)

        data = {}

        for value in result:
            key = list(value.keys())[0]
            if key in data:
                data[key]['pid'] = data[key]['pid'] + ',' + str(value[key])
                data[key]['count'] += 1
            else:
                data[key] = {}
                data[key]['pid'] = str(value[key])
                data[key]['count'] = 1

        self.table.setRowCount(len(data.keys()))

        for index, key in enumerate(data.keys()):
            column = 0

            record = [key, data[key]['pid'], data[key]['count']]
            for value in record:
                item = QTableWidgetItem()
                item.setText(str(value))
                self.table.setItem(index, column, item)
                column += 1