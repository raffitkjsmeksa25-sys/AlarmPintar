
class AlarmManager:
    def __init__(self):
        self.alarms = []

    def add_alarm(self, alarm_time):
        alarm = {
            "time": alarm_time,
            "active": True
        }

        self.alarms.append(alarm)

    def remove_alarm(self, index):
        if 0 <= index < len(self.alarms):
            self.alarms.pop(index)

    def toggle_alarm(self, index):
        if 0 <= index < len(self.alarms):
            self.alarms[index]["active"] = not self.alarms[index]["active"]

    def get_alarms(self):
        return self.alarms
