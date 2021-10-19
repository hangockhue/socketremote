import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
import socket
from multiprocessing import Process, Value

import serverfunc
import ctypes
import pickle
import struct
import cv2

serverThread = None
stop = False


def video_stream(conn, streaming):
    streaming.value = True

    while streaming.value:
        frame = serverfunc.take_screenshot()
        _, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        a = pickle.dumps(frame, 0)
        message = struct.pack("Q", len(a)) + a
        conn.sendall(message)

def connectclient(conn):
    global stop
    streaming = Value('b', False)

    while True:
        if stop:
            break

        try:
            data = conn.recv(2048)
        except Exception:
            break

        data = data.decode("utf-8")

        if data == '':
            break

        if data == "take_screenshot":
            frame = serverfunc.take_screenshot()
            
            _, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            a = pickle.dumps(frame, 0)
            message = struct.pack("Q", len(a)) + a
            conn.sendall(message)
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
        if data == "start_streaming":
            newthread = Process(target=video_stream, args=(conn, streaming))
            newthread.start()
        if data == "stop_streaming":
            streaming.value = False
        if data == "get_mac_address":
            mac_address = serverfunc.get_mac_address()
            conn.send(bytes(mac_address, "utf-8"))

def runserver():
    TCP_IP = socket.gethostname()
    TCP_PORT = 8000
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))

    tcpServer.listen(4)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")

    while True:
        client, _ = tcpServer.accept()
        print("New client")
        newthread = Process(target=connectclient, args=(client,))
        newthread.start()

class Server(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.tcpServer = None
        self.start = False

    def initUI(self):
        user32 = ctypes.windll.user32

        desktop_width = user32.GetSystemMetrics(0)
        desktop_height = user32.GetSystemMetrics(1)

        width = int(desktop_width * 0.056)
        height = int(desktop_height * 0.107)

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.setWindowTitle('Server')

        layout = QVBoxLayout()

        open_button = QPushButton("Mở Server", self)
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
            msg = QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText(f"Đã khởi động")
            msg.exec()


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

    sys.exit(app.exec())

if __name__ == '__main__':
    main()