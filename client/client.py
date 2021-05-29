import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
try:

    message = 'This is the message.  It will be repeated.'
    print(f'sending {message}')
    s.sendall(bytes(message, "utf-8"))
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = s.recv(16)
        amount_received += len(data)
        print(f'received {data}')

finally:
    s.close()

# # s.sendall(b"Hello, work")
# while True:
#     msg = s.recv(1024)
#
#     print(msg.decode("utf-8"))
