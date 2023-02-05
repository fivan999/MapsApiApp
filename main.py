import sys
import os
import requests
from typing import List
from dataclasses import dataclass, field
from PyQt5.QtWidgets import (QMainWindow, QApplication, QRadioButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from support import get_place_map, get_place_toponym


# для экранов с высоким разрешением
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# текущее состояние карты
@dataclass
class MapsData:
    spn: float = 0.003
    coords: List[float] = field(default_factory=list)
    display: str = "map"
    pt: str = ""
    postal_code: str = ""
    address: str = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUI()

    def setupUI(self) -> None:
        self.setupData()
        self.setWindowTitle("Best Yandex Maps App")
        uic.loadUi("UI/MainWindow.ui", self)
        self.map_type_group.buttonClicked.connect(self.chooseMapType)
        self.search_place_button.clicked.connect(self.searchPlace)
        self.reset_search_button.clicked.connect(self.resetSearchResult)
        self.postal_code_checkbox.stateChanged.connect(self.resetPostalCode)
        self.getPicture()

    # устанавливаем начальные координаты
    def setupData(self) -> None:
        self.data = MapsData()
        self.data.coords = [30.312363709126018, 59.94157564755226]
        self.map_type_choices = {
            "Схема": "map",
            "Спутник": "sat",
            "Гибрид": "sat,skl"
        }

    # получаем картинку запросом
    def getPicture(self) -> None:
        response = get_place_map(self.data)
        if response:
            self.setPicture(response)
        else:
            self.showMessage("reqerror", 
                             f"Ошибка запроса: {response.status_code}. Причина: {response.reason}, {response.request.url}")

    # ставим изображение из ответа сервера
    def setPicture(self, response: requests.Response) -> None:
        with open("image.png", "wb") as file:
            file.write(response.content)
        pixmap = QPixmap("image.png")
        self.picture.setPixmap(pixmap)

    # обработка клавиш
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

    # сообщение пользователю
    def showMessage(self, type: str, text: str) -> None:
        if type == "reqerror":
            QMessageBox.critical(self, "Ошибка запроса", text, QMessageBox.Ok)
 
    # смена типа карты
    def chooseMapType(self, button: QRadioButton) -> None:
        self.data.display = self.map_type_choices[button.text()]
        self.getPicture()

    # поиск места из ввода пользователя
    def searchPlace(self, coords: str = "") -> None:
        place = self.search_place_input.toPlainText().strip()
        if coords:
            toponym = get_place_toponym(coords=coords)
        elif place:
            toponym = get_place_toponym(place_name=place)
        else:
            return

        if toponym:
            toponym = toponym.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            if coords:
                self.setPlace(toponym, set_centre=False)
            else:
                self.setPlace(toponym)
        else:
            self.showMessage("reqerror", 
                            f"Ошибка запроса: {toponym.status_code}. Причина: {toponym.reason}")            

    # ставим метку на карте и позиционируем ее
    def setPlace(self, toponym: dict, set_centre: bool = True) -> None:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coords = toponym["Point"]["pos"]

        if set_centre:
            self.data.coords = list(map(float, toponym_coords.split()))
            self.data.spn = 0.003
        self.data.address = toponym_address
        self.data.pt = ",".join(list(map(str, toponym_coords.split()))) + ",pm2rdm"

        self.getPicture()
        self.getPostalCode(toponym)
        self.resetPostalCode()

    # получаем почтовый код
    def getPostalCode(self, toponym: dict) -> None:
        try:
            self.data.postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']
        except Exception:
            self.data.postal_code = ""

    # удаляем метку
    def resetSearchResult(self) -> None:
        self.data.pt = ""
        self.data.postal_code = ""
        self.data.address = ""
        self.search_address_edit.setPlainText("")
        self.getPicture()

    # реагируем на изменение чекбокса почтового кода
    def resetPostalCode(self) -> None:
        if self.postal_code_checkbox.isChecked() and self.data.postal_code:
            self.search_address_edit.setPlainText(self.data.address + " (" + self.data.postal_code + ")")
        else:
            self.search_address_edit.setPlainText(self.data.address)

    # поиск места по клику ЛКМ
    def searchPlaceClick(self, mouse_pos: tuple) -> None:
        x, y = mouse_pos[0] - 10, mouse_pos[1] - 10
        if 0 <= x <= 600 and 0 <= y <= 450:
            x_size, y_size = self.data.spn / 600, self.data.spn / 450
            coord_1 = self.data.coords[0] - self.data.spn / 2 + x_size * x 
            coord_2 = self.data.coords[1] - self.data.spn / 2 + y_size * y

            print(coord_1, coord_2, self.data.coords)
            self.searchPlace(coords=f"{coord_1},{coord_2}")

    # поиск организации по клику ПКМ
    def searchOrganization(self, mouse_pos: tuple) -> None:
        pass

    # обрабатываем нажатия мыши
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.searchPlaceClick((event.x(), event.y()))
        else:
            self.searchOrganization((event.x(), event.y()))

    # удаляем картинку при закрытии приложения
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        os.remove("image.png")


# ловим ошибки от PyQT
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
