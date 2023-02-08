# MapsApiApp
[![Python package](https://github.com/fivan999/MapsApiApp/actions/workflows/python-package.yml/badge.svg)](https://github.com/fivan999/MapsApiApp/actions/workflows/python-package.yml)
## Приложение на PyQt, использующее возможности Api Яндекс.Карт

### Установка
- Склонировать репозиторий
```
git clone https://github.com/fivan999/MapsApiApp
```
- Создать виртуальное окружение
```
python -m venv venv
venv\Scripts\activate
```
- Установить зависимости
    - Для запуска
    ```
    pip install -r requirements/base.txt

    ```
    - Для разработки
    ```
    pip install -r requirements/dev.txt
    ```
### Запуск
- Создать файл .env в корне проекта и записать в него значение:
    - GEOCODER_APIKEY=ваш-ключ-геокодераБ
Иначе проект работать не будет
- Запусить 
```
python main.py
```
### Управление
- ```PageUP``` - уменьшение области показа
- ```PageDown``` - увеличение области показа
- ```W``` - вверх
- ```S``` - вниз
- ```A``` - влево
- ```D``` - вправо
