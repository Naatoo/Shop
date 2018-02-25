import psycopg2

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QLineEdit, QHeaderView
from PyQt5.QtCore import pyqtSlot

from datetime import datetime
from functools import partial

from queries import view_data, view_column_names
from views import create_view_orders_items


def update_order_paid(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    UPDATE orders
    SET "Payment Date"=%s
    WHERE "ID"=%s
    '''
    cursor.execute(sql, data)

    connection.commit()
    connection.close()


def search_order(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    if data[0] == "All":
        sql = '''
        SELECT *
        FROM orders_view
        WHERE
            CAST("ID" AS TEXT) LIKE %s
            OR "Customer" ILIKE %s
            OR CAST("Order Date" AS TEXT) ILIKE %s
            OR CAST("Payment Date" AS TEXT) ILIKE %s
        ORDER BY "ID"
        '''
        cursor.execute(sql, tuple([text for text in data[1] for columns in range(4)]))
    else:
        if data[0] == "Id":
            sql = '''
            SELECT *
            FROM orders_view
            WHERE CAST("ID" AS TEXT) ILIKE %s
            ORDER BY "ID"
            '''
        elif data[0] == "Customer":
            sql = '''
            SELECT *
            FROM orders_view
            WHERE "Customer" ILIKE %s
            ORDER BY "ID"
            '''
        elif data[0] == "Order Date":
            sql = '''
            SELECT *
            FROM orders_view
            WHERE CAST("Order Date" AS TEXT) ILIKE %s
            ORDER BY "ID"
            '''
        elif data[0] == "Payment Date":
            sql = '''
            SELECT *
            FROM orders_view
            WHERE CAST("Payment Date" AS TEXT) ILIKE %s
            ORDER BY "ID"
            '''
        elif data[0] == "Zip Code":
            sql = '''
            SELECT *
            FROM vendors
            WHERE "Zip code" ILIKE %s
            ORDER BY "ID"
            '''
        cursor.execute(sql, data[1])

    rows = cursor.fetchall()
    connection.close()
    return rows


class OrdersWidgetTab(QTabWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QGridLayout(self)

        self.orders_table = OrdersTable()

        self.order_details_button = QPushButton("Show order details", self)
        self.order_details_button.setToolTip("Show details of selected order")
        self.order_details_button.clicked.connect(self.orders_table.show_details)

        self.search_label = QLabel("Search by:")
        self.dropdownlist_search = QComboBox()
        categories = [column for index, column in enumerate(self.orders_table.column_names) if
                      index in range(4)]
        categories.insert(0, "All")
        self.dropdownlist_search.addItems(categories)

        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.search_orders)

        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.layout.addWidget(self.order_details_button, 0, 0)
        self.layout.addWidget(self.search_label, 1, 0)
        self.layout.addWidget(self.dropdownlist_search, 1, 1)
        self.layout.addWidget(self.search_field, 1, 2)
        self.layout.addWidget(self.orders_table, 2, 0, 1, 3)

        self.setLayout(self.layout)

    def search_orders(self):
        self.orders_table.refresh_orders(self.dropdownlist_search.currentText(), self.search_field.text())


class OrdersTable(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        self.column_names = view_column_names("orders_view")

        self.setColumnCount(len(self.column_names))
        self.setHorizontalHeaderLabels(self.column_names)
        self.itemSelectionChanged.connect(self.change_orders)
        self.itemDoubleClicked.connect(self.show_details)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.refresh_orders(search_by="All", text="")
        self.change_orders()

        self.setSortingEnabled(True)
        self.resizeRowsToContents()
        self.horizontalHeader().sortIndicatorChanged.connect(self.resizeRowsToContents)

    def refresh_orders(self, search_by, text):
        self.resizeRowsToContents()
        not_paid = {}
        self.data = search_order((search_by, (text + "%",),))
        self.setRowCount(len(self.data))
        for row_id, row in enumerate(self.data):
            for column_id, cell in enumerate(row):
                if column_id != 3 or cell is not None:
                    self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
                else:
                    button = QPushButton("Already paid")
                    not_paid[row[0]] = button
                    button.clicked.connect(partial(self.order_paid, button, not_paid))
                    self.setCellWidget(row_id, column_id, button)

    def change_orders(self):
        items = self.selectedItems()
        self.row_data = [cell.text() for cell in items]

    @pyqtSlot()
    def show_details(self):
        if not self.row_data:
            return
        else:
            create_view_orders_items(self.row_data[0])
            self.order = OrderDetailsWindow(parent=self)
            width = 850
            height = 600
            self.order.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width,
                                   height)

    @pyqtSlot()
    def order_paid(self, button, not_paid):
        for id, but in not_paid.items():
            if button is but:
                update_order_paid((str(datetime.now())[:-7], id,))
                self.removeCellWidget(id - 1, 3)
                self.refresh_orders(search_by="All", text="")
                break


class OrderDetailsWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.setAutoFillBackground(True)

        self.order_details_table = OrderDetailsTable()
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        header = self.order_details_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.close_button)
        self.layout.addWidget(self.order_details_table)
        self.setLayout(self.layout)
        self.show()


class OrderDetailsTable(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        self.orders_column_names = view_column_names("orders_items_view")
        self.orders_data = view_data("orders_items_view")
        self.single_order_view = QTableWidget()
        self.setColumnCount(len(self.orders_column_names))
        self.setHorizontalHeaderLabels(self.orders_column_names)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.refresh_order()

        self.setSortingEnabled(True)
        self.resizeRowsToContents()
        self.horizontalHeader().sortIndicatorChanged.connect(self.resizeRowsToContents)

    def refresh_order(self):
        self.orders_data = view_data("orders_items_view")
        self.setRowCount(len(self.orders_data))
        for row_id, row in enumerate(self.orders_data):
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
