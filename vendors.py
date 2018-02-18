import psycopg2

from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSlot

from queries import view_data, view_column_names


def insert_vendor(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''INSERT INTO vendors
          ("Name", "City", "Street", "House number", "Zip code")
          VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


def delete_vendor(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DELETE FROM vendors WHERE "ID"=%s;'''
    cursor.execute(sql, (id,))

    connection.commit()
    connection.close()


def update_vendor(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = '''UPDATE vendors SET
            "Name"=%s,
            "City"=%s,
            "Street"=%s,
            "House number"=%s,
            "Zip code"=%s
             WHERE "ID"=%s'''
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


class VendorsTable(QTableWidget):
    def __init__(self):
        super(QTableWidget, self).__init__()

        self.column_names = view_column_names("vendors")

        self.setColumnCount(len(self.column_names))
        self.setHorizontalHeaderLabels(self.column_names)
        self.itemSelectionChanged.connect(self.change_vendors)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.refresh_vendors()

    def refresh_vendors(self):
        self.data = view_data("vendors")
        self.setRowCount(len(self.data))
        for row_id, row in enumerate(self.data):
            for column_id, cell in enumerate(row):
                self.setItem(row_id, column_id, QTableWidgetItem(str(cell)))

    def change_vendors(self):
        items = self.selectedItems()
        self.row_data = [cell.text() for cell in items]


class NewVendorWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.data = view_data("vendors")

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

        self.add_customer_button = QPushButton("Add Vendor")
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
        insert_vendor([self.name_input_edit.text(),
                    self.city_input_edit.text(), self.street_input_edit.text(),
                    self.house_input.text(), self.zipcode_input_edit.text()])
        self.close()
        self.parent().vendors_table.refresh_vendors()


class UpdateVendorWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.data = view_data("vendors")

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

        self.update_customer_button = QPushButton("Update Vendor")
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
        row = self.data[self.parent().vendors_table.currentRow()]
        self.name_input.setCurrentText(row[1])
        self.city_input.setCurrentText(row[2])
        self.street_input.setCurrentText(row[3])
        self.house_input.setText(row[4])
        self.zipcode_input.setCurrentText(row[5])

    @pyqtSlot()
    def update(self):
        update_vendor([self.name_input_edit.text(),
                    self.city_input_edit.text(), self.street_input_edit.text(),
                    self.house_input.text(), self.zipcode_input_edit.text(),
                    self.parent().vendors_table.currentRow() + 1])
        self.close()
        self.parent().vendors_table.refresh_vendors()
