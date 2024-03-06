import sqlite3
import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidget, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн

        self.initDB()
        self.initUI()
        self.pushButton.clicked.connect(self.showAll)

    def initDB(self):
        self.cur = sqlite3.connect("coffee.sqlite").cursor()

    def initUI(self):
        columns = ["ID",
                   "Название сорта",
                   "Степень обжарки",
                   "Молотый/в зернах",
                   "Описание вкуса",
                   "Цена",
                   "Объем упаковки"]
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.resizeColumnsToContents()

    def showAll(self):
        columns = ["ID",
                   "Название сорта",
                   "Степень обжарки",
                   "Молотый/в зернах",
                   "Описание вкуса",
                   "Цена",
                   "Объем упаковки"]
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        query = ("""
            SELECT *
            FROM coffee
        """)
        result = self.cur.execute(query).fetchall()
        table = self.tableWidget
        table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, col in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(col)))
        table.resizeColumnsToContents()
        message = f"Нашлось {str(len(result))} записей" if result else "К сожалению, ничего не нашлось"
        self.statusBar().showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())