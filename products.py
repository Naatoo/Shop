from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QDoubleSpinBox, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets

import psycopg2


def sql_insert(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def delete(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''DELETE FROM products WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))
    connection.commit()
    connection.close()


def sql_update(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''UPDATE products
             SET
             "Name"=%s,
             "Quantity"=%s,
             "Selling price"=%s,
             "Category"=%s
             WHERE "ID"=%s
             '''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def view(table_name):
    data = (table_name,)
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''SELECT * FROM %s ORDER BY "ID"''' % table_name
    cursor.execute(sql)
    rows = cursor.fetchall()

    sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s"
    cursor.execute(sql, data)
    column_names = cursor.fetchall()
    column_names_final = [tup[0].title() for tup in column_names]

    connection.close()
    return column_names_final, rows


class NewItem(QWidget):
    def __init__(self, data):
        super(QWidget, self).__init__()

        self.title = "Add new item"
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

        self.id_label = QLabel("Product id")
        self.id_input = QSpinBox()
        self.id_input.setMaximum(100000)

        # Default values
        self.indexes = [number[0] for number in data[1]]
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
        self.name_input.addItems(set([item_id[1] for item_id in data[1]]))
        self.name_input_edit = QLineEdit()

        self.name_input.setLineEdit(self.name_input_edit)
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.quantity_label = QLabel("Quantity")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(100000)
        self.quantity_input.setValue(1)
        self.layout.addWidget(self.quantity_label, 2, 0)
        self.layout.addWidget(self.quantity_input, 2, 1)

        self.price_sell_label = QLabel("Selling price")
        self.price_sell_input = QDoubleSpinBox()
        self.price_sell_input.setMaximum(100000)
        self.price_sell_input.setValue(100.00)
        self.layout.addWidget(self.price_sell_label, 3, 0)
        self.layout.addWidget(self.price_sell_input, 3, 1)

        self.category_label = QLabel("Category")
        self.category_input = QComboBox()
        self.category_input.addItems(set([item_id[4] for item_id in data[1]]))
        self.category_input_edit = QLineEdit()
        self.category_input.setLineEdit(self.category_input_edit)
        self.layout.addWidget(self.category_label, 4, 0)
        self.layout.addWidget(self.category_input, 4, 1)

        self.add_item_button = QPushButton("Add item")
        self.layout.addWidget(self.add_item_button, 5, 0)
        self.add_item_button.clicked.connect(self.add)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, 5, 1)
        self.cancel_button.clicked.connect(self.close)

        self.reset_button = QPushButton("Reset to default")
        self.layout.addWidget(self.reset_button, 5, 2)
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
        self.quantity_input.setValue(1)
        self.price_sell_input.setValue(100.00)
        self.category_input.setCurrentIndex(0)

    @pyqtSlot()
    def add(self):
        data = view("products")[1]
        if len(self.name_input_edit.text()) > 40 or self.name_input_edit.text() in [row[1] for row in data]:
            return
        if self.id_input.text() in [str(row[0]) for row in data] or self.id_input.text() == 0:
            return
        if self.price_sell_input.text() == "0,00":
            return
        if len(self.category_input_edit.text()) != 3 or self.category_input_edit.text().isupper() is not True:
            return
        try:
            int(self.id_input.text())
            int(self.quantity_input.text())
            price = self.price_sell_input.text()
            price = price.replace(",", ".")
            float(price.replace(",", "."))
        except ValueError:
            return
        price = self.price_sell_input.text()
        if "," in price:
            price = price.replace(",", ".")
        sql_insert([self.id_input.text(), self.name_input_edit.text(),
                    self.quantity_input.text(), price, self.category_input_edit.text()])
        self.close()


class UpdateItem(QWidget):
    def __init__(self, data, row_data):
        super(QWidget, self).__init__()

        self.data = data
        self.row_data = row_data

        self.title = "Update product"
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

        self.id = row_data
        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems(set([item_id[1] for item_id in data[1]]))
        self.name_input_edit = QLineEdit()
        self.name_input.setLineEdit(self.name_input_edit)

        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.quantity_label = QLabel("Quantity")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(100000)
        self.quantity_input.setValue(data[1][row_data][2])
        self.layout.addWidget(self.quantity_label, 2, 0)
        self.layout.addWidget(self.quantity_input, 2, 1)

        self.price_sell_label = QLabel("Selling price")
        self.price_sell_input = QDoubleSpinBox()
        self.price_sell_input.setMaximum(100000)
        self.price_sell_input.setValue(data[1][row_data][3])
        self.layout.addWidget(self.price_sell_label, 3, 0)
        self.layout.addWidget(self.price_sell_input, 3, 1)

        self.category_label = QLabel("Category")
        self.category_input = QComboBox()
        self.category_input.addItems(set([item_id[4] for item_id in data[1]]))
        self.category_input_edit = QLineEdit()
        self.category_input.setLineEdit(self.category_input_edit)

        self.layout.addWidget(self.category_label, 4, 0)
        self.layout.addWidget(self.category_input, 4, 1)

        self.update_item_button = QPushButton("Update item")
        self.layout.addWidget(self.update_item_button, 5, 0)

        self.update_item_button.clicked.connect(self.update)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, 5, 1)
        self.cancel_button.clicked.connect(self.close)

        self.reset_button = QPushButton("Reset to default")
        self.layout.addWidget(self.reset_button, 5, 2)
        self.reset_button.clicked.connect(self.reset_to_default)

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    @pyqtSlot()
    def reset_to_default(self):
        self.name_input.setCurrentIndex(1)
        self.quantity_input.setValue(self.data[1][self.row_data][2])
        self.price_sell_input.setValue(self.data[1][self.row_data][3])
        self.category_input.setCurrentIndex(1)

    @pyqtSlot()
    def update(self):
        price = self.price_sell_input.text()
        if "," in price:
            price = price.replace(",", ".")
        sql_update([self.name_input.text(),
                    self.quantity_input.text(), price, self.category_input.text(), self.id])
        self.close()


class ProductsTemp(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        self.data = view("temp_orders_items_view")
        column_names = self.data[0]
        self.rows = self.data[1]

        self.repaint()
        self.setColumnCount(len(self.data[0]))
        self.setHorizontalHeaderLabels(column_names)
        self.move(0, 0)
        self.itemSelectionChanged.connect(self.change_products)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.refresh_products()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.change_products()


    def change_products(self):
        items = self.selectedItems()
        self.row_data_product = [cell.text() for cell in items]

    def refresh_products(self):
        self.rows = view("temp_orders_items_view")[1]
        self.setRowCount(len(self.rows) + 1)

        row_id = 0
        for row in self.rows:
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
            row_id += 1
        comboBox = QtWidgets.QComboBox()
        for name in [row[1] for row in view("products")[1]]:
            comboBox.addItem(name)
        self.setCellWidget(row_id, 1, comboBox)

