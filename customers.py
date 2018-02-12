from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QDoubleSpinBox, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets

import psycopg2


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


def sql_insert(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''INSERT INTO customers
          ("Name", "City", "Street", "House number", "Zip code")
          VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def delete_order(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DELETE FROM customers WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))

    connection.commit()
    connection.close()


class CustomersTable(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        self.customers_column_names = view_column_names("customers")
        self.customers_data = view_data("customers")
        self.repaint()
        self.setColumnCount(len(self.customers_column_names))
        self.setHorizontalHeaderLabels(self.customers_column_names)
        self.move(0, 0)
        self.itemSelectionChanged.connect(self.change_customers)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.refresh_customers()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.change_customers()

    def refresh_customers(self):
        self.customers_data = view_data("customers")
        self.setRowCount(len(self.customers_data))
        for row_id, row in enumerate(self.customers_data):
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))

    def change_customers(self):
        items = self.selectedItems()
        self.row_data_customers = [cell.text() for cell in items]

    @pyqtSlot()
    def add_customer(self):
        self.customer = NewCustomer()
        self.refresh_customers()


class NewCustomer(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        data = view_data("customers")

        self.setAutoFillBackground(True)
        self.groupbox= QGroupBox()
        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)

        self.default_values = []

        self.id_label = QLabel("Customer id")
        self.id_input = QSpinBox()
        self.id_input.setMaximum(100000)

        # Default values
        self.indexes = [number[0] for number in data]
        if min(self.indexes) > 2:
            self.id_default = min(range(1, min(self.indexes) - 1))
        elif min(self.indexes) == 2:
            self.id_default = 1
        else:
            self.indexes_sorted = sorted(self.indexes)
            for id in self.indexes_sorted:
                if id + 1 not in self.indexes:
                    self.id_default = id + 1
                    break

        self.id_input.setValue(self.id_default)
        self.layout.addWidget(self.id_label, 0, 0)
        self.layout.addWidget(self.id_input, 0, 1)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems(set([item_id[1] for item_id in data]))
        self.name_input_edit = QLineEdit()

        self.name_input.setLineEdit(self.name_input_edit)
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.city_label = QLabel("City")
        self.city_input = QComboBox()
        self.city_input.addItems(set([item_id[2] for item_id in data]))
        self.city_input_edit = QLineEdit()

        self.city_input.setLineEdit(self.city_input_edit)
        self.layout.addWidget(self.city_label, 2, 0)
        self.layout.addWidget(self.city_input, 2, 1)

        self.street_label = QLabel("Street")
        self.street_input = QComboBox()
        self.street_input.addItems(set([item_id[3] for item_id in data]))
        self.street_input_edit = QLineEdit()

        self.street_input.setLineEdit(self.street_input_edit)
        self.layout.addWidget(self.street_label, 4, 0)
        self.layout.addWidget(self.street_input, 4, 1)

        self.house_label = QLabel("House Number")
        self.house_input = QLineEdit()
        self.layout.addWidget(self.house_label, 5, 0)
        self.layout.addWidget(self.house_input, 5, 1)

        self.zipcode_label = QLabel("Zip Code")
        self.zipcode_input = QComboBox()
        self.zipcode_input.addItems(set([item_id[5] for item_id in data]))
        self.zipcode_input_edit = QLineEdit()

        self.zipcode_input.setLineEdit(self.zipcode_input_edit)
        self.layout.addWidget(self.zipcode_label, 6, 0)
        self.layout.addWidget(self.zipcode_input, 6, 1)

        self.add_customer_button = QPushButton("Add customer")
        self.layout.addWidget(self.add_customer_button, 7, 0)
        self.add_customer_button.clicked.connect(self.add)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, 7, 1)
        self.cancel_button.clicked.connect(self.close)

        self.reset_button = QPushButton("Reset to default")
        self.layout.addWidget(self.reset_button, 7, 2)
        self.reset_button.clicked.connect(self.reset_to_default)

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    @pyqtSlot()
    def reset_to_default(self):
        self.id_input.setValue(self.id_default)
        self.name_input.setCurrentIndex(0)
        self.city_input.setCurrentIndex(0)
        self.street_input.setCurrentIndex(0)
        self.house_input.setText("1")
        self.zipcode_input.setCurrentIndex(1)

    @pyqtSlot()
    def add(self):
        data = view_data("customers")

        sql_insert([self.name_input_edit.text(),
                    self.city_input_edit.text(), self.street_input_edit.text(),
                    self.house_input.text(), self.zipcode_input_edit.text()])
        self.close()
        self.parent().refresh_customers()


class CustomersWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.groupbox = QGroupBox()
        self.layout = QGridLayout()

        self.layout = QVBoxLayout(self)

        self.customers_view = CustomersTable()
        self.customers_view.itemDoubleClicked.connect(self.choose_and_close)
        self.layout.addWidget(self.customers_view)

        self.choose_customer_button = QPushButton("Choose customer", self)
        self.choose_customer_button.setToolTip("Choose the customer of this order")
        self.choose_customer_button.move(500, 80)
        self.choose_customer_button.clicked.connect(self.choose_and_close)
        self.layout.addWidget(self.choose_customer_button)

        self.setLayout(self.layout)
        self.layout.update()

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    def choose_and_close(self):
        self.chosen_customer_id = self.customers_view.row_data_customers[0]
        self.close()
        self.parent().refresh_chosen_customer()
