import sys
from PyQt6.QtWidgets import QApplication
from screens.home import Home


def main():
    app = QApplication(sys.argv)
    x = Home()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
