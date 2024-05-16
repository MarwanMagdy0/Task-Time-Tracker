from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.uic import loadUi
import os
PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
class PopupUI(QMainWindow):
    yes_button : QPushButton
    no_button  : QPushButton
    message_label: QLabel
    timer_label : QLabel
    time_finished = pyqtSignal()
    yes_signal    = pyqtSignal()
    def __init__(self):
        super().__init__()
        loadUi(PATH + "pop_up.ui", self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.yes_button.clicked.connect(self.yes_method)
        self.no_button.clicked.connect(self.no_method)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_method)
        self.time_variable = 30
        self.center()
        
    def are_you_still_working_method(self, task_name = ""):
        self.time_variable = 30
        self.timer.start()
        self.message_label.setText(f"Are you still working on {task_name}?\n if not you will lose 10min")
        self.timer_label.setText(f"{self.time_variable}")
    
    def are_you_working_method(self, task_name=""):
        self.message_label.setText(f"Are you working on {task_name}")
        self.timer.start()
        self.time_variable = 30
        self.timer_label.setText(f"{self.time_variable}")
    
    def no_method(self):
        self.time_finished.emit()
        self.timer.stop()
        if __name__ != "__main__":
            self.hide()
        else: # for testing
            self.close()

    def timer_method(self):
        self.time_variable -= 1
        self.timer_label.setText(f"{self.time_variable}")
        if self.time_variable == 0:
            self.time_finished.emit()
            self.timer.stop()
            self.hide()
    
    def yes_method(self):
        self.timer.stop()
        if __name__ != "__main__":
            self.hide()
        else: # for testing
            self.close()
        self.yes_signal.emit()
    
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)


if __name__ == "__main__":
    app = QApplication([])
    ui = PopupUI()
    ui.show()
    app.exec_()
