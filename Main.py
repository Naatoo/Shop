import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QGridLayout, QGroupBox, QSpinBox, QComboBox, QStyleFactory
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets


import products, orders


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

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()

        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Orders")

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

        self.refresh_products()
        self.goods_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab1.layout.addWidget(self.goods_view)
        self.tab1.setLayout(self.tab1.layout)

        self.orders_column_names = orders.view_column_names("orders_view")
        self.orders_data = orders.view_data("orders_view")
        self.tab2.layout = QVBoxLayout(self)
        self.orders_view = QTableWidget()
        self.orders_view.repaint()
        self.orders_view.setColumnCount(len(self.orders_column_names))
        self.orders_view.setHorizontalHeaderLabels(self.orders_column_names)
        self.orders_view.move(0, 0)
        self.orders_view.itemSelectionChanged.connect(self.change)

        self.orders_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.orders_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_orders()
        self.orders_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab2.layout.addWidget(self.orders_view)

        self.tab2.setLayout(self.tab2.layout)

    def refresh_orders(self):
        self.orders_data = orders.view_data("orders_view")
        self.orders_view.setRowCount(len(self.orders_data))
        # self.category = self.dropdownlist_category.currentText()
        # if self.category == "All products":
        #     self.goods_view.setRowCount(len(self.rows))
        # else:
        #     self.rows_table = [row[4] for row in self.rows].count(self.category)
        #     self.goods_view.setRowCount(self.rows_table)
        row_id = 0
        for row in self.orders_data:
            for column_id, cell in enumerate(row):
                self.orders_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
            row_id += 1
        self.tab2.layout.update()


    def change(self):
        items = self.goods_view.selectedItems()
        self.row_data = [cell.text() for cell in items]

    def refresh_products(self):
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
        self.refresh_products()

    @pyqtSlot()
    def add_item(self):
        self.item = products.NewItem(self.data)
        row_id = 0
        for row in self.rows:
            if self.category == row[4] or self.category == "All products":
                for column_id, cell in enumerate(row):
                    self.goods_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
                row_id += 1
        self.refresh_products()

    @pyqtSlot()
    def delete_item(self):
        if self.goods_view.currentRow() < 0:
            return
        buttonReply = QMessageBox.question(self, 'Confirmation', "Do you want to remove " + self.row_data[1],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            return
        else:
            products.delete(self.row_data[0])
            self.refresh_products()

    @pyqtSlot()
    def update_item(self):
        if self.goods_view.currentRow() < 1:
            return
        self.update_item = products.UpdateItem(self.data, self.goods_view.currentRow())
        self.refresh_products()

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
