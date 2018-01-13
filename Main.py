import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QGridLayout, QGroupBox, QSpinBox, QComboBox, QStyleFactory
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets


import products


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Shop"
        self.left = 30
        self.top = 30
        self.width = 1000
        self.height = 750

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage("v0.1")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)

        fileMenu.addAction(exitButton)

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()

        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Tab 2")

        self.create_tab2()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.tab1.layout = QVBoxLayout(self)

        self.data = products.view("products")
        column_names = self.data[0]
        self.rows = self.data[1]

        self.add_button = QPushButton("Add new product", self)
        self.add_button.setToolTip("Add an item which is not in the list yet")
        self.add_button.move(500, 80)
        self.add_button.clicked.connect(self.add_item)
        self.tab1.layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update product", self)
        self.update_button.setToolTip("Update selected product")
        self.update_button.move(500, 80)
        self.update_button.clicked.connect(self.update_item)
        self.tab1.layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete product", self)
        self.delete_button.setToolTip("Delete selected product")
        self.delete_button.move(500, 80)
        self.delete_button.clicked.connect(self.delete_item)
        self.tab1.layout.addWidget(self.delete_button)

        self.dropdownlist_category = QComboBox()
        categories = set([item_id[4] for item_id in self.data[1]])
        categories.add("All products")
        self.dropdownlist_category.addItems(categories)
        self.dropdownlist_category.activated.connect(self.select_category)
        self.tab1.layout.addWidget(self.dropdownlist_category)

        self.goods_view = QTableWidget()
        self.goods_view.repaint()
        self.goods_view.setColumnCount(len(self.data[0]))
        self.goods_view.setHorizontalHeaderLabels(column_names)
        self.goods_view.move(0, 0)
        self.goods_view.itemSelectionChanged.connect(self.change)

        self.goods_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.goods_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_table()
        self.goods_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab1.layout.addWidget(self.goods_view)

        self.tab1.setLayout(self.tab1.layout)
        self.tab1.layout.addWidget(self.goods_view)
        self.tab1.setLayout(self.tab1.layout)

    def change(self):
        items = self.goods_view.selectedItems()
        self.row_data = [cell.text() for cell in items]

    def refresh_table(self):
        self.rows = products.view("products")[1]
        self.category = self.dropdownlist_category.currentText()
        if self.category == "All products":
            self.goods_view.setRowCount(len(self.rows))
        else:
            self.rows_table = [row[4] for row in self.rows].count(self.category)
            self.goods_view.setRowCount(self.rows_table)
        row_id = 0
        for row in self.rows:
            if self.category == row[4] or self.category == "All products":
                for column_id, cell in enumerate(row):
                    self.goods_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
                row_id += 1
        self.tab1.layout.update()

    @pyqtSlot()
    def select_category(self):
        self.refresh_table()

    @pyqtSlot()
    def add_item(self):
        self.item = products.NewItem(self.data)
        row_id = 0
        for row in self.rows:
            if self.category == row[4] or self.category == "All products":
                for column_id, cell in enumerate(row):
                    self.goods_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
                row_id += 1
        self.refresh_table()

    @pyqtSlot()
    def delete_item(self):
        if self.goods_view.currentRow() < 0:
            return
        buttonReply = QMessageBox.question(self, 'Confirmation', "Do you like want to remove " + self.row_data[1],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            return
        else:
            products.delete(self.row_data[0])
            self.refresh_table()

    @pyqtSlot()
    def update_item(self):
        if self.goods_view.currentRow() < 1:
            return
        self.update_item = products.UpdateItem(self.data, self.goods_view.currentRow())
        self.refresh_table()

    def create_tab2(self):
        self.tab2.layout = QVBoxLayout(self)
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        self.textbutton = QPushButton("Text", self)
        self.textbutton.move(20, 80)
        self.textbutton.clicked.connect(self.on_click_text_button)

        self.label = QLabel("First Label", self)
        self.label.move(200, 80)
        self.tab2.layout.addWidget(self.textbox)
        self.tab2.layout.addWidget(self.textbutton)
        self.tab2.layout.addWidget(self.label)
        self.tab2.setLayout(self.tab2.layout)

    @pyqtSlot()
    def on_click_text_button(self):
        textboxvalue = self.textbox.text()
        QMessageBox.question(self, "Message", "You typed: " + textboxvalue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    shop = App()
    sys.exit(app.exec_())
