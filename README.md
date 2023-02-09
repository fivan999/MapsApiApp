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
    - GEOCODER_APIKEY=ваш-ключ-геокодера (без него ничего работать не будет)
    - ORGANIZATION_APIKEY=ваш-ключ-поиска-по-организациям (необязательный)
- Запусить 
```
python main.py
```
### Управление
- ```PageUP``` - увеличение области показа
- ```PageDown``` - уменьшение области показа
- ```W``` - вверх
- ```S``` - вниз
- ```A``` - влево
- ```D``` - вправо
