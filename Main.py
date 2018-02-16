import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel, QComboBox, QStyleFactory
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, QObject

from datetime import datetime
from queries import view_column_names, view_data

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

        self.customers, self.id, self.products = orders.OrderQueries.view_new_order()

        tables.temp()
        self.choose_customer_button = QPushButton("Choose customer", self)
        self.choose_customer_button.setToolTip("Add a customer which is not in the list yet")
        self.choose_customer_button.clicked.connect(self.choose_customer)
        self.tab0.layout.addWidget(self.choose_customer_button)

        self.label_chosen_customer = QLabel("Choose customer")
        self.tab0.layout.addWidget(self.label_chosen_customer)

        self.add_button = QPushButton("Add product", self)
        self.add_button.setToolTip("Add new product to the order")
        self.add_button.clicked.connect(self.add_item_to_order)
        self.tab0.layout.addWidget(self.add_button)

        self.temp_products = products.ProductsTemp()

        self.delete_button = QPushButton("Delete product", self)
        self.delete_button.setToolTip("Delete selected product from this order")
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

        self.data = view_data("products")

        self.add_button = QPushButton("Add new product", self)
        self.add_button.setToolTip("Add an item which is not in the list yet")
        self.add_button.clicked.connect(self.add_item)

        self.update_button = QPushButton("Update product", self)
        self.update_button.setToolTip("Update selected product")
        self.update_button.clicked.connect(self.update_item)

        self.delete_button = QPushButton("Delete product", self)
        self.delete_button.setToolTip("Delete selected product")
        self.delete_button.clicked.connect(self.delete_item)

        self.dropdownlist_category = QComboBox()
        categories = set([item_id[4] for item_id in self.data])
        categories.add("All products")
        self.dropdownlist_category.addItems(categories)
        self.products_table = products.ProductsTable(parent=self)

        self.dropdownlist_category.activated.connect(self.select_category)

        self.tab1.layout.addWidget(self.add_button)
        self.tab1.layout.addWidget(self.update_button)
        self.tab1.layout.addWidget(self.delete_button)
        self.tab1.layout.addWidget(self.dropdownlist_category)
        self.tab1.layout.addWidget(self.products_table)
        self.tab1.setLayout(self.tab1.layout)

        # -------------------------------------------------------

        self.tab2.layout = QVBoxLayout(self)

        self.orders_table = orders.OrdersTable()

        self.order_details_button = QPushButton("Show order details", self)
        self.order_details_button.setToolTip("Show details of selected order")
        self.order_details_button.clicked.connect(self.orders_table.show_details)

        self.delete_button_orders = QPushButton("Delete order", self)
        self.delete_button_orders.setToolTip("Delete selected order")
        self.delete_button_orders.clicked.connect(self.orders_table.delete_order)

        self.tab2.layout.addWidget(self.order_details_button)
        self.tab2.layout.addWidget(self.delete_button_orders)
        self.tab2.layout.addWidget(self.orders_table)

        self.tab2.setLayout(self.tab2.layout)

        # -------------------------------------------------------

        self.tab3.layout = QVBoxLayout(self)

        self.customers_table = customers.CustomersTable()
        self.add_customers_button = QPushButton("Add new customers", self)
        self.add_customers_button.setToolTip("Add a customer which is not in the list yet")
        self.add_customers_button.clicked.connect(self.add_customer)

        self.tab3.layout.addWidget(self.customers_table)
        self.tab3.layout.addWidget(self.add_customers_button)
        self.tab3.setLayout(self.tab3.layout)
        self.tab3.layout.update()

        # -------------------------------------------------------

        self.tab4.layout = QVBoxLayout(self)
        self.vendors_table = vendors.VendorsTable()

        self.add_vendors_button = QPushButton("Add new vendors", self)
        self.add_vendors_button.setToolTip("Add a vendor which is not in the list yet")
        self.add_vendors_button.clicked.connect(self.add_vendor)

        self.delete_button_vendors = QPushButton("Delete vendor", self)
        self.delete_button_vendors.setToolTip("Delete selected vendor")
        self.delete_button_vendors.clicked.connect(self.delete_vendor)

        self.tab4.layout.addWidget(self.add_vendors_button)
        self.tab4.layout.addWidget(self.delete_button_vendors)
        self.tab4.layout.addWidget(self.vendors_table)
        self.tab4.setLayout(self.tab4.layout)

        # -------------------------------------------------------

    @pyqtSlot()
    def choose_customer(self):
        self.customer_choice_window = customers.CustomersWindow(parent=self)
        width = 850
        height = 600
        self.customer_choice_window.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_chosen_customer(self):
        self.customers_table.refresh_customers()
        self.label_chosen_customer.setText(self.customer_choice_window.customers_table.row_data_customers[1])

    @pyqtSlot()
    def add_customer(self):
        self.customer = customers.NewCustomerWindow(parent=self)
        width = 400
        height = 300
        self.customer.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

        # -------------------------------------------------------

    @pyqtSlot()
    def add_item_to_order(self):
        self.selected_product = products.SelectItem(parent=self)
        width = 850
        height = 600
        self.selected_product.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_products_in_order(self):
        self.temp_products.refresh_products()

    def finish_order(self):
        if self.temp_products.rows and self.label_chosen_customer.text() != "Choose customer":
            quantity_list = [int(self.temp_products.cellWidget(row, 2).text())
                             for row in range(self.temp_products.rowCount())]
            price_list = [int(self.temp_products.cellWidget(row, 3).text()[:-3])
                          for row in range(self.temp_products.rowCount())]
            free_order_id = max([val[0] for val in self.orders_table.data]) + 1
            final_order_data = [[row[0], quantity_list[index], price_list[index], free_order_id]
                                for index, row in enumerate(self.temp_products.rows)]
            now_datetime = str(datetime.now())[:-7]
            orders.OrderQueries.insert_order([now_datetime, None, self.customer_choice_window.chosen_customer_id])

            orders.OrderQueries.insert_ordered_position(final_order_data)

            self.orders_table.refresh_orders()
            tables.temp()
            self.temp_products.refresh_products()
            self.label_chosen_customer.setText("Choose customer")

    # ------------------------------------------------

    @pyqtSlot()
    def add_vendor(self):
        self.vendor = vendors.NewVendor(parent=self)
        width = 400
        height = 300
        self.vendor.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width,
                                height)
        self.vendors_table.refresh_vendors()

    @pyqtSlot()
    def delete_vendor(self):
        if self.vendors_table.currentRow() < 0:
            return
        vendors.delete_vendor(self.vendors_table.row_data[0])
        self.vendors_table.refresh_vendors()

        # -------------------------------------------------------

    @pyqtSlot()
    def select_category(self):
        args = self.dropdownlist_category.currentText(),
        self.products_table.refresh_products(*args)


    @pyqtSlot()
    def add_item(self):
        self.item = products.NewItem(parent=self)
        width = 400
        height = 300
        self.item.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    @pyqtSlot()
    def delete_item(self):
        if self.products_table.currentRow() < 0:
            return
        buttonReply = QMessageBox.question(self, 'Confirmation', "Do you want to remove "
                                           + self.products_table.row_data[1],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            return
        else:
            products.delete_product(self.products_table.row_data[0])
            self.select_category()

    @pyqtSlot()
    def update_item(self):
        if self.products_table.currentRow() < 1:
            return
        self.update_item = products.UpdateItem(parent=self)
        width = 400
        height = 300
        self.update_item.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    shop = App()
    sys.exit(app.exec_())
