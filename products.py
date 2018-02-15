import psycopg2

from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QDoubleSpinBox, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets

from queries import view_column_names, view_data


def insert_product(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def delete_product(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''DELETE FROM products WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))
    connection.commit()
    connection.close()


def delete_from_current_order(name):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''DELETE FROM temp WHERE "Name"=%s;'''
    cursor.execute(sql, (name,))
    connection.commit()
    connection.close()


def give_name_to_select(name):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''SELECT "Name"
             FROM temp
             WHERE "ID" > (SELECT "ID"
                           FROM temp
                           WHERE "Name"=%s)'''
    cursor.execute(sql, (name,))
    name = cursor.fetchall()
    connection.commit()
    connection.close()
    return name[0]


def update_product(data):
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


# def view(table_name):
#     data = (table_name,)
#     connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
#     cursor = connection.cursor()
#
#     sql = '''SELECT * FROM %s ORDER BY "ID"''' % table_name
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#
#     sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s"
#     cursor.execute(sql, data)
#     column_names = cursor.fetchall()
#     column_names_final = [tup[0].title() for tup in column_names]
#
#     connection.close()
#     return column_names_final, rows


def temp_insert(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''INSERT INTO temp 
             ("Item ID", "Name", "Quantity", "Selling Price", "Category")
             VALUES 
             (%s, %s, %s, %s, %s)'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


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

        self.dropdownlist_category = QComboBox()
        self.data = view_data("products")
        categories = set([item_id[4] for item_id in self.data])
        categories.add("All products")
        self.dropdownlist_category.addItems(categories)

        self.products_table = ProductsTable(parent=self)
        self.products_table.itemDoubleClicked.connect(self.add)

        self.dropdownlist_category.activated.connect(self.products_table.select_category)

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.dropdownlist_category)
        self.layout.addWidget(self.products_table)
        self.setLayout(self.layout)
        self.show()

    def add(self):
        temp_insert(self.products_table.row_data)
        self.close()
        self.parent().refresh_products_in_order()


class ProductsTable(QTableWidget):
    def __init__(self, parent):
        super(QTableWidget, self).__init__(parent)

        self.products_column_names = view_column_names("products")
        self.setColumnCount(len(self.products_column_names))
        self.setHorizontalHeaderLabels(self.products_column_names)
        self.itemSelectionChanged.connect(self.change_products)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.refresh_products()

    # def refresh_products(self):
    #     self.products_data = view_data("products")
    #     self.setRowCount(len(self.products_data))
    #     for row_id, row in enumerate(self.products_data):
    #         for column_id, cell in enumerate(row):
    #             self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
    #
    # def change_products(self):
    #     items = self.selectedItems()
    #     self.row_data_products = [cell.text() for cell in items]

    def change_products(self):
        items = self.selectedItems()
        self.row_data = [cell.text() for cell in items]

    def refresh_products(self):
        self.rows = view_data("products")
        self.category = self.parent().dropdownlist_category.currentText()
        if self.category == "All products":
            self.setRowCount(len(self.rows))
        else:
            self.rows_table = [row[4] for row in self.rows].count(self.category)
            self.setRowCount(self.rows_table)
        row_id = 0
        for row in self.rows:
            if self.category == row[4] or self.category == "All products":
                for column_id, cell in enumerate(row):
                    self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
                row_id += 1

    @pyqtSlot()
    def select_category(self):
        self.refresh_products()


class ProductsTemp(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        column_names = view_column_names("temp")[1:]

        self.setColumnCount(len(column_names))
        self.setHorizontalHeaderLabels(column_names)
        self.itemSelectionChanged.connect(self.change_products)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.quantity_list = []
        self.price_list = []

        self.refresh_products()

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


class NewItem(QWidget):
    def __init__(self, data, parent):
        super(QWidget, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)

        self.default_values = []

        self.id_label = QLabel("Product id")
        self.id_input = QSpinBox()
        self.id_input.setMaximum(100000)

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

        self.setLayout(self.layout)
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
        data = view_data("products")
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
        insert_product([self.id_input.text(), self.name_input_edit.text(),
                        self.quantity_input.text(), price, self.category_input_edit.text()])
        self.close()
        self.parent().products_table.refresh_products()


class UpdateItem(QWidget):
    def __init__(self, data, row_data, parent=None):
        super(QWidget, self).__init__(parent)

        self.data = data
        self.row_data = row_data
        self.setAutoFillBackground(True)

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

        self.setLayout(self.layout)
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
        update_product([self.name_input_edit.text(),
                        self.quantity_input.text(), price, self.category_input_edit.text(), self.id])
        self.close()
        self.parent().products_table.refresh_products()



