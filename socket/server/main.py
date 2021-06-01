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
import pickle
from pynput.keyboard import Listener, Key

all_processes = []





def connectclient(tcpServer):
    while True:
        (conn, (ip, port)) = tcpServer.accept()

        data = conn.recv(2048)

        data = data.decode("utf-8")

        if data == "take_screenshot":
            image_data = serverfunc.take_screen_shot()
            serialized_data = pickle.dumps(image_data, protocol=2)
            conn.sendall(serialized_data)
        if data == "get_process":
            data_process = serverfunc.get_process_running()
            conn.sendall(bytes(str(data_process), "utf-8"))
        if "kill_process" in data:
            serverfunc.kill_process_running(int(data[13:]))
        if "get_value" in data:
            data = data.split("`")
            result = serverfunc.get_value(data[1], data[2])
            conn.send(bytes(result, "utf-8"))
        if data == "shutdown":
            serverfunc.shutdown_pc()
        if data == "key_log_listening":
            serverfunc.listening_keyboard(True)
            pass
        if data == "key_log_stop_listening":
            serverfunc.listening_keyboard(False)
            pass


def on_press(key):
    print('{0} pressed'.format(
        key))
    conn.sendall(key)
# Collect events until released


def listening_keyboard(listening=True):
    if listening:
        with Listener(
                on_press=on_press) as listener:
            listener.join()
        print(listener)
    else:
        return False


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