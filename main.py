
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

from screens.home import HomeScreen
from screens.add_alarm import AddAlarm
from screens.camera_screen import CameraScreen
from services.alarm_manager import AlarmManager


class SmartWakeApp(App):

    def build(self):
        self.title = "SmartWake"

        Window.clearcolor = (0.06, 0.09, 0.15, 1)

        self.alarm_manager = AlarmManager()

        self.alarm_sound = SoundLoader.load("sounds/alarm.wav")

        if self.alarm_sound:
            self.alarm_sound.loop = True

        self.home = HomeScreen(self)
        self.camera_screen = CameraScreen(self)
        self.add_alarm_screen = AddAlarm(self)

        self.screen_manager = ScreenManager()

        home_page = Screen(name="home")
        home_page.add_widget(self.home)

        camera_page = Screen(name="camera")
        camera_page.add_widget(self.camera_screen)

        self.screen_manager.add_widget(home_page)
        self.screen_manager.add_widget(camera_page)

        Clock.schedule_interval(self.check_alarms, 1)

        return self.screen_manager

    def show_screen(self, screen):
        if screen == self.camera_screen:
            self.screen_manager.current = "camera"
        else:
            self.screen_manager.current = "home"

    def open_add_alarm(self):
        self.add_alarm_screen.open()

    def open_camera(self):
        self.show_screen(self.camera_screen)
        self.camera_screen.start_camera()

    def back_to_home(self):
        self.camera_screen.stop_camera()
        self.show_screen(self.home)

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

    def on_stop(self):
        self.camera_screen.stop_camera()


if __name__ == "__main__":
    SmartWakeApp().run()
