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
)

headers = [
    'name process',
    'ID process',
    'count process',
]


class Process(QWidget):

    def __init__(self):
        super().__init__()

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
        self.setWindowTitle('Process')
        self.show()
    
    def kill(self):
        name, done = QInputDialog.getText(self, '', 'Nhập ID:')
        print(name)

    def start(self):
        name, done = QInputDialog.getText(self, '', 'Nhập tên:')
        print(name)

    def delete(self):
        self.table.clearContents()

    def select(self):
        self.table.clearContents()

        data = [
            [1,2,3],
            [4,5,6]
        ]
        self.table.setRowCount(len(data))

        column = 0
        for index, record in enumerate(data):
            for value in record:
                item = QTableWidgetItem()
                item.setText(str(value))
                self.table.setItem(index, column, item)
                column += 1