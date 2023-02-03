import sys
import requests
from typing import List
from dataclasses import dataclass, field
from PyQt5.QtWidgets import (QMainWindow, QApplication, QRadioButton)
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
    spn: float = 0.003
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
        self.map_type_group.buttonClicked.connect(self.chooseMapType)
        self.getPicture()

    def setupData(self) -> None:
        self.data = MapsData()
        self.data.coords = [30.312363709126018, 59.94157564755226]
        self.map_type_choices = {
            "Схема": "map",
            "Спутник": "sat",
            "Гибрид": "sat,skl"
        }

    def getPicture(self) -> None:
        response = get_place_map(self.data)
        if response:
            self.setPicture(response)
        else:
            print(response.request.url)

    def setPicture(self, response: requests.Response) -> None:
        with open("image.png", "wb") as file:
            file.write(response.content)
        pixmap = QPixmap("image.png")
        self.picture.setPixmap(pixmap)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.key()

        if key == Qt.Key.Key_PageUp:
            if self.data.spn != 89:
                self.data.spn = min(self.data.spn * 2, 89)
                self.getPicture()

        elif key == Qt.Key.Key_PageDown:
            if self.data.spn != 0.002:
                self.data.spn = max(self.data.spn / 2, 0.002)
                self.getPicture()

        elif key == Qt.Key.Key_Up:
            self.data.coords[1] += self.data.spn
            if self.data.coords[1] > 85:
                self.data.coords[1] = 85
            else:
                self.getPicture()

        elif key == Qt.Key.Key_Down:
            self.data.coords[1] -= self.data.spn
            if self.data.coords[1] < 1:
                self.data.coords[1] = min(self.data.spn, 1)
            else:
                self.getPicture()

        elif key == Qt.Key.Key_Right:
            self.data.coords[0] += self.data.spn
            if self.data.coords[0] > 179:
                self.data.coords[0] = 179
            else:
                self.getPicture()

        elif key == Qt.Key.Key_Left:
            self.data.coords[0] -= self.data.spn
            if self.data.coords[0] < 1:
                self.data.coords[0] = min(self.data.spn, 1)
            else:
                self.getPicture()

    def chooseMapType(self, button: QRadioButton) -> None:
        self.data.display = self.map_type_choices[button.text()]
        self.getPicture()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
