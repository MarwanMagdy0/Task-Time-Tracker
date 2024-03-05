import json
import os

PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

class HandleJsonFiles:
    def __init__(self, file_path, default = None):
        self.file_path = os.path.normpath(file_path)
        if not os.path.isfile(self.file_path):
            if default is not None:
                self.save_data(default)
            else:
                self.save_data({})


    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
        
    def __getitem__(self, key):
        data = self.read_data()
        return data[key]
    
    def __setitem__(self, key: str, value) -> None:
        data = self.read_data()
        data[key] = value
        self.save_data(data)
        
    def keys(self):
        data = self.read_data()
        return data.keys()


json_file = HandleJsonFiles(PATH + "times.json")