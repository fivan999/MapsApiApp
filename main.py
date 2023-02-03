import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from support import get_place_toponym, get_place_map


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUI()

    def setupUI(self):
        self.coords = [30.312363709126018, 59.94157564755226]
        self.setWindowTitle("Best Yandex Maps App")
        uic.loadUi("UI/MainWindow.ui", self)
        self.getPicture()

    def getPicture(self):
        response = get_place_map(self.coords)
        if response:
            self.setPicture(response)
        else:
            raise Exception("invalid request", response.status_code, response.reason)

    def setPicture(self, response):
        with open("image.png", "wb") as file:
            file.write(response.content)
        pixmap = QPixmap("image.png")
        self.picture.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
