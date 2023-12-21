import os
import sys
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QLineEdit, QComboBox, QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class DisplayWidget(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.initUi(data)

    def initUi(self, data):
        self.setWindowTitle('Информация о книге')
        self.setGeometry(300, 300, 300, 500)
        labels = ['Название', 'Автор', 'Год выпуска', 'Жанр']
        for i in range(4):
            self.titleLabel = QLabel(f'<font size=24><b>{labels[i]}</b></font>', self)
            font = self.titleLabel.font()
            font.setPointSize(50)
            self.titleLabel.adjustSize()
            self.titleLabel.move((300 - self.titleLabel.width()) // 2, 220 + 70 * i)
            self.informationLabel = QLabel(f'<font size=5>{data[i]}</font>', self)
            self.informationLabel.adjustSize()
            self.informationLabel.move((300 - self.informationLabel.width()) // 2, 250 + 70 * i)
        self.imageLabel = QLabel(self)
        try:
            if data[-1] is None:
                raise ValueError
            self.pixmap = QPixmap(f'data/{data[-1]}')
        except (FileNotFoundError, ValueError):
            self.pixmap = QPixmap('data/default.png')
        self.pixmap = self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.adjustSize()
        self.imageLabel.move((300 - self.imageLabel.width()) // 2, 10)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.con = sqlite3.connect('books.sqlite')
        self.cur = self.con.cursor()

    def initUi(self):
        self.setWindowTitle('Каталог библиотеки')
        self.setGeometry(300, 300, 500, 600)
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(['Название', 'Автор'])
        self.comboBox.move(20, 20)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.resize(150, 30)
        self.lineEdit.move(20, 90)
        self.searchButton = QPushButton('Искать', self)
        self.searchButton.resize(150, 100)
        self.searchButton.move(220, 20)
        self.searchButton.clicked.connect(self.search)
        self.listWidget = QListWidget(self)
        self.listWidget.resize(450, 400)
        self.listWidget.move(20, 150)

    def search(self):
        self.listWidget.clear()
        query = '''SELECT title, authors.name, year, genres.name, image FROM books
JOIN authors ON books.author = authors.id JOIN genres ON books.genre = genres.id'''
        if self.comboBox.currentText() == 'Название':
            query += f" WHERE title LIKE '%{self.lineEdit.text()}%'"
        else:
            query += f" WHERE authors.name LIKE '%{self.lineEdit.text()}%'"
        result = self.cur.execute(query).fetchall()
        for elem in result:
            item = QListWidgetItem()
            self.listWidget.addItem(item)            
            button = QPushButton(elem[0], self)
            button.clicked.connect(lambda event, data=elem: self.display_information(data))
            self.listWidget.setItemWidget(item, button)
            
    def display_information(self, data):
        self.displayWidget = DisplayWidget(self, data)
        self.displayWidget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())