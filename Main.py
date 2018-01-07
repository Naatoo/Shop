import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QGridLayout, QGroupBox, QSpinBox, QComboBox
from PyQt5.QtWidgets import QDoubleSpinBox, QTableView
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QIcon

import backend
import tables


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Shop"
        self.left = 100
        self.top = 100
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

        self.data = backend.view("products")

        column_names = self.data[0]
        self.rows = self.data[1]
        self.buttonclick = QPushButton("Add new item", self)
        self.buttonclick.setToolTip("Add an item which is not in the list yet")
        self.buttonclick.move(500, 80)
        self.buttonclick.clicked.connect(self.add_new_item)
        self.buttonclick.clicked.connect(self.update)
        self.tab1.layout.addWidget(self.buttonclick)
        self.goods_view = QTableWidget()
        self.goods_view.repaint()
        self.goods_view.setHorizontalHeaderLabels(column_names)
        self.goods_view.move(0, 0)
        self.add_table()

        self.tab1.layout.addWidget(self.goods_view)

        self.tab1.setLayout(self.tab1.layout)

        self.tab1.layout.addWidget(self.goods_view)

        self.tab1.setLayout(self.tab1.layout)

    def add_table(self):
        self.data = backend.view("products")

        self.rows = self.data[1]
        columns = 5
        self.row = len(self.rows)

        self.goods_view.setRowCount(self.row)
        self.goods_view.setColumnCount(columns)

        for row_id, row in enumerate(self.rows):
            for column_id, cell in enumerate(row):
                self.goods_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
        self.tab1.layout.update()

    @pyqtSlot()
    def add_new_item(self):
        from PyQt5 import QtCore, QtGui

        self.new_item = NewItemWidget(self.data)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.goods_view.setRowCount(self.row)
        for row_id, row in enumerate(self.rows):
            for column_id, cell in enumerate(row):
                self.goods_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
        self.goods_view.update()
        self.add_table()


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


class NewItemWidget(QWidget):
    def __init__(self, data):
        super(QWidget, self).__init__()

        self.title = "Add new item"
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.groupbox= QGroupBox()
        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)

        self.id_label = QLabel("Product id")
        self.id_input = QSpinBox()
        self.id_input.setMaximum(100000)
        self.id_input.setValue(max([item_id[0] for item_id in data[1]]) + 1)
        self.layout.addWidget(self.id_label, 0, 0)
        self.layout.addWidget(self.id_input, 0, 1)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems([item_id[1] for item_id in data[1]])
        self.name_input_edit = QLineEdit()
        self.name_input.setLineEdit(self.name_input_edit)
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.quantity_label = QLabel("Quantity")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(100000)
        self.quantity_input.setValue(1)
        self.layout.addWidget(self.quantity_label, 2, 0)
        self.layout.addWidget(self.quantity_input, 2, 1)

        self.price_sell_label = QLabel("Selling price")
        self.price_sell_input = QDoubleSpinBox()
        self.price_sell_input.setMaximum(100000)
        self.price_sell_input.setValue(100.00)
        self.layout.addWidget(self.price_sell_label, 3, 0)
        self.layout.addWidget(self.price_sell_input, 3, 1)

        self.category_label = QLabel("Category")
        self.category_input = QComboBox()
        self.category_input.addItems([item_id[4] for item_id in data[1]])
        self.category_input_edit = QLineEdit()
        self.category_input.setLineEdit(self.category_input_edit)
        self.layout.addWidget(self.category_label, 4, 0)
        self.layout.addWidget(self.category_input, 4, 1)

        self.add_item_button = QPushButton("Add item")
        self.layout.addWidget(self.add_item_button, 5, 0)

        self.add_item_button.clicked.connect(self.add_item)

        self.cancel_button = QPushButton("Cancel")

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    @pyqtSlot()
    def add_item(self):
        price = self.price_sell_input.text()
        if "," in price:
            price = price.replace(",", ".")
        tables.sql_insert([self.id_input.text(), self.name_input_edit.text(),
                    self.quantity_input.text(), price, self.category_input_edit.text()])
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shop = App()
    sys.exit(app.exec_())
