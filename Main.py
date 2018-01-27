import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QGridLayout, QGroupBox, QSpinBox, QComboBox, QStyleFactory
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets


import products
import orders
import views
import customers
import vendors


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
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Orders")
        self.tabs.addTab(self.tab3, "Customers")
        self.tabs.addTab(self.tab4, "Vendors")

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
        self.goods_view.itemSelectionChanged.connect(self.change_products)

        self.goods_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.goods_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_products()
        self.goods_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab1.layout.addWidget(self.goods_view)
        self.tab1.setLayout(self.tab1.layout)

        # -------------------------------------------------------
        # -------------------------------------------------------

        self.orders_column_names = orders.view_column_names("orders_view")
        self.orders_data = orders.view_data("orders_view")
        self.tab2.layout = QVBoxLayout(self)

        self.add_order_button = QPushButton("Add new order", self)
        self.add_order_button.move(500, 80)
        self.add_order_button.clicked.connect(self.add_order)
        self.tab2.layout.addWidget(self.add_order_button)

        self.delete_button_orders = QPushButton("Delete order", self)
        self.delete_button_orders.setToolTip("Delete selected order")
        self.delete_button_orders.move(500, 80)
        self.delete_button_orders.clicked.connect(self.delete_order)
        self.tab2.layout.addWidget(self.delete_button_orders)

        self.orders_view = QTableWidget()
        self.orders_view.repaint()
        self.orders_view.setColumnCount(len(self.orders_column_names))
        self.orders_view.setHorizontalHeaderLabels(self.orders_column_names)
        self.orders_view.move(0, 0)
        self.orders_view.itemSelectionChanged.connect(self.change_orders)
        self.orders_view.itemClicked.connect(self.show_details)

        self.orders_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.orders_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_orders()
        self.orders_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab2.layout.addWidget(self.orders_view)

        self.tab2.setLayout(self.tab2.layout)

        # -------------------------------------------------------
        # -------------------------------------------------------
        # -------------------------------------------------------

        # self.customers_column_names = customers.view_column_names("customers")
        # self.customers_data = customers.view_data("customers")
        self.tab3.layout = QVBoxLayout(self)

        self.customers_view = customers.CustomersTable()
    #    print(self.customers_view.row_data_customers)
        self.add_customers_button = QPushButton("Add new customers", self)
        self.add_customers_button.setToolTip("Add a customer which is not in the list yet")
        self.add_customers_button.move(500, 80)
  #      self.add_customers_button.clicked.connect(self.add_customer)
        self.tab3.layout.addWidget(self.add_customers_button)

        self.tab3.layout.addWidget(self.customers_view)

        self.tab3.setLayout(self.tab3.layout)
        self.tab3.layout.update()

        # -------------------------------------------------------
        # -------------------------------------------------------
        # -------------------------------------------------------
        # -------------------------------------------------------

        self.vendors_column_names = customers.view_column_names("vendors")
        self.vendors_data = customers.view_data("vendors")
        self.tab4.layout = QVBoxLayout(self)

        self.add_vendors_button = QPushButton("Add new vendors", self)
        self.add_vendors_button.setToolTip("Add a vendor which is not in the list yet")
        self.add_vendors_button.move(500, 80)
        self.add_vendors_button.clicked.connect(self.add_vendor)
        self.tab4.layout.addWidget(self.add_vendors_button)

        self.delete_button_vendors = QPushButton("Delete vendor", self)
        self.delete_button_vendors.setToolTip("Delete selected vendor")
        self.delete_button_vendors.move(500, 80)
        self.delete_button_vendors.clicked.connect(self.delete_vendor)
        self.tab4.layout.addWidget(self.delete_button_vendors)

        self.vendors_view = QTableWidget()
        self.vendors_view.repaint()
        self.vendors_view.setColumnCount(len(self.vendors_column_names))
        self.vendors_view.setHorizontalHeaderLabels(self.vendors_column_names)
        self.vendors_view.move(0, 0)
        self.vendors_view.itemSelectionChanged.connect(self.change_vendors)

        self.vendors_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.vendors_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_vendors()
        self.vendors_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab4.layout.addWidget(self.vendors_view)

        self.tab4.setLayout(self.tab4.layout)

        # -------------------------------------------------------

    def refresh_vendors(self):
        self.vendors_data = vendors.view_data("vendors")
        self.vendors_view.setRowCount(len(self.vendors_data))
        for row_id, row in enumerate(self.vendors_data):
            for column_id, cell in enumerate(row):
                self.vendors_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
        self.tab4.layout.update()

    def change_vendors(self):
        items = self.vendors_view.selectedItems()
        self.row_data_vendors = [cell.text() for cell in items]
        print(self.row_data_vendors[0])

    @pyqtSlot()
    def add_vendor(self):
        self.vendors_data = vendors.view_data("vendors")
        self.vendor = vendors.NewVendor(self.vendors_data)
        self.refresh_vendors()

    @pyqtSlot()
    def delete_vendor(self):
        if self.vendors_view.currentRow() < 0:
            return
        vendors.delete_order(self.row_data_vendors[0])
        self.refresh_vendors()

        # -------------------------------------------------------

    # def refresh_customers(self):
    #     self.customers_data = customers.view_data("customers")
    #     self.customers_view.setRowCount(len(self.customers_data))
    #     for row_id, row in enumerate(self.customers_data):
    #         for column_id, cell in enumerate(row):
    #             self.customers_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
    #     self.tab3.layout.update()
    #
    # def change_customers(self):
    #     items = self.customers_view.selectedItems()
    #     self.row_data_customers = [cell.text() for cell in items]
    #     print(self.row_data_customers[0])
    #
    # @pyqtSlot()
    # def add_customer(self):
    #     self.customer = customers.NewCustomer()
    #     self.refresh_customers()

    @pyqtSlot()
    def add_order(self):
        self.orders = orders.NewOrder()
        self.refresh_orders()

    @pyqtSlot()
    def delete_order(self):
        if self.orders_view.currentRow() < 0:
            return
        orders.delete_order(self.row_data_order[0])
        self.refresh_orders()

    @pyqtSlot()
    def show_details(self):
        views.create_view_orders_items(self.row_data_order[0])
        self.order = orders.Order(self.row_data_order)

    def refresh_orders(self):
        self.orders_data = orders.view_data("orders_view")
        self.orders_view.setRowCount(len(self.orders_data))
        for row_id, row in enumerate(self.orders_data):
            for column_id, cell in enumerate(row):
                self.orders_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
        self.tab2.layout.update()

    def change_orders(self):
        items = self.orders_view.selectedItems()
        self.row_data_order = [cell.text() for cell in items]

        # -------------------------------------------------------

    def change_products(self):
        items = self.goods_view.selectedItems()
        self.row_data_product = [cell.text() for cell in items]

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
        buttonReply = QMessageBox.question(self, 'Confirmation', "Do you want to remove " + self.row_data_product[1],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            return
        else:
            products.delete(self.row_data_product[0])
            self.refresh_products()

    @pyqtSlot()
    def update_item(self):
        if self.goods_view.currentRow() < 1:
            return
        self.update_item = products.UpdateItem(self.data, self.goods_view.currentRow())
        self.refresh_products()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    shop = App()
    sys.exit(app.exec_())
