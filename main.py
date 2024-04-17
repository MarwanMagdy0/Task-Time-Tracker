from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt5.QtCore import QTimer, Qt, QThread
from PyQt5.uic import loadUi
from PIL import Image
import pystray
from utiles import *
from pop_up import PopupUI

class TrayThread(QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    
    def on_left_click(self):
        """
        this method show the screen of the program
        """
        self.ui.show()
        self.ui.activateWindow()
    
    def on_right_click(self):
        """
        this method closes the entire program
        """
        self.ui.close()

    def run(self):
        image = Image.open(PATH + "logo.png")

        # Create a menu item with the left-click event handler
        menu = (pystray.MenuItem("show", self.on_left_click, default = True),
                pystray.MenuItem("exit", self.on_right_click))

        # Create the tray icon with the menu
        icon = pystray.Icon("tray_icon", image, "Tray Icon", menu)

        # Run the tray icon
        icon.run()

class CustomTreeItem(QTreeWidgetItem):
    def __init__(self, item, key):
        super().__init__(item)
        self.key = key

class UI(QMainWindow):
    time_label : QLabel
    prop_label : QLabel
    treeWidget : QTreeWidget
    add_task_button        : QPushButton
    add_subtask_button     : QPushButton
    remove_selected_button : QPushButton
    minus_button           : QPushButton
    plus_button            : QPushButton
    play_pause_button      : QPushButton
    def __init__(self):
        super().__init__()
        loadUi(PATH + "load.ui", self)
        self.init_widgets()
        self.init_timers()
        self.load_data()
        self.pop_up = PopupUI()
        self.pop_up.time_finished.connect(self.time_finished_method)
        self.selected_task = None
        self.tray_thread = TrayThread(self)
        self.tray_thread.start()

    def init_widgets(self):
        self.treeWidget.itemClicked.connect(self.handle_item_click)
        self.treeWidget.itemChanged.connect(self.on_item_changed)
        self.add_task_button.clicked.connect(self.add_task_method)
        self.add_subtask_button.clicked.connect(self.add_sub_task_method)
        self.remove_selected_button.clicked.connect(self.remove_selected_method)
        self.play_pause_button.clicked.connect(self.play_pause_method)
        self.minus_button.clicked.connect(lambda: self.edit_time_method(-60))
        self.plus_button.clicked.connect(lambda: self.edit_time_method(60))

    def init_timers(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)

        self.evert20minuit_timer = QTimer()
        self.evert20minuit_timer.setInterval(40000)
        self.evert20minuit_timer.timeout.connect(self.check_user_status)
        self.evert20minuit_timer.start()

    def load_data(self):
        all_data = json_file.read_data()
        for item_key, item_data in all_data.items():
            if item_data["top-level"] and item_data["display"]:
                item = CustomTreeItem([item_data["name"]], item_key)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.treeWidget.insertTopLevelItems(self.treeWidget.topLevelItemCount(), [item])
                self.load_childs(item, item_data["childs"])
    
    def load_childs(self, item, childs):
        all_data = json_file.read_data()
        for child_key in childs:
            if all_data[child_key]["display"]:
                sub_item = CustomTreeItem([all_data[child_key]["name"]], child_key)
                sub_item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.addChild(sub_item)
                self.load_childs(sub_item, all_data[child_key]["childs"])

    def handle_item_click(self, item : CustomTreeItem, column):
        self.selected_task = item
        self.prop_label.setText(item.text(0))
        self.update_time(0)
    
    def on_item_changed(self, item : CustomTreeItem, column):
        data = json_file.read_data()
        data[item.key]["name"] = item.text(0)
        json_file.save_data(data)

    def update_time(self, added_time = 1):
        if self.selected_task is None:
            return
        key = self.selected_task.key
        data = json_file.read_data()
        if key not in data.keys():
            return
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
    
    def check_user_status(self):
        print("checked")
        if self.selected_task is None:
            return
        if self.play_pause_button.text() == ">":
            self.pop_up.are_you_working_method()
        else:
            self.pop_up.are_you_still_working_method()
        self.pop_up.show()
    
    def time_finished_method(self):
        if self.selected_task is None:
            return
        key = self.selected_task.key
        data = json_file.read_data()
        if key not in data.keys():
            return
        timestamps = data[key]["timestamps"]
        if not timestamps.get(get_hour_timestamp(), False):
            timestamps[get_hour_timestamp()] = 0
        
        if self.play_pause_button.text() == "||":
            # if he is not working 10 min will be removed from his working time
            timestamps[get_hour_timestamp()] -= 10 * 60

        json_file.save_data(data)
    
    def get_childs(self, key):
        children = []
        data = json_file.read_data()
        if key in data:
            for child_key in data[key]["childs"]:
                children.append(child_key)
                children.extend(self.get_childs(child_key))
        return children
    
    def play_pause_method(self):
        if self.play_pause_button.text() == ">":
            self.play_pause_button.setText("||")
            self.timer.start()
        
        else:
            self.play_pause_button.setText(">")
            self.timer.stop()
        
    def edit_time_method(self, delta_time):
        if self.selected_task is None:
            return
        key = self.selected_task.key
        data = json_file.read_data()
        if key not in data.keys():
            return
        timestamps = data[key]["timestamps"]
        if not timestamps.get(get_hour_timestamp(), False):
            timestamps[get_hour_timestamp()] = 0
        timestamps[get_hour_timestamp()] += delta_time
        json_file.save_data(data)
        self.update_time(0)

    def add_task_method(self):
        data = json_file.read_data()
        key = len(data)
        item = CustomTreeItem([f"task_{key}"], f"{key}")
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.treeWidget.insertTopLevelItems(self.treeWidget.topLevelItemCount(), [item])
        data[f"{key}"] ={"name": f"task_{key}", "timestamps": {}, "display": True, "top-level": True, "childs": []}
        json_file.save_data(data)
    
    def add_sub_task_method(self):
        if self.selected_task is None:
            return
        data = json_file.read_data()
        key = len(data)
        sub_item = CustomTreeItem([f"task_{key}"], f"{key}")
        sub_item.setFlags(sub_item.flags() | Qt.ItemIsEditable)
        self.selected_task.addChild(sub_item)
        data[f"{key}"] ={"name": f"task_{key}", "timestamps": {}, "display": True, "top-level": False, "childs": []}
        data[f"{self.selected_task.key}"]["childs"].append(f"{key}")
        json_file.save_data(data)
    
    def remove_selected_method(self):
        if self.selected_task is None:
            return
        data = json_file.read_data()

        # to remove item from the ui and its key and remove its key from its parent
        parent = self.selected_task.parent()
        if parent is not None:
            parent.removeChild(self.selected_task)
            parent_key = parent.key
            print(data[parent_key]["childs"])
            data[parent_key]["childs"].remove(self.selected_task.key)
        else: # if it is a top level item
            index = self.treeWidget.indexOfTopLevelItem(self.selected_task)
            self.treeWidget.takeTopLevelItem(index)
        data.pop(self.selected_task.key)

        # remove all childs to this item
        for child_key in self.get_childs(self.selected_task.key):
            data.pop(child_key)

        json_file.save_data(data)
        self.selected_task = parent
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        if event.spontaneous():
            self.hide()
            event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    app.exec_()