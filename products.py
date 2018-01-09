from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QSpinBox, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QDoubleSpinBox, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

import psycopg2


def create_table(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS products''')
    cursor.execute('''CREATE TABLE products
                   (Pozycja_towaru INT PRIMARY KEY NOT NULL,
                     Nazwa CHAR(40) NOT NULL,
                     Ilość_w_magazynie INT NULL,
                     Cena_sprzedaży FLOAT NOT NULL,
                     kat CHAR(3) NOT NULL);''')
    # INDEX `fk_kat_idx` (`id_kat` ASC),\
    # INDEX `fk_mag_idx` (`id_mag` ASC),\
    # CONSTRAINT `fk_kat`\
    #   FOREIGN KEY (`id_kat`)\
    #   REFERENCES `sklep_internetowy`.`Kategorie` (`Id_kat`)\
    # CONSTRAINT `fk_mag`\
    #   FOREIGN KEY (`id_mag`)\
    #   REFERENCES `sklep_internetowy`.`Magazyn` (`id_Magazynu`)"
    connection.commit()
    for row in data:
        sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s)"
        data = row
        cursor.execute(sql, data)
        connection.commit()
    connection.close()


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
    sql = "DELETE FROM products WHERE Pozycja_towaru=%s;"
    cursor.execute(sql, (id,))
    connection.commit()
    connection.close()


def view(table_name):
    data = (table_name,)
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = "SELECT * FROM %s" % table_name
    cursor.execute(sql)
    rows = cursor.fetchall()

    sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s"
    cursor.execute(sql, data)
    column_names = cursor.fetchall()
    column_names_final = [tup[0] for tup in column_names]

    connection.close()
    return column_names_final, rows


data = ((1, 'Telefon_Samsung_S8', 4, 2900, "MOB"), (2, 'Telefon LG G6/32GB/Szary', 12, 2300, "MOB"),
        (3, 'Gra Fifa18', 32, 219, "GAM"))


class NewItemWidget(QWidget):
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

        self.id_label = QLabel("Product id")
        self.id_input = QSpinBox()
        self.id_input.setMaximum(100000)

        # Default id value
        indexes = [number[0] for number in data[1]]
        indexes_sorted = sorted(indexes)
        for id in indexes_sorted:
            if id + 1 not in indexes:
                self.id_input.setValue(id + 1)
                break

        self.layout.addWidget(self.id_label, 0, 0)
        self.layout.addWidget(self.id_input, 0, 1)

        self.name_label = QLabel("Name")
        self.name_input = QComboBox()
        self.name_input.addItems([item_id[1] for item_id in data[1]])
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
        self.category_input.addItems([item_id[4] for item_id in data[1]])
        self.category_input_edit = QLineEdit()
        self.category_input.setLineEdit(self.category_input_edit)
        self.layout.addWidget(self.category_label, 4, 0)
        self.layout.addWidget(self.category_input, 4, 1)

        self.add_item_button = QPushButton("Add item")
        self.layout.addWidget(self.add_item_button, 5, 0)

        self.add_item_button.clicked.connect(self.add)

        self.cancel_button = QPushButton("Cancel")

        self.groupbox.setLayout(self.layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.groupbox)
        self.setLayout(windowLayout)
        self.show()

    @pyqtSlot()
    def add(self):
        price = self.price_sell_input.text()
        if "," in price:
            price = price.replace(",", ".")
        sql_insert([self.id_input.text(), self.name_input_edit.text(),
                    self.quantity_input.text(), price, self.category_input_edit.text()])
        self.close()
