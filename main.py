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
    prop_label : QLabel
    treeWidget : QTreeWidget
    def __init__(self):
        super().__init__()
        loadUi(PATH + "load.ui", self)
        self.treeWidget.itemClicked.connect(self.handle_item_double_click)
        self.init_timer()
        self.load_data()
        self.selected_task = None
        print(self.get_childs("1"))
    
    def init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def load_data(self):
        all_data = json_file.read_data()
        for item_key, item_data in all_data.items():
            if item_data["top-level"] and item_data["display"]:
                item = CustomTreeItem([item_data["name"]], item_key)
                self.treeWidget.insertTopLevelItems(self.treeWidget.topLevelItemCount(), [item])
                self.load_childs(item, item_data["childs"])
    
    def load_childs(self, item, childs):
        all_data = json_file.read_data()
        for child_key in childs:
            if all_data[child_key]["display"]:
                sub_item = CustomTreeItem([all_data[child_key]["name"]], child_key)
                item.addChild(sub_item)
                self.load_childs(sub_item, all_data[child_key]["childs"])

    def handle_item_double_click(self, item : CustomTreeItem, column):
        self.selected_task = item
        self.prop_label.setText(item.text(0))
        self.update_time(0)

    def update_time(self, added_time = 1):
        if self.selected_task is None:
            return
        key = self.selected_task.key
        data = json_file.read_data()
        timestamps = data[key]["timestamps"]
        if not timestamps.get(get_hour_timestamp(), False):
            timestamps[get_hour_timestamp()] = 0
        timestamps[get_hour_timestamp()] += added_time
        json_file.save_data(data)
        sum_of_times = 0
        for child_key in self.get_childs(key) + [key]: # loop over the selected item and its childs
            timestamps = data[child_key]["timestamps"]
            today_only_times_per_child = get_timestamps_inrange_from_today(timestamps.keys(), 0, 0)
            today_times_value_per_child = [timestamps[timestamp] for timestamp in today_only_times_per_child]
            sum_of_times += sum(today_times_value_per_child)
        
        h,m,s = seconds2hours_minuits_seconds(sum_of_times)
        self.time_label.setText(f"{h:02}:{m:02}:{s:02}")
    
    def get_childs(self, key):
        children = []
        data = json_file.read_data()
        if key in data:
            for child_key in data[key]["childs"]:
                children.append(child_key)
                children.extend(self.get_childs(child_key))
        return children

if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    ui.show()
    app.exec_()