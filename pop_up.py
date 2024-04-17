from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.uic import loadUi
import os
PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
class PopupUI(QMainWindow):
    submit : QPushButton
    message_label: QLabel
    timer_label : QLabel
    time_finished = pyqtSignal()
    def __init__(self):
        super().__init__()
        loadUi(PATH + "pop_up.ui", self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.submit.clicked.connect(self.submit_method)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_method)
        self.time_variable = 30
        
    def are_you_still_working_method(self):
        self.time_variable = 30
        self.timer.start()
        self.message_label.setText("Are you still working?\n if not you will lose 10min")
        self.timer_label.setText(f"{self.time_variable}")
    
    def are_you_working_method(self):
        self.message_label.setText("Are you working?")
        self.timer.start()
        self.time_variable = 30
        self.timer_label.setText(f"{self.time_variable}")

    def timer_method(self):
        self.time_variable -= 1
        self.timer_label.setText(f"{self.time_variable}")
        if self.time_variable == 0:
            self.time_finished.emit()
            self.timer.stop()
            self.hide()
    
    def submit_method(self):
        self.timer.stop()
        if __name__ != "__main__":
            self.hide()
        else: # for testing
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    ui = PopupUI()
    ui.show()
    app.exec_()