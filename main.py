import sys
import requests
from typing import List
from dataclasses import dataclass, field
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from support import get_place_map


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


@dataclass
class MapsData:
    scale: int = 10
    coords: List[float] = field(default_factory=list)
    display: str = "map"


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUI()

    def setupUI(self) -> None:
        self.setupData()
        self.setWindowTitle("Best Yandex Maps App")
        uic.loadUi("UI/MainWindow.ui", self)
        self.getPicture()

    def setupData(self) -> None:
        self.data = MapsData()
        self.data.coords = [30.312363709126018, 59.94157564755226]

    def getPicture(self) -> None:
        response = get_place_map(self.data)
        if response:
            self.setPicture(response)
        else:
            raise Exception("invalid request", response.status_code, response.reason)

    def setPicture(self, response: requests.Response) -> None:
        with open("image.png", "wb") as file:
            file.write(response.content)
        pixmap = QPixmap("image.png")
        self.picture.setPixmap(pixmap)
        print(1)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.key()

        if key == Qt.Key.Key_PageUp:
            if self.data.scale != 17:
                self.data.scale += 1
                self.getPicture()

        elif key == Qt.Key.Key_PageDown:
            if self.data.scale != 0:
                self.data.scale -= 1
                self.getPicture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
