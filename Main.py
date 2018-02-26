import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel, QComboBox, QStyleFactory
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QHBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSlot, QObject

from datetime import datetime

from products import ProductsWidgetTab
from orders import OrdersWidgetTab
from views import create_view_orders
from customers import CustomersWidgetTab
from vendors import VendorsWidgetTab
from new_order import NewOrderWidgetTab


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Shop"
        self.left = 100
        self.top = 100
        self.width = 1024
        self.height = 768

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage("v0.3")

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        self.show()


class MainWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab_new_order = NewOrderWidgetTab()
        self.tab_products = ProductsWidgetTab()
        self.tab_orders = OrdersWidgetTab()
        self.tab_customers = CustomersWidgetTab()
        self.tab_vendors = VendorsWidgetTab()

        self.tabs.addTab(self.tab_new_order, "New Order")
        self.tabs.addTab(self.tab_products, "Products")
        self.tabs.addTab(self.tab_orders, "Orders")
        self.tabs.addTab(self.tab_customers, "Customers")
        self.tabs.addTab(self.tab_vendors, "Vendors")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        create_view_orders()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    shop = App()
    sys.exit(app.exec_())
