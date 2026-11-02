
import json
import os
from datetime import datetime


class AlarmManager:
    def __init__(self):
        self.alarms = []

        self.file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "alarms.json"
        )

        self.load_alarms()

    def load_alarms(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    self.alarms = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.alarms = []

    def save_alarms(self):
        with open(self.file_path, "w") as file:
            json.dump(self.alarms, file, indent=4)

    def add_alarm(self, alarm_time):
        alarm = {
            "time": alarm_time,
            "active": True,
            "triggered_date": None
        }

        self.alarms.append(alarm)
        self.save_alarms()

    def remove_alarm(self, index):
        if 0 <= index < len(self.alarms):
            self.alarms.pop(index)
            self.save_alarms()

    def toggle_alarm(self, index):
        if 0 <= index < len(self.alarms):
            self.alarms[index]["active"] = not self.alarms[index]["active"]
            self.save_alarms()

    def get_alarms(self):
        return self.alarms

    def check_alarms(self):
        current_time = datetime.now()
        current_hour_minute = current_time.strftime("%H:%M")
        current_date = current_time.strftime("%Y-%m-%d")

        ringing_alarms = []

        for alarm in self.alarms:
            if (
                alarm["active"]
                and alarm["time"] == current_hour_minute
                and alarm["triggered_date"] != current_date
            ):
                alarm["triggered_date"] = current_date
                ringing_alarms.append(alarm["time"])

        if ringing_alarms:
            self.save_alarms()

        return ringing_alarms
