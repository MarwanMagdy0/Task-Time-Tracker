from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from utiles import *

class CustomTreeItem(QTreeWidgetItem):
    def __init__(self, item, key):
        super().__init__(item)
        self.key = key

class UI(QMainWindow):
    time_label : QLabel
    treeWidget : QTreeWidget
    def __init__(self):
        super().__init__()
        loadUi(PATH + "load.ui", self)
        self.treeWidget.itemClicked.connect(self.handle_item_click)
        self.treeWidget.itemDoubleClicked.connect(self.handle_item_double_click)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.seconds2display = 61 * 60
        self.load_data()
    
    def load_data(self):
        all_data = json_file.read_data()
        for item_key, item_data in all_data.items():
            if item_data["top-level"]:
                item = CustomTreeItem([item_data["name"]], item_key)
                self.treeWidget.insertTopLevelItems(self.treeWidget.topLevelItemCount(), [item])
                self.load_childs(item, item_data["childs"])
    
    def load_childs(self, item, childs):
        print(childs)
        all_data = json_file.read_data()
        for child_key in childs:
            sub_item = CustomTreeItem([all_data[child_key]["name"]], child_key)
            item.addChild(sub_item)
            self.load_childs(sub_item, all_data[child_key]["childs"])

    def handle_item_double_click(self, item, column):
        print(item.key, "stop double clicking meeeee")
    
    def handle_item_click(self, item, column):
        pass

    def update_time(self):
        h,m,s = seconds2minuits_seconds(self.seconds2display)
        self.time_label.setText(f"{h:02}:{m:02}:{s:02}")
        self.seconds2display -= 1

if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    ui.show()
    app.exec_()