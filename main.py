
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

from screens.home import HomeScreen
from screens.add_alarm import AddAlarm
from services.alarm_manager import AlarmManager


class SmartWakeApp(App):
    def build(self):
        self.title = "SmartWake"

        Window.clearcolor = (0.06, 0.09, 0.15, 1)

        self.alarm_manager = AlarmManager()

        # Memuat suara alarm
        self.alarm_sound = SoundLoader.load("sounds/alarm.wav")

        if self.alarm_sound:
            self.alarm_sound.loop = True
        else:
            print("File suara alarm tidak ditemukan!")

        self.home = HomeScreen(self)
        self.add_alarm_screen = AddAlarm(self)

        Clock.schedule_interval(self.check_alarms, 1)

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

    def check_alarms(self, dt):
        ringing_alarms = self.alarm_manager.check_alarms()

        for alarm_time in ringing_alarms:
            self.show_alarm_popup(alarm_time)

    def show_alarm_popup(self, alarm_time):
        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        message = Label(
            text=f"ALARM BERBUNYI!\nWaktu: {alarm_time}",
            font_size="22sp",
            bold=True
        )

        stop_button = Button(
            text="MATIKAN ALARM",
            size_hint_y=None,
            height=50
        )

        content.add_widget(message)
        content.add_widget(stop_button)

        popup = Popup(
            title="SMARTWAKE",
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False
        )

        def stop_alarm(instance):
            if self.alarm_sound:
                self.alarm_sound.stop()

            popup.dismiss()

        stop_button.bind(on_press=stop_alarm)

        if self.alarm_sound:
            self.alarm_sound.play()

        popup.open()


if __name__ == "__main__":
    SmartWakeApp().run()
