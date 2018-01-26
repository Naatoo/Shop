from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QDoubleSpinBox, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets

import psycopg2
from customers import NewCustomer
from customers import CustomersTable

def view_data(table_name):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''SELECT * FROM %s ORDER BY "ID"''' % table_name
    cursor.execute(sql)
    rows = cursor.fetchall()

    connection.close()
    return rows


def view_column_names(table_name):
    data = (table_name,)
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s"
    cursor.execute(sql, data)
    column_names = cursor.fetchall()
    column_names_final = [tup[0].title() for tup in column_names]

    connection.close()
    return column_names_final


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

    sql = '''SELECT "ID" FROM orders'''
    cursor.execute(sql)
    orders_id = cursor.fetchall()

    sql = '''SELECT * FROM products'''
    cursor.execute(sql)
    products = cursor.fetchall()

    return [name[0] for name in customers],  [id[0] for id in orders_id], products


class Order(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__()

        self.title = "Order details"
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.groupbox= QGroupBox()
        self.layout = QVBoxLayout(self)

        self.setLayout(self.layout)

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


class NewOrder(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.title = "Add new order"
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

        self.default_values = []

        self.id_label = QLabel("Customer id")
        self.id_input = QSpinBox()
        self.id_input.setMaximum(100000)

        # Default values
        self.customers, self.orders_id, self.products = view_new_order()
        print(self.customers)
        print(self.orders_id)
        print(self.products)
        self.id_default = max(self.orders_id) + 1
        print(self.id_default)

        self.customer_name_label = QLabel("Customer")
        self.customer_name_input = QComboBox()
        self.customer_name_input.addItems(self.customers)
        self.layout.addWidget(self.customer_name_label, 1, 0)
        self.layout.addWidget(self.customer_name_input, 1, 1)

        self.add_customers_button = QPushButton("Add new customers", self)
        self.add_customers_button.setToolTip("Add a customer which is not in the list yet")
        self.add_customers_button.move(500, 80)
        self.add_customers_button.clicked.connect(self.add_customer)
        self.layout.addWidget(self.add_customers_button)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, 7, 1)
        self.cancel_button.clicked.connect(self.close)

        self.reset_button = QPushButton("Reset to default")
        self.layout.addWidget(self.reset_button, 7, 2)
        self.reset_button.clicked.connect(self.reset_to_default)

        self.customers_view = CustomersTable()
        self.layout.addWidget(self.customers_view)

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    @pyqtSlot()
    def add_customer(self):
        self.customer = NewCustomer()
    #    self.customer.refresh_customers()

    @pyqtSlot()
    def reset_to_default(self):
        self.id_input.setValue(self.id_default)
        self.name_input.setCurrentIndex(0)
        self.city_input.setCurrentIndex(0)
        self.street_input.setCurrentIndex(0)
        self.house_input.setText("1")
        self.zipcode_input.setCurrentIndex(1)

