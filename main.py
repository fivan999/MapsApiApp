import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QLabel)
from PyQt5.QtGui import QPixmap
from support import get_place_toponym, get_place_map


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coords = [30.312363709126018, 59.94157564755226]
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Best Yandex Maps Api")
        self.setFixedSize(1000, 500)
        self.picture = QLabel()
        self.picture.setFixedSize(640, 480)
        self.picture.move(20, 20)
        self.getPicture()

    def getPicture(self):
        response = get_place_map(self.coords)
        if response:
            self.setPicture(response)
        else:
            print("invalid request")

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
