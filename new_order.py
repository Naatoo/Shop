import psycopg2

from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWidgets import QDoubleSpinBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView
from PyQt5.QtCore import pyqtSlot

from datetime import datetime

from queries import view_column_names, view_data
from orders import OrderQueries
from products import ProductsTemp, SelectItem, update_quantity
from customers import CustomersWindow
import tables


def find_free_id():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''SELECT max("ID") + 1
             FROM orders'''
    cursor.execute(sql)
    id = cursor.fetchone()
    connection.commit()
    connection.close()
    return id


class NewOrderWidgetTab(QTabWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QGridLayout(self)

        self.customers, self.id, self.products = OrderQueries.view_new_order()

        tables.temp()
        self.choose_customer_button = QPushButton("Choose customer", self)
        self.choose_customer_button.setToolTip("Add a customer which is not in the list yet")
        self.choose_customer_button.clicked.connect(self.choose_customer)

        self.label_chosen_customer = QLabel("Choose customer")

        self.add_button = QPushButton("Add product", self)
        self.add_button.setToolTip("Add new product to the order")
        self.add_button.clicked.connect(self.add_item_to_order)

        self.temp_products = ProductsTemp()

        self.delete_button = QPushButton("Delete product", self)
        self.delete_button.setToolTip("Delete selected product from this order")
        self.delete_button.clicked.connect(self.temp_products.delete)

        self.finish_order_button = QPushButton("Finish order", self)
        self.finish_order_button.setToolTip("Finish this order")
        self.finish_order_button.clicked.connect(self.finish_order)

        header = self.temp_products.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.add_button, 0, 0)
        self.layout.addWidget(self.delete_button, 0, 1)
        self.layout.addWidget(self.label_chosen_customer, 1, 0)
        self.layout.addWidget(self.choose_customer_button, 1, 1)
        self.layout.addWidget(self.temp_products, 2, 0, 1, 2)
        self.layout.addWidget(self.finish_order_button)
        self.setLayout(self.layout)

    @pyqtSlot()
    def choose_customer(self):
        self.customer_choice_window = CustomersWindow(parent=self)
        width = 850
        height = 600
        self.customer_choice_window.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_chosen_customer(self):
    #    self.customers_table.refresh_customers()
        self.label_chosen_customer.setText(self.customer_choice_window.customers_table.row_data_customers[1])

    @pyqtSlot()
    def add_item_to_order(self):
        self.selected_product = SelectItem(parent=self)
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
      #      free_order_id = max([val[0] for val in self.parent().tab_orders.orders_table.data]) + 1
            final_order_data = [[row[0], quantity_list[index], price_list[index], find_free_id()[0]]
                                for index, row in enumerate(self.temp_products.rows)]
            now_datetime = str(datetime.now())[:-7]
            OrderQueries.insert_order([now_datetime, None, self.customer_choice_window.chosen_customer_id])
            OrderQueries.insert_ordered_position(final_order_data)
    #        self.parent().tab_orders.orders_table.refresh_orders(search_by="All", text="")
            update_quantity([row[1::-1] for row in final_order_data])
     #       self.parent().tab_products.select_category()
            tables.temp()
            self.temp_products.refresh_products()
            self.label_chosen_customer.setText("Choose customer")
