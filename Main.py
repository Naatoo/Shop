import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QGridLayout, QGroupBox, QSpinBox, QComboBox, QStyleFactory
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5 import QtWidgets, QtCore
from datetime import datetime


import products
import orders
import views
import customers
import vendors
import tables


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

        self.statusBar().showMessage("v0.2")

        self.table_widget = MainWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MainWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab0 = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tabs.addTab(self.tab0, "New Order")
        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Orders")
        self.tabs.addTab(self.tab3, "Customers")
        self.tabs.addTab(self.tab4, "Vendors")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        views.create_view_orders()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        self.tab0.layout = QVBoxLayout(self)
        self.default_values = []

        # Default values
        self.customers, self.id, self.products = orders.view_new_order()

        tables.temp()
        self.choose_customer_button = QPushButton("Choose customer", self)
        self.choose_customer_button.setToolTip("Add a customer which is not in the list yet")
        self.choose_customer_button.move(500, 80)
        self.choose_customer_button.clicked.connect(self.choose_customer)
        self.tab0.layout.addWidget(self.choose_customer_button)

        self.label_chosen_customer = QLabel("Choose customer")
        self.tab0.layout.addWidget(self.label_chosen_customer)

        self.add_button = QPushButton("Add product", self)
        self.add_button.setToolTip("Add new product to the order")
        self.add_button.move(500, 80)
        self.add_button.clicked.connect(self.add_item_to_order)
        self.tab0.layout.addWidget(self.add_button)

        self.temp_products = products.ProductsTemp()

        self.delete_button = QPushButton("Delete product", self)
        self.delete_button.setToolTip("Delete selected product from this order")
        self.delete_button.move(500, 80)
        self.delete_button.clicked.connect(self.temp_products.delete)
        self.tab0.layout.addWidget(self.delete_button)

        self.orders_data = orders.view_data("orders_view")
        self.tab0.layout.addWidget(self.temp_products)

        self.finish_order_button = QPushButton("Finish order", self)
        self.finish_order_button.setToolTip("Finish this order")
        self.finish_order_button.clicked.connect(self.finish_order)
        self.tab0.layout.addWidget(self.finish_order_button)

        self.tab0.setLayout(self.tab0.layout)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        self.tab1.layout = QVBoxLayout(self)

        self.data = products.view("products")
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

        self.goods_view = products.ProductsTable()

        self.refresh_products()
        self.tab1.layout.addWidget(self.goods_view)
        self.tab1.setLayout(self.tab1.layout)

        # -------------------------------------------------------
        # -------------------------------------------------------

        self.orders_column_names = orders.view_column_names("orders_view")
        self.orders_data = orders.view_data("orders_view")
        self.tab2.layout = QVBoxLayout(self)

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
        self.orders_view.itemDoubleClicked.connect(self.show_details)

        self.orders_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.orders_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_orders()
        self.tab2.layout.addWidget(self.orders_view)

        self.tab2.setLayout(self.tab2.layout)

        # -------------------------------------------------------
        # -------------------------------------------------------
        # -------------------------------------------------------

        self.tab3.layout = QVBoxLayout(self)

        self.customers_view = customers.CustomersTable()
        self.add_customers_button = QPushButton("Add new customers", self)
        self.add_customers_button.setToolTip("Add a customer which is not in the list yet")
        self.add_customers_button.clicked.connect(self.add_customer)
        self.add_customers_button.move(500, 80)
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


    @pyqtSlot()
    def choose_customer(self):
        self.customer_choice_window = customers.CustomersWindow(parent=self)
        width = 850
        height = 600
        self.customer_choice_window.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_chosen_customer(self):
        self.customers_view.refresh_customers()
        self.label_chosen_customer.setText(self.customer_choice_window.customers_view.row_data_customers[1])

    @pyqtSlot()
    def add_customer(self):
        self.customer = customers.NewCustomer(parent=self)
        width = 400
        height = 300
        self.customer.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_customers(self):
        self.customers_view.refresh_customers()

    @pyqtSlot()
    def add_item_to_order(self):
        self.selected_product = products.SelectItem(parent=self)
        width = 850
        height = 600
        self.selected_product.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_products_in_order(self):
        self.temp_products.refresh_products()

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

    def finish_order(self):
        if self.temp_products.rows and self.label_chosen_customer.text() != "Choose customer":
   #         data = products.give_items_for_new_order()
            quantity_list = [int(self.temp_products.cellWidget(row, 2).text()) for row in range(self.temp_products.rowCount())]
            price_list = [int(self.temp_products.cellWidget(row, 3).text()[:-3]) for row in range(self.temp_products.rowCount())]
            print(price_list)
            free_order_id = max([val[0] for val in self.orders_data]) + 1
            final_order_data = [[row[0], quantity_list[index], price_list[index], free_order_id] for index, row in enumerate(self.temp_products.rows)]
            print(final_order_data)

            now_datetime = str(datetime.now())[:-7]
            orders.insert_order([now_datetime, None, self.customer_choice_window.chosen_customer_id])

            orders.insert_ordered_position(final_order_data)

            self.refresh_orders()
            tables.temp()
            self.temp_products.refresh_products()
            self.label_chosen_customer.setText("Choose customer")

    # ------------------------------------------------

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

    @pyqtSlot()
    def add_vendor(self):
        self.vendors_data = vendors.view_data("vendors")
        self.vendor = vendors.NewVendor(self.vendors_data, parent=self)
        width = 400
        height = 300
        self.vendor.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)
        self.refresh_vendors()

    @pyqtSlot()
    def delete_vendor(self):
        if self.vendors_view.currentRow() < 0:
            return
        vendors.delete_order(self.row_data_vendors[0])
        self.refresh_vendors()

        # -------------------------------------------------------

    @pyqtSlot()
    def delete_order(self):
        if self.orders_view.currentRow() < 0:
            return
        orders.delete_order(self.row_data_order[0])
        self.refresh_orders()

    @pyqtSlot()
    def show_details(self):
        views.create_view_orders_items(self.row_data_order[0])
        self.order = orders.Order(parent=self)
        width = 850
        height = 600
        self.order.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_orders(self):
        self.orders_data = orders.view_data("orders_view")
        self.orders_view.setRowCount(len(self.orders_data))
        for row_id, row in enumerate(self.orders_data):
            for column_id, cell in enumerate(row):
                self.orders_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
        self.tab2.layout.update()


    def change_orders(self):
        items = self.orders_view.selectedItems()
        free_order_id = []
        self.row_data_order = [cell.text() for cell in items]

        # -------------------------------------------------------

    @pyqtSlot()
    def select_category(self):
        self.refresh_products()

    @pyqtSlot()
    def add_item(self):
        self.item = products.NewItem(self.data, parent=self)
        width = 400
        height = 300
        self.item.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    @pyqtSlot()
    def delete_item(self):
        if self.goods_view.currentRow() < 0:
            return
        buttonReply = QMessageBox.question(self, 'Confirmation', "Do you want to remove "
                                           + self.goods_view.row_data_products[1],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            return
        else:
            products.delete(self.goods_view.row_data_products[0])
            self.refresh_products()

    @pyqtSlot()
    def update_item(self):
        if self.goods_view.currentRow() < 1:
            return
        self.update_item = products.UpdateItem(self.data, self.goods_view.currentRow(), parent=self)
        width = 400
        height = 300
        self.update_item.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    shop = App()
    sys.exit(app.exec_())
