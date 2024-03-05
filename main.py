from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("load.ui", self)

if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    ui.show()
    app.exec_()
        