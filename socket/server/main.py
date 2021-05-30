import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
)
import socket
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtNetwork import QHostAddress, QTcpServer
from threading import Thread
import serverfunc
import numpy as np



class Server(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.tcpServer = None

    def initUI(self):

        desktop_rect = QApplication.desktop().screen().rect()

        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        width = int(desktop_width * 0.156)
        height = int(desktop_height * 0.167)

        self.setGeometry(
            int(desktop_width / 2 - width / 2),
            int(desktop_height / 2 - height / 2),
            width,
            height
        )

        self.setWindowTitle('Server')

        layout = QVBoxLayout()

        open_button = QPushButton("Mở Server")
        open_button.clicked.connect(self.open_server)

        layout.addStretch()
        layout.addWidget(open_button)
        layout.addStretch()

        self.setLayout(layout)

        self.show()

    def open_server(self):
        print("start server")
        serverThread = ServerThread(self)
        serverThread.start()


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        TCP_IP = '192.168.0.107'
        TCP_PORT = 1234
        BUFFER_SIZE = 20
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind((TCP_IP, TCP_PORT))
        threads = []

        self.tcpServer.listen(4)
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            global conn
            (conn, (ip, port)) = self.tcpServer.accept()
            newthread = ClientThread(ip, port, self.tcpServer)
            newthread.start()
            threads.append(newthread)



class ClientThread(Thread):

    def __init__(self, ip, port, tcpServer) :
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.tcpServer = tcpServer
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            # (conn, (self.ip,self.port)) = serverThread.tcpServer.accept()
            global conn
            data = conn.recv(2048)
            # print(data)
            if data == b"take_screenshot":
                image_data =  serverfunc.take_screen_shot()
                print(image_data.shape)
                conn.send(bytes(np.array_str(image_data), "utf-8"))
            if data == b"get_process":
                data_process = serverfunc.get_process_running()
                print(data_process)
                conn.send(bytes(str(data_process), "utf-8"))
            if data.find(b"kill_process") == 0:

                serverfunc.kill_process_running(int(data[13:]))



def main():
    app = QApplication(sys.argv)
    ex = Server()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()