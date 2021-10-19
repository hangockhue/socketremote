import cv2
import pickle
import struct
import time

def streaming_video(socket):
    socket.send(bytes('start_streaming', 'utf-8'))

    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = socket.recv(4*1024)
            if not packet: break
            data += packet
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += socket.recv(4*1024)

        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow("Receiving...", frame)
        cv2.waitKey(1)
        
        if not cv2.getWindowProperty('Receiving...', cv2.WND_PROP_VISIBLE) :
            socket.send(bytes('stop_streaming', 'utf-8'))
            break
