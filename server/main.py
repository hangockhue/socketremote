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


serverThread = None
stop = False
listener = None


def connectclient(conn):
    global stop

    while True:
        data = conn.recv(2048)

        data = data.decode("utf-8")

        if stop or data == '':
            break

        if data == "take_screenshot":
            photo_to_send = serverfunc.take_screen_shot()
            conn.sendall(photo_to_send)
        if data == "get_process":
            data_process = serverfunc.get_process_running()
            conn.sendall(bytes(str(data_process), "utf-8"))
        if "kill_process" in data:
            result = serverfunc.kill_process_running(int(data[13:]))
            conn.send(bytes(result, "utf-8"))
        if "open_process" in data:
            data = data.split("`")
            result = serverfunc.open_process(data[1])
            conn.send(bytes(result, "utf-8"))
        if "get_value" in data:
            data = data.split("`")
            result = serverfunc.get_value(data[1], data[2])
            conn.send(bytes(result, "utf-8"))
        if "set_value" in data:
            data = data.split("`")
            result = serverfunc.set_value(
                data[1],
                data[2],
                data[3],
                data[4],
            )
            conn.send(bytes(result, "utf-8"))
        if "send_file" in data:
            data = data.split("`")
            result = serverfunc.set_value_file(
                data[1],
                data[2],
                data[3],
                data[4],
            )
            conn.send(bytes(result, "utf-8"))
        if "delete_value" in data:
            data = data.split("`")
            result = serverfunc.delete_value(data[1], data[2])
            conn.send(bytes(result, "utf-8"))
        if "create_key" in data:
            data = data.split("`")
            result = serverfunc.create_key(data[1])
            conn.send(bytes(result, "utf-8"))
        if "delete_key" in data:
            data = data.split("`")
            result = serverfunc.delete_key(data[1])
            conn.send(bytes(result, "utf-8"))
        if data == "shutdown":
            serverfunc.shutdown_pc()
        if data == "key_log_listening":
            serverfunc.listening_keyboard(True)
        if data == "key_log_stop_listening":
            serverfunc.listening_keyboard(False)
        if data == "get_key_log":
            result = serverfunc.get_key_log()

            if result:
                conn.send(bytes(result, "utf-8"))
            else:
                conn.send(bytes("None", "utf-8"))
        if data == "get_application_running":
            data_application = serverfunc.get_application_running()
            conn.sendall(bytes(str(data_application), "utf-8"))

def runserver():
    TCP_IP = socket.gethostname()
    TCP_PORT = 8000
    BUFFER_SIZE = 20
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))

    tcpServer.listen(4)
    while True:
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        client, _ = tcpServer.accept()
        newthread = Process(target=connectclient, args=(client,))
        newthread.start()

class Server(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.tcpServer = None
        self.start = False

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

        if not self.start:
            global serverThread
            serverThread = Process(target=runserver)
            serverThread.start()
            
            self.start = True


def off():
    global serverThread
    global stop
    
    if serverThread:
        serverThread.terminate()

    serverfunc.listening_keyboard(False)
    stop = True

def main():
    app = QApplication(sys.argv)
    ex = Server()

    app.aboutToQuit.connect(off)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()