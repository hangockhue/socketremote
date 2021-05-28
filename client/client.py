import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((socket.gethostname(), 1234))

msg = c.recv(1024)
print(msg.decode("utf-8"))
