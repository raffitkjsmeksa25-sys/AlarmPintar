
from kivy.app import App
from kivy.core.window import Window

from screens.home import HomeScreen
from screens.add_alarm import AddAlarm
from services.alarm_manager import AlarmManager


class SmartWakeApp(App):
    def build(self):
        self.title = "SmartWake"

        Window.clearcolor = (0.06, 0.09, 0.15, 1)

        self.alarm_manager = AlarmManager()

        self.home = HomeScreen(self)
        self.add_alarm_screen = AddAlarm(self)

        return self.home

    def open_add_alarm(self):
        self.add_alarm_screen.open()

    def add_alarm(self, alarm_time):
        self.alarm_manager.add_alarm(alarm_time)
        self.home.refresh_alarm_list()

    def remove_alarm(self, index):
        self.alarm_manager.remove_alarm(index)
        self.home.refresh_alarm_list()

    def toggle_alarm(self, index):
        self.alarm_manager.toggle_alarm(index)
        self.home.refresh_alarm_list()


if __name__ == "__main__":
    SmartWakeApp().run()
