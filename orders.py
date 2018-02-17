import psycopg2

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSlot

from datetime import datetime
from functools import partial

from queries import view_data, view_column_names
from views import create_view_orders_items


class OrderQueries:

    @staticmethod
    def delete_order(id):
        connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
        cursor = connection.cursor()

        sql = '''DELETE FROM ordered_position WHERE "ID_ord"=%s;'''
        cursor.execute(sql, (id,))

        sql = '''DELETE FROM orders WHERE "ID"=%s;'''
        cursor.execute(sql, (id,))

        connection.commit()
        connection.close()

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def insert_order(data):
        connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
        cursor = connection.cursor()
        sql = '''INSERT INTO orders ("Ordered", "Paid", "ID_cust")
                 VALUES (%s, %s, %s)'''
        cursor.execute(sql, data)
        connection.commit()
        connection.close()

    @staticmethod
    def update_order(data):
        connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
        cursor = connection.cursor()
        sql = '''UPDATE orders
                 SET "Paid"=%s
                 WHERE "ID"=%s'''
        cursor.execute(sql, data)
        connection.commit()
        connection.close()


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
        self.refresh_orders()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.change_orders()

    def refresh_orders(self):
        not_paid = {}
        self.data = view_data("orders_view")
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
    def delete_order(self):
        if self.currentRow() < 0:
            return
        OrderQueries.delete_order(self.row_data[0])
        self.refresh_orders()

    @pyqtSlot()
    def show_details(self):
        if not self.row_data:
            return
        else:
            create_view_orders_items(self.row_data[0])
            self.order = OrderDetailsWindow(parent=self)
            width = 850
            height = 600
            self.order.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    @pyqtSlot()
    def order_paid(self, button, not_paid):
        for id, but in not_paid.items():
            if button is but:
                OrderQueries.update_order((str(datetime.now())[:-7], id,))
                self.removeCellWidget(id - 1, 3)
                self.refresh_orders()
                break


class OrderDetailsWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.setAutoFillBackground(True)

        self.order_details_table = OrderDetailsTable()
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

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

    def refresh_order(self):
        self.orders_data = view_data("orders_items_view")
        self.setRowCount(len(self.orders_data))
        for row_id, row in enumerate(self.orders_data):
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
