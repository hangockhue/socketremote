import sys
from PyQt5.QtWidgets import QApplication
from screens.home import Home


def main():
    app = QApplication(sys.argv)
    x = Home()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
