import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.uic import loadUi
from utiles import PATH
class DragableCounterWindow(QDialog):
    escape_pressed = pyqtSignal()
    prop_label : QLabel
    time_label : QLabel
    minus_button      : QPushButton
    play_pause_button : QPushButton
    plus_button       : QPushButton

    def __init__(self):
        super().__init__()
        loadUi(PATH + "dragable_counter.ui", self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(1)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.FramelessWindowHint)
        self.go_top_right()  # Initial position

        # Set focus policy for buttons
        self.minus_button.setFocusPolicy(Qt.NoFocus)
        self.play_pause_button.setFocusPolicy(Qt.NoFocus)
        self.plus_button.setFocusPolicy(Qt.NoFocus)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.escape_pressed.emit()
        elif event.key() == Qt.Key_Plus:
            self.adjustOpacity(1)  # Increase opacity by 10%
        elif event.key() == Qt.Key_Minus:
            self.adjustOpacity(-1)  # Decrease opacity by 10%
        elif event.key() == Qt.Key_Up:
            self.move_to_top()
        elif event.key() == Qt.Key_Left:
            self.move_to_left()
        elif event.key() == Qt.Key_Right:
            self.move_to_right()
        elif event.key() == Qt.Key_Down:
            self.move_to_bottom()

    def adjustOpacity(self, delta):
        opacity = self.windowOpacity() + delta
        opacity = max(0.1, min(opacity, 1.0))  # Ensure opacity is between 0.1 and 1.0
        self.setWindowOpacity(opacity)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def go_top_right(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()

        # Set position to top-right corner
        window_width = self.width()
        self.move(screen_rect.width() - window_width, 0)

    def move_to_top(self):
        self.move(self.x(), 0)

    def move_to_left(self):
        self.move(0, self.y())

    def move_to_right(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        window_width = self.width()
        self.move(screen_rect.width() - window_width, self.y())

    def move_to_bottom(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        window_height = self.height()
        self.move(self.x(), screen_rect.height() - window_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragableCounterWindow()
    window.show()
    sys.exit(app.exec_())
