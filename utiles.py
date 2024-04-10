import json
import os
import datetime
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

def seconds2hours_minuits_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)


json_file = HandleJsonFiles(PATH + "times.json")
def get_hour_timestamp():
    now = datetime.datetime.now()
    # print(now.year, now.month, now.day, now.hour)
    zero_minuit = datetime.datetime(now.year, now.month, now.day, now.hour)
    return str(int(zero_minuit.timestamp()))

def get_timestamps_inrange_from_today(list_of_timestamps, days_before, days_after):
    now = datetime.datetime.now()
    today_start = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    today_end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

    # Calculate start and end date range
    start_range = today_start - datetime.timedelta(days=days_before)
    end_range = today_end + datetime.timedelta(days=days_after)

    timestamps_in_range = []
    for timestamp in list_of_timestamps:
        if start_range <= datetime.datetime.fromtimestamp(int(timestamp)) <= end_range:
            timestamps_in_range.append(timestamp)

    return timestamps_in_range


if __name__ == "__main__":
    print(get_hour_timestamp())
    print(get_timestamps_inrange_from_today(["1712739600"], 0, 0))
