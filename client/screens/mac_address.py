from PyQt6.QtWidgets import QMessageBox

def show_mac_address(socket):
    socket.send(bytes('get_mac_address', 'utf-8'))
    data = socket.recv(2048).decode("utf-8")
    msg = QMessageBox()
    msg.setWindowTitle("Mac Address")
    msg.setText(f"Địa chỉ Mac: {data}")
    msg.exec()