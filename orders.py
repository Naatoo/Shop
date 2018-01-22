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


def delete_order(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DELETE FROM ordered_position WHERE "ID_ord"=%s;'''
    cursor.execute(sql, (id,))

    sql = '''DELETE FROM orders WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))

    connection.commit()
    connection.close()


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

