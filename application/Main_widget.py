from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from application.tabs.products import ProductsWidgetTab
from application.tabs.orders import OrdersWidgetTab
from application.tabs.customers import CustomersWidgetTab
from application.tabs.vendors import VendorsWidgetTab
from application.tabs.new_order import NewOrderWidgetTab


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



