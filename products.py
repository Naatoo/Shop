import psycopg2

from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWidgets import QDoubleSpinBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets

from queries import view_column_names, view_data


def insert_product(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    INSERT INTO products
    ("Name",
     "Quantity",
     "Selling price",
     "Category")
    VALUES
        (%s, %s, %s, %s)'''
    cursor.execute(sql, data)

    connection.commit()
    connection.close()


def delete_product(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    DELETE FROM products
    WHERE "ID" =%s
    '''
    cursor.execute(sql, (id,))

    connection.commit()
    connection.close()


def update_product(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    UPDATE products
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


def search_product(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    if data[0] == "All":
        sql = '''
        SELECT *
        FROM products
        WHERE
            CAST("ID" AS TEXT) LIKE %s
            OR "Name" ILIKE %s
            OR "Category" ILIKE %s
        ORDER BY "ID"
        '''
        cursor.execute(sql, tuple([text for text in data[1] for column in range(3)]))
    else:
        if data[0] == "Id":
            sql = '''
            SELECT *
            FROM products
            WHERE CAST("ID" AS TEXT) ILIKE %s
            ORDER BY "ID"
            '''
        elif data[0] == "Name":
            sql = '''
            SELECT *
            FROM products
            WHERE "Name" ILIKE %s
            ORDER BY "ID"
            '''
        elif data[0] == "Category":
            sql = '''
            SELECT *
            FROM products
            WHERE "Category" ILIKE %s
            ORDER BY "ID"
            '''
        cursor.execute(sql, data[1])

    rows = cursor.fetchall()
    connection.close()
    return rows


class ProductsWidgetTab(QTabWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QGridLayout(self)

        self.data = view_data("products")

        self.add_button = QPushButton("Add new product", self)
        self.add_button.setToolTip("Add an item which is not in the list yet")
        self.add_button.clicked.connect(self.add_item)

        self.update_button = QPushButton("Update product", self)
        self.update_button.setToolTip("Update selected product")
        self.update_button.clicked.connect(self.update_item)

        self.delete_button = QPushButton("Delete product", self)
        self.delete_button.setToolTip("Delete selected product")
        self.delete_button.clicked.connect(self.delete_item)

        self.products_table = ProductsTable(parent=self)

        self.search_label = QLabel("Search by:")
        self.dropdownlist_search = QComboBox()
        categories = [column for index, column in enumerate(self.products_table.products_column_names) if
                      index in (0, 1, 4)]
        categories.insert(0, "All")
        self.dropdownlist_search.addItems(categories)

        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.search_products)

        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.add_button, 0, 0)
        self.layout.addWidget(self.delete_button, 0, 1)
        self.layout.addWidget(self.update_button, 0, 2)
        self.layout.addWidget(self.search_label, 1, 0)
        self.layout.addWidget(self.dropdownlist_search, 1, 1)
        self.layout.addWidget(self.search_field, 1, 2)
        self.layout.addWidget(self.products_table, 2, 0, 1, 3)
        self.setLayout(self.layout)

    def search_products(self):
        self.products_table.refresh_products(self.dropdownlist_search.currentText(), self.search_field.text())

    @pyqtSlot()
    def add_item(self):
        self.item = NewItem(parent=self)
        width = 400
        height = 300
        self.item.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width, height)

    @pyqtSlot()
    def delete_item(self):
        if self.products_table.currentRow() < 0:
            return
        buttonReply = QMessageBox.question(self, 'Confirmation',
                                           "Do you want to remove " + self.products_table.row_data[1],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            return
        else:
            delete_product(self.products_table.row_data[0])
            self.search_products()

    @pyqtSlot()
    def update_item(self):
        if self.products_table.currentRow() < 0:
            return
        self.update_item = UpdateItem(self)
        width = 400
        height = 300
        self.update_item.setGeometry(int(self.width() / 2 - width / 2), int(self.height() / 2 - height / 2), width,
                                     height)


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

        self.refresh_products(search_by="All", text="")

        self.setSortingEnabled(True)
        self.resizeRowsToContents()
        self.horizontalHeader().sortIndicatorChanged.connect(self.resizeRowsToContents)

    def change_products(self):
        items = self.selectedItems()
        self.row_data = [cell.text() for cell in items]

    def refresh_products(self, search_by, text):
        self.data = search_product((search_by, (text + "%",),))
        self.setRowCount(len(self.data))
        for row_id, row in enumerate(self.data):
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))


class NewItem(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.data = view_data("products")
        self.setAutoFillBackground(True)
        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems(set([row[1] for row in self.data]))
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
        self.category_input.addItems(set([row[4] for row in self.data]))
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
        self.name_input.setCurrentIndex(0)
        self.quantity_input.setValue(1)
        self.price_sell_input.setValue(100.00)
        self.category_input.setCurrentIndex(0)

    @pyqtSlot()
    def add(self):
        self.data = view_data("products")
        if len(self.name_input_edit.text()) > 40 or self.name_input_edit.text() in [row[1] for row in self.data]:
            return
        if self.price_sell_input.text() == "0,00":
            return
        if len(self.category_input_edit.text()) != 3 or self.category_input_edit.text().isupper() is not True:
            return
        try:
            int(self.quantity_input.text())
            price = self.price_sell_input.text()
            price = price.replace(",", ".")
            float(price.replace(",", "."))
        except ValueError:
            return
        price = self.price_sell_input.text()
        if "," in price:
            price = price.replace(",", ".")
        insert_product(
            [self.name_input_edit.text(), self.quantity_input.text(), price, self.category_input_edit.text()])
        self.close()
        self.parent().search_products()


class UpdateItem(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.data = view_data("products")
        self.setAutoFillBackground(True)

        self.layout = QGridLayout()
        self.layout.setRowStretch(1, 6)
        self.layout.setColumnStretch(1, 2)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems(set([row[1] for row in self.data]))
        self.name_input_edit = QLineEdit()
        self.name_input.setLineEdit(self.name_input_edit)

        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_input, 1, 1)

        self.quantity_label = QLabel("Quantity")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(100000)
        self.layout.addWidget(self.quantity_label, 2, 0)
        self.layout.addWidget(self.quantity_input, 2, 1)

        self.price_sell_label = QLabel("Selling price")
        self.price_sell_input = QDoubleSpinBox()
        self.price_sell_input.setMaximum(100000)
        self.layout.addWidget(self.price_sell_label, 3, 0)
        self.layout.addWidget(self.price_sell_input, 3, 1)

        self.category_label = QLabel("Category")
        self.category_input = QComboBox()
        self.category_input.addItems(set([row[4] for row in self.data]))
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

        self.reset_to_default()
        self.show()

    @pyqtSlot()
    def reset_to_default(self):
        row = self.data[self.parent().products_table.currentRow()]
        self.name_input.setCurrentText(row[1])
        self.quantity_input.setValue(int(row[2]))
        self.price_sell_input.setValue(int(row[3]))
        self.category_input.setCurrentText(row[4])

    @pyqtSlot()
    def update(self):
        price = self.price_sell_input.text()
        if "," in price:
            price = price.replace(",", ".")
        update_product([self.name_input_edit.text(), self.quantity_input.text(), price, self.category_input_edit.text(),
                        self.parent().products_table.currentRow() + 1])
        self.close()
        self.parent().search_products()
