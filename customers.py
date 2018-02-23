import psycopg2

from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget
from PyQt5.QtCore import pyqtSlot

from queries import view_column_names, view_data


def insert_customer(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''INSERT INTO customers
          ("Name", "City", "Street", "House number", "Zip code")
          VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def delete_customer(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DELETE FROM customers WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))

    connection.commit()
    connection.close()


def update_customer(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''UPDATE customers SET
            "Name"=%s,
            "City"=%s,
            "Street"=%s,
            "House number"=%s,
            "Zip code"=%s
             WHERE "ID"=%s'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def search_customer(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    if data[0] == "All":
        sql = '''SELECT * FROM customers
                 WHERE
                 CAST("ID" AS TEXT) LIKE %s
                 OR "Name" ILIKE %s
                 OR "City" ILIKE %s 
                 OR "Street" ILIKE %s
                 OR "Zip code" ILIKE %s
                 ORDER BY "ID"'''
        cursor.execute(sql, tuple([text for text in data[1] for column in range(5)]))
    else:
        if data[0] == "Id":
            sql = '''SELECT * FROM customers
                    WHERE "ID"=%s
                    ORDER BY "ID" '''
        elif data[0] == "Name":
            sql = '''SELECT * FROM customers
                    WHERE "Name" ILIKE %s
                    ORDER BY "ID" '''
        elif data[0] == "City":
            sql = '''SELECT * FROM customers
                    WHERE "City" ILIKE %s 
                    ORDER BY "ID" '''
        elif data[0] == "Street":
            sql = '''SELECT * FROM customers
                    WHERE "Street" ILIKE %s
                    ORDER BY "ID" '''
        elif data[0] == "Zip code":
            sql = '''SELECT * FROM customers
                    WHERE "Zip code" ILIKE %s
                    ORDER BY "ID" '''
        cursor.execute(sql, data[1])

    rows = cursor.fetchall()

    connection.close()
    return rows


class CustomersWidgetTab(QTabWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QGridLayout(self)

        self.customers_table = CustomersTable()
        self.add_customers_button = QPushButton("Add new customers", self)
        self.add_customers_button.setToolTip("Add a customer which is not in the list yet")
        self.add_customers_button.clicked.connect(self.add_customer)

        self.delete_button_customers = QPushButton("Delete customer", self)
        self.delete_button_customers.setToolTip("Delete selected customer")
        self.delete_button_customers.clicked.connect(self.delete_customer)

        self.update_button_customers = QPushButton("Update customer", self)
        self.update_button_customers.setToolTip("Update selected customer")
        self.update_button_customers.clicked.connect(self.update_customer)

        self.search_label = QLabel("Search by:")
        self.dropdownlist_search = QComboBox()
        categories = [column for index, column in enumerate(self.customers_table.column_names) if
                      index in range(4) or index == 5]
        categories.insert(0, "All")
        self.dropdownlist_search.addItems(categories)

        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.search_customers)

        self.layout.addWidget(self.add_customers_button, 0, 0)
        self.layout.addWidget(self.delete_button_customers, 0, 1)
        self.layout.addWidget(self.update_button_customers, 0, 2)
        self.layout.addWidget(self.search_label, 1, 0)
        self.layout.addWidget(self.dropdownlist_search, 1, 1)
        self.layout.addWidget(self.search_field, 1, 2)
        self.layout.addWidget(self.customers_table, 2, 0, 1, 3)
        self.setLayout(self.layout)

    def search_customers(self):
        self.customers_table.refresh_customers(self.dropdownlist_search.currentText(), self.search_field.text())

    @pyqtSlot()
    def add_customer(self):
        self.customer = NewCustomerWindow(parent=self)
        width = 400
        height = 300
        self.customer.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    @pyqtSlot()
    def delete_customer(self):
        if self.customers_table.currentRow() < 0:
            return
        delete_customer(self.customers_table.row_data_customers[0])
        self.search_customers()

    @pyqtSlot()
    def update_customer(self):
        if self.customers_table.currentRow() < 0:
            return
        self.update_customer = UpdateCustomerWindow(self)
        width = 400
        height = 300
        self.update_customer.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width,
                                         height)


class CustomersTable(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        self.column_names = view_column_names("customers")
        self.setColumnCount(len(self.column_names))
        self.setHorizontalHeaderLabels(self.column_names)
        self.itemSelectionChanged.connect(self.change_selection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.refresh_customers(search_by="All", text="")
        self.change_selection()

    def refresh_customers(self, search_by, text):
        self.data = search_customer((search_by, (text + "%",),))
        self.setRowCount(len(self.data))
        for row_id, row in enumerate(self.data):
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))

    def change_selection(self):
        items = self.selectedItems()
        self.row_data_customers = [cell.text() for cell in items]


class NewCustomerWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.data = view_data("customers")

        self.setAutoFillBackground(True)
        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems(set([item_id[1] for item_id in self.data]))
        self.name_input_edit = QLineEdit()

        self.name_input.setLineEdit(self.name_input_edit)
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.city_label = QLabel("City")
        self.city_input = QComboBox()
        self.city_input.addItems(set([item_id[2] for item_id in self.data]))
        self.city_input_edit = QLineEdit()

        self.city_input.setLineEdit(self.city_input_edit)
        self.layout.addWidget(self.city_label, 2, 0)
        self.layout.addWidget(self.city_input, 2, 1)

        self.street_label = QLabel("Street")
        self.street_input = QComboBox()
        self.street_input.addItems(set([item_id[3] for item_id in self.data]))
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
        self.zipcode_input.addItems(set([item_id[5] for item_id in self.data]))
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

        self.setLayout(self.layout)
        self.show()

    @pyqtSlot()
    def reset_to_default(self):
        self.name_input.setCurrentIndex(0)
        self.city_input.setCurrentIndex(0)
        self.street_input.setCurrentIndex(0)
        self.house_input.setText("1")
        self.zipcode_input.setCurrentIndex(1)

    @pyqtSlot()
    def add(self):
        insert_customer([self.name_input_edit.text(), self.city_input_edit.text(), self.street_input_edit.text(),
                         self.house_input.text(), self.zipcode_input_edit.text()])
        self.close()
        self.parent().search_customers()


class UpdateCustomerWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.data = view_data("customers")

        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)
        self.setAutoFillBackground(True)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems(set([item_id[1] for item_id in self.data]))
        self.name_input_edit = QLineEdit()
        self.name_input.setLineEdit(self.name_input_edit)
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.city_label = QLabel("City")
        self.city_input = QComboBox()
        self.city_input.addItems(set([item_id[2] for item_id in self.data]))
        self.city_input_edit = QLineEdit()

        self.city_input.setLineEdit(self.city_input_edit)
        self.layout.addWidget(self.city_label, 2, 0)
        self.layout.addWidget(self.city_input, 2, 1)

        self.street_label = QLabel("Street")
        self.street_input = QComboBox()
        self.street_input.addItems(set([item_id[3] for item_id in self.data]))
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
        self.zipcode_input.addItems(set([item_id[5] for item_id in self.data]))
        self.zipcode_input_edit = QLineEdit()

        self.zipcode_input.setLineEdit(self.zipcode_input_edit)
        self.layout.addWidget(self.zipcode_label, 6, 0)
        self.layout.addWidget(self.zipcode_input, 6, 1)

        self.update_customer_button = QPushButton("Update customer")
        self.layout.addWidget(self.update_customer_button, 7, 0)
        self.update_customer_button.clicked.connect(self.update)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, 7, 1)
        self.cancel_button.clicked.connect(self.close)

        self.reset_button = QPushButton("Reset to default")
        self.layout.addWidget(self.reset_button, 7, 2)
        self.reset_button.clicked.connect(self.reset_to_default)

        self.reset_to_default()
        self.setLayout(self.layout)
        self.show()

    @pyqtSlot()
    def reset_to_default(self):
        row = self.data[self.parent().customers_table.currentRow()]
        self.name_input.setCurrentText(row[1])
        self.city_input.setCurrentText(row[2])
        self.street_input.setCurrentText(row[3])
        self.house_input.setText(row[4])
        self.zipcode_input.setCurrentText(row[5])

    @pyqtSlot()
    def update(self):
        update_customer([self.name_input_edit.text(), self.city_input_edit.text(), self.street_input_edit.text(),
                         self.house_input.text(), self.zipcode_input_edit.text(),
                         self.parent().customers_table.row_data_customers[0]])
        self.close()
        self.parent().search_customers()


class CustomersWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.customers_table = CustomersTable()
        self.customers_table.itemDoubleClicked.connect(self.select_and_close)
        self.layout.addWidget(self.customers_table)

        self.choose_customer_button = QPushButton("Choose customer", self)
        self.choose_customer_button.setToolTip("Choose the customer of this order")
        self.choose_customer_button.clicked.connect(self.select_and_close)
        self.layout.addWidget(self.choose_customer_button)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.close)

        self.setLayout(self.layout)
        self.show()

    def select_and_close(self):
        if not self.customers_table.row_data_customers:
            return
        else:
            self.chosen_customer_id = self.customers_table.row_data_customers[0]
            self.close()
            self.parent().refresh_chosen_customer()
