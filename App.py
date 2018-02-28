import sys

from PyQt5.QtWidgets import QApplication, QStyleFactory, QMainWindow

from Main_widget import MainWidget


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    shop = App()
    sys.exit(app.exec_())
