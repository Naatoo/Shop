import psycopg2

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QTabWidget
from PyQt5.QtWidgets import QDoubleSpinBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView
from PyQt5.QtCore import pyqtSlot

from datetime import datetime

from application.db.queries import view_column_names, view_data
from application.tabs.products import ProductsTable
from application.tabs.customers import CustomersTable
from application.db.tables import create_temp


def insert_ordered_position(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    INSERT INTO ordered_position
    ("ID_prod", "Quantity", "Selling price", "ID_ord")
    VALUES (%s, %s, %s, %s)
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


def insert_order(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    INSERT INTO orders ("Order Date", "Payment Date", "ID_cust")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, data)

    connection.commit()
    connection.close()


def find_free_id():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    SELECT max("ID") + 1
    FROM orders
    '''
    cursor.execute(sql)

    id = cursor.fetchone()
    connection.commit()
    connection.close()
    return id


def temp_insert(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    INSERT INTO temp
    ("Item ID", "Name", "Quantity", "Selling Price", "Category")
    VALUES
        (%s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, data)

    connection.commit()
    connection.close()


def delete_from_current_order(name):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    DELETE FROM temp
    WHERE "Name" = %s
    '''
    cursor.execute(sql, (name,))

    connection.commit()
    connection.close()


def update_quantity(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    UPDATE products
    SET
        "Quantity" = "Quantity" - %s
    WHERE "ID" = %s
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


class NewOrderWidgetTab(QTabWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QGridLayout(self)

        create_temp()
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
        self.customer_choice_window = SelectCustomerWindow(parent=self)
        width = 850
        height = 600
        self.customer_choice_window.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    def refresh_chosen_customer(self):
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
            final_order_data = [[row[0], quantity_list[index], price_list[index], find_free_id()[0]]
                                for index, row in enumerate(self.temp_products.rows)]
            now_datetime = str(datetime.now())[:-7]
            insert_order([now_datetime, None, self.customer_choice_window.chosen_customer_id])
            insert_ordered_position(final_order_data)
    #        self.parent().tab_orders.orders_table.refresh_orders(search_by="All", text="")
            update_quantity([row[1::-1] for row in final_order_data])
     #       self.parent().tab_products.select_category()
            create_temp()
            self.temp_products.refresh_products()
            self.label_chosen_customer.setText("Choose customer")


class ProductsTemp(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        column_names = view_column_names("temp")[1:]

        self.setColumnCount(len(column_names))
        self.setHorizontalHeaderLabels(column_names)
        self.itemSelectionChanged.connect(self.change_products)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.quantity_list = []
        self.price_list = []

        self.change_products()
        self.refresh_products()

        self.setSortingEnabled(True)
        self.resizeRowsToContents()
        self.horizontalHeader().sortIndicatorChanged.connect(self.resizeRowsToContents)

    def change_products(self):
        items = self.selectedItems()
        self.row_data_product = [cell.text() for cell in items]

    def refresh_products(self):
        self.rows = [row[1:] for row in view_data("temp")]
        self.setRowCount(len(self.rows))
        for row_id, row in enumerate(self.rows):
            for column_id, cell in enumerate(row):
                if column_id not in (2, 3):
                    self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
                else:
                    editable = QDoubleSpinBox()
                    editable.setSingleStep(1)
                    if column_id == 2:
                        self.quantity_list.append(editable)
                        editable.setMinimum(1)
                        editable.setMaximum(cell)
                        editable.setDecimals(0)
                        editable.setValue(1)
                    if column_id == 3:
                        self.price_list.append(editable)
                        editable.setMinimum(0.01)
                        editable.setMaximum(100000)
                        editable.setDecimals(2)
                        editable.setValue(cell)
                    self.setCellWidget(row_id, column_id, editable)

    def delete(self):
        if self.rows and self.row_data_product:
            name_deleted_item = self.row_data_product[1]
            if name_deleted_item not in self.rows[-1]:
                default_name = give_name_to_select(name_deleted_item)[0]
                for row in self.rows:
                    if default_name in row:
                        self.row_data_product = row
                        break
            else:
                if len(self.rows) > 1:
                    self.row_data_product = self.rows[-2]
            delete_from_current_order(name_deleted_item)
            self.refresh_products()
        else:
            pass


class SelectItem(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.layout = QGridLayout()

        self.add_button = QPushButton("Add product", self)
        self.add_button.setToolTip("Add this item to an order")
        self.add_button.clicked.connect(self.add)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        self.products_table = ProductsTable(parent=self)
        self.products_table.itemDoubleClicked.connect(self.add)

        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.products_table)
        self.setLayout(self.layout)
        self.show()

    def add(self):
        if self.products_table.row_data[2] == "0":
            QMessageBox.information(self, "Error", "You do not have this item in stock")
            return
        else:
            temp_insert(self.products_table.row_data)
            self.close()
            self.parent().refresh_products_in_order()


class SelectCustomerWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.layout = QGridLayout(self)

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

        header = self.customers_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.setLayout(self.layout)
        self.show()

    def select_and_close(self):
        if not self.customers_table.row_data_customers:
            return
        else:
            self.chosen_customer_id = self.customers_table.row_data_customers[0]
            self.close()
            self.parent().refresh_chosen_customer()
