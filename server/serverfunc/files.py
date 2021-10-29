import os


def remove_file(file_dir):
    try:
        os.remove(file_dir)
        return "1"
    except Exception as e:
        print(e)
        return "0"


def send_file(file_dir):
    with open(file_dir, "rb") as f:
        bytes_read = f.read()

        return bytes_read