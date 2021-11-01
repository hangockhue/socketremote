from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QStyle,
    QMenu,
    QFileDialog,
    QMessageBox,
)
from PyQt6 import QtCore, QtNetwork
from PyQt6.QtGui import QAction
import struct
import pickle
import json


FOLDER = 0
FILE = 1


def get_direction(item: QTreeWidgetItem):
    parent = item.parent()
    if parent == None:
        return item.text(0) + '/'
    return get_direction(parent) + item.text(0) + '/'

class TreeViewScreen(QWidget):
    def __init__(self, socket, host):
        super().__init__()
        self.url = f'http://{host}:8080'

        self.initUI()
        self.socket = socket
    
    def initUI(self):
        layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel("Folder Tree")

        req = QtNetwork.QNetworkRequest(QtCore.QUrl(self.url))
        print(self.url)

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponseVolumnes)
        self.nam.get(req)

        self.tree.itemDoubleClicked.connect(self.onItemClicked)
        self.tree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)  
        self.tree.customContextMenuRequested.connect(self.openMenu)  

        layout.addWidget(self.tree)
        self.setLayout(layout)

        self.show()

        self.menu = QMenu()
        self.copy_action = QAction('Copy')
        self.copy_action.triggered.connect(self.copy_file)
        self.delete_action = QAction('Delete')
        self.delete_action.triggered.connect(self.delete_file)
        self.menu.addAction(self.copy_action)
        self.menu.addAction(self.delete_action)

        pixmapi = QStyle.StandardPixmap.SP_DirIcon
        self.dir_icon = self.style().standardIcon(pixmapi)

        pixmapi = QStyle.StandardPixmap.SP_FileIcon
        self.file_icon = self.style().standardIcon(pixmapi)

    def handleResponseVolumnes(self, reply):
        er = reply.error()

        if er == QtNetwork.QNetworkReply.NetworkError.NoError:
            bytes_string = reply.readAll()
            volumes = json.loads(str(bytes_string, 'utf-8'))['volumes']
            print(bytes_string)

            pixmapi = QStyle.StandardPixmap.SP_DriveDVDIcon
            icon = self.style().standardIcon(pixmapi)

            for i in volumes:
                a = QTreeWidgetItem(self.tree)
                a.setText(0, i)
                a.setIcon(0, icon)
        else:
            print("Error occured: ", er)
            print(reply.errorString())

    def onItemClicked(self, item, _):
        self.clickedItem = item
        direction = get_direction(item)

        req = QtNetwork.QNetworkRequest(QtCore.QUrl(self.url + '/' + direction))
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponseDirection)
        self.nam.get(req)

    def handleResponseDirection(self, reply):
        er = reply.error()

        if er == QtNetwork.QNetworkReply.NetworkError.NoError:
            # Remove all old data
            for i in reversed(range(self.clickedItem.childCount())):
                self.clickedItem.removeChild(self.clickedItem.child(i))

            bytes_string = reply.readAll()
            result = json.loads(str(bytes_string, 'utf-8'))

            for i in result['folders']:
                a = QTreeWidgetItem(self.clickedItem, type=FOLDER)
                a.setText(0, i)
                a.setIcon(0, self.dir_icon)

            for i in result['files']:
                a = QTreeWidgetItem(self.clickedItem, type=FILE)
                a.setText(0, i)
                a.setIcon(0, self.file_icon)

            self.clickedItem.setExpanded(True)
        else:
            print("Error occured: ", er)
            print(reply.errorString())

    def openMenu(self, point):
        index = self.tree.indexAt(point)

        if not index.isValid():
            return

        self.chose_file = self.tree.itemAt(point)

        if self.chose_file.type() == FILE:
            self.menu.exec(self.tree.mapToGlobal(point))

    def copy_file(self):
        direction = get_direction(self.chose_file)[:-1]

        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save a file',
            self.chose_file.text(0),
            '*'
        )

        self.socket.send(bytes(f"copy_file`{direction}", 'utf-8'))

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
        data = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        with open(path, "wb") as f:
            f.write(data)

        msg = QMessageBox()
        msg.setWindowTitle("IP")
        msg.setText("Copy thành công")
        msg.exec()
            

    def delete_file(self):
        direction = get_direction(self.chose_file)[:-1]
        self.socket.send(bytes(f"delete_file`{direction}", 'utf-8'))
        data = self.socket.recv(2048).decode("utf-8")
        
        if data == '1':
            self.chose_file.parent().removeChild(self.chose_file)
