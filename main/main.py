import sqlite3
import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QLineEdit, QWidgetItem
from addEditForm import Ui_dialog
from mainForm import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initDB()
        self.initUI()
        self.pushButton.clicked.connect(self.showAll)
        self.pushButton_2.clicked.connect(lambda: self.addRow([]))
        self.pushButton_3.clicked.connect(self.editDB)

    def initDB(self):
        self.cur = sqlite3.connect("../data/coffee.sqlite").cursor()

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
        self.rowMarked = -1
        self.tableWidget.cellClicked.connect(self.markRow)

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

    def markRow(self, row, column):
        self.rowMarked = row

    def addRow(self, data):
        newDialog = QDialog(self)
        newWindow = Ui_dialog()
        newWindow.setupUi(newDialog)
        newDialog.setWindowTitle("Добавить новую запись")
        newWindow.buttonBox.accepted.connect(lambda: self.saveRow(newWindow.verticalLayout))
        if data:
            vert: QVBoxLayout = newWindow.verticalLayout
            [vert.itemAt(i).widget().setText(text) for i, text in enumerate(data)]
        newDialog.show()

    def saveRow(self, layout):
        vert: QVBoxLayout = layout
        data = [vert.itemAt(i).widget().text() for i in range(layout.count())]
        if all(data):
            values = "NULL, " + ', '.join(map(lambda x: f"'{x}'", data))
            query = f"""
                    INSERT INTO coffee
                    VALUES ({values})
                    """
            try:
                self.cur.execute(query)
                self.showAll()
            except Exception as e:
                self.saveRow(layout)
        else:
            self.addRow(data)

    def editDB(self):
        if self.rowMarked < 0:
            return
        table: QTableWidget = self.tableWidget
        columnsNum = table.columnCount()
        newDialog = QDialog(self)
        newWindow = Ui_dialog()
        newWindow.setupUi(newDialog)
        newDialog.setWindowTitle("Редактировать запись")
        data = [table.item(self.rowMarked, col).text() for col in range(columnsNum)]
        vert: QVBoxLayout = newWindow.verticalLayout
        [vert.itemAt(i).widget().setText(text) for i, text in enumerate(data[1:])]
        newWindow.buttonBox.accepted.connect(lambda: self.updateRow(data[0], newWindow.verticalLayout))
        newDialog.show()

    def updateRow(self, rowId, layout):
        vert: QVBoxLayout = layout
        data = [vert.itemAt(i).widget().text() for i in range(layout.count())]
        if all(data):
            query = f"""
            UPDATE coffee
            SET sortName = '{data[0]}',
            grillRate = '{data[1]}',
            beansOrGround = '{data[2]}',
            tasteDescription = '{data[3]}',
            price = '{data[4]}',
            volume = '{data[5]}'
            WHERE id = '{rowId}'
            """
            try:
                self.cur.execute(query)
                self.rowMarked = -1
                self.showAll()
            except Exception as e:
                self.updateRow(rowId, layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
