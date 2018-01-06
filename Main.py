import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLineEdit, QAction, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget
from PyQt5.QtWidgets import QLineEdit, QInputDialog
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QIcon
import backend


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Shop"
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage("v0.1")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)

        fileMenu.addAction(exitButton)

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.create_tab1()
        self.create_tab2()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def create_tab1(self):
        self.tab1.layout = QVBoxLayout(self)
        self.buttonclick = QPushButton("Button", self)
        self.buttonclick.setToolTip("First button")
        self.buttonclick.move(500, 80)
        self.buttonclick.clicked.connect(self.on_click)
        self.tab1.layout.addWidget(self.buttonclick)

        data = backend.view("products")
        column_names = data[0]
        rows = data[1]
        for a in rows:
            print(a)
        self.create_products_view(column_names, rows)
        self.tab1.layout.addWidget(self.goods_view)

        self.tab1.setLayout(self.tab1.layout)

    def create_products_view(self, column_names, rows):
        columns = 6
        self.goods_view = QTableWidget()
        self.goods_view.setRowCount(len(rows))
        self.goods_view.setColumnCount(columns)

        for row_id, row in enumerate(rows):
            for column_id, cell in enumerate(row):
                print(cell)
                self.goods_view.setItem(row_id, column_id, QTableWidgetItem(str(cell)))
        self.goods_view.setHorizontalHeaderLabels(column_names)
        self.goods_view.move(0, 0)

        # table selection change
        self.goods_view.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def create_tab2(self):
        self.tab2.layout = QVBoxLayout(self)
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        self.textbutton = QPushButton("Text", self)
        self.textbutton.move(20, 80)
        self.textbutton.clicked.connect(self.on_click_text_button)

        self.label = QLabel("First Label", self)
        self.label.move(200, 80)
        self.tab2.layout.addWidget(self.textbox)
        self.tab2.layout.addWidget(self.textbutton)
        self.tab2.layout.addWidget(self.label)
        self.tab2.setLayout(self.tab2.layout)

    @pyqtSlot()
    def on_click(self):
        print("clicked")

    @pyqtSlot()
    def on_click_text_button(self):
        textboxvalue = self.textbox.text()
        QMessageBox.question(self, "Message", "You typed: " + textboxvalue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shop = App()
    sys.exit(app.exec_())
