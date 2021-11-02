from PyQt6.QtWidgets import (
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
import ctypes
from .helper import recv_timeout

headers = [
    'name process',
    'ID process',
    'count process',
]


class Process(QWidget):

    def __init__(self, socket):
        super().__init__()

        self.socket = socket

        self.initUI()


    def initUI(self):

        user32 = ctypes.windll.user32

        desktop_width = user32.GetSystemMetrics(0)
        desktop_height = user32.GetSystemMetrics(1)

        width = int(desktop_width * 0.187)
        height = int(desktop_height * 0.167)

        self.resize(width, height)

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
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.table)

        self.setLayout(vbox1)
        self.setWindowTitle('Process')
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
                msg.setText("Không tìm thấy process")

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
        
        self.socket.send(bytes('get_process', 'utf-8'))

        result = recv_timeout(self.socket)

        result = ast.literal_eval(result)

        data = {}

        for i in result:
            if i['name'] in data:
                data[i['name']]['pid'] = data[i['name']]['pid'] + ',' + str(i['pid'])
                data[i['name']]['count'] += 1
            else:
                data[i['name']] = {}
                data[i['name']]['pid'] = str(i['pid'])
                data[i['name']]['count'] = 1

        self.table.setRowCount(len(data.keys()))

        for index, key in enumerate(data.keys()):
            column = 0

            record = [key, data[key]['pid'], data[key]['count']]
            for value in record:
                item = QTableWidgetItem()
                item.setText(str(value))
                self.table.setItem(index, column, item)
                column += 1