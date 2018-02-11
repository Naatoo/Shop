from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets

import psycopg2
from queries import view_data, view_column_names


def delete_order(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DELETE FROM ordered_position WHERE "ID_ord"=%s;'''
    cursor.execute(sql, (id,))

    sql = '''DELETE FROM orders WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))

    connection.commit()
    connection.close()


def view_new_order():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''SELECT "Name" FROM customers'''
    cursor.execute(sql)
    customers = cursor.fetchall()

    sql = '''SELECT max("ID") FROM orders'''
    cursor.execute(sql)
    orders_id = cursor.fetchone()

    sql = '''SELECT * FROM products'''
    cursor.execute(sql)
    products = cursor.fetchall()

    return [name[0] for name in customers],  orders_id[0], products


def insert_ordered_position(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''INSERT INTO ordered_position
          ("ID_prod", "Quantity", "Selling price",  "ID_ord")
          VALUES (%s, %s, %s, %s)'''
    for row in data:
        cursor.execute(sql, row)
        connection.commit()
    connection.close()


def insert_order(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''INSERT INTO orders ("Ordered", "Paid", "ID_cust")
             VALUES (%s, %s, %s)'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


class Order(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.groupbox= QGroupBox()
        self.layout = QVBoxLayout(self)

        self.setLayout(self.layout)
        self.setAutoFillBackground(True)
        self.orders_column_names = view_column_names("orders_items_view")
        self.orders_data = view_data("orders_items_view")
        self.single_order_view = QTableWidget()
        self.single_order_view.repaint()
        self.single_order_view.setColumnCount(len(self.orders_column_names))
        self.single_order_view.setHorizontalHeaderLabels(self.orders_column_names)
        self.single_order_view.move(0, 0)

        self.single_order_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.single_order_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_order()
        self.single_order_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.single_order_view)

        self.close_button = QPushButton("Close")
        self.layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

        self.setLayout(self.layout)

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    def refresh_order(self):
        self.orders_data = view_data("orders_items_view")
        self.single_order_view.setRowCount(len(self.orders_data))
        row_id = 0
        for row in self.orders_data:
            for column_id, cell in enumerate(row):
                self.single_order_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
            row_id += 1
        self.layout.update()


# class NewOrder(QWidget):
#     def __init__(self):
#         super(QWidget, self).__init__()
#
#         self.title = "Add new order"
#         self.left = 100
#         self.top = 100
#         self.width = 800
#         self.height = 600
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         self.groupbox = QGroupBox()
#         self.layout = QGridLayout()
#
#         self.default_values = []
#
#         self.id_label = QLabel("Customer id")
#         self.id_input = QSpinBox()
#         self.id_input.setMaximum(100000)
#
#         # Default values
#         self.customers, self.orders_id, self.products = view_new_order()
#         print(self.customers)
#         print(self.orders_id)
#         print(self.products)
# #        self.id_default = max(self.orders_id) + 1
#  #       print(self.id_default)
#
#         self.customer_name_input = QComboBox()
#         self.customer_name_input.addItems(self.customers)
# #        self.layout.addWidget(self.customer_name_label, 1, 0)
#         self.layout.addWidget(self.customer_name_input, 1, 0)
#
#         self.add_customers_button = QPushButton("Add new customers", self)
#         self.add_customers_button.setToolTip("Add a customer which is not in the list yet")
#         self.add_customers_button.move(500, 80)
#         self.add_customers_button.clicked.connect(self.add_customer)
#         self.layout.addWidget(self.add_customers_button, 2, 0)
#
#         self.customers_view = CustomersTable()
#         self.layout.addWidget(self.customers_view, 3, 0)
#
#         self.groupbox.setLayout(self.layout)
#         windowLayout = QVBoxLayout()
#         windowLayout.addWidget(self.groupbox)
#         self.setLayout(windowLayout)
#         self.show()
#
#     @pyqtSlot()
#     def add_customer(self):
#         self.customer = NewCustomer()
#     #    self.customer.refresh_customers()
#
#     @pyqtSlot()
#     def reset_to_default(self):
#    #     self.id_input.setValue(self.id_default)
#         self.name_input.setCurrentIndex(0)
#         self.city_input.setCurrentIndex(0)
#         self.street_input.setCurrentIndex(0)
#         self.house_input.setText("1")
#         self.zipcode_input.setCurrentIndex(1)
#
