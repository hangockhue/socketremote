import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
)
import socket
from PyQt5.QtWidgets import QApplication
from multiprocessing import Process
import serverfunc
import numpy as np

all_processes = []


def connectclient(tcpServer):
    while True:
        (conn, (ip, port)) = tcpServer.accept()

        data = conn.recv(2048)
        print(data)
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


def runserver():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 1234
    BUFFER_SIZE = 20
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))
    threads = []

    tcpServer.listen(4)
    while True:
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        global conn
        (conn, (ip, port)) = tcpServer.accept()
        newthread = Process(target=connectclient, args=(tcpServer,))
        newthread.start()
        threads.append(newthread)

        global all_processes
        all_processes.append(newthread)

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

        serverThread = Process(target=runserver)
        serverThread.start()

        global all_processes
        all_processes.append(serverThread)



def off():
    global all_processes

    print(all_processes)
    
    for p in all_processes:
        p.terminate()

def main():
    app = QApplication(sys.argv)
    ex = Server()

    app.aboutToQuit.connect(off)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()