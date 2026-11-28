
import os
import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader

from screens.home import HomeScreen
from screens.add_alarm import AddAlarm
from screens.camera_screen import CameraScreen
from services.alarm_manager import AlarmManager


# Menentukan lokasi file pendukung aplikasi
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SmartWakeApp(App):

    def build(self):
        self.title = "SmartWake"

        Window.clearcolor = (0.06, 0.09, 0.15, 1)

        self.alarm_manager = AlarmManager()

        # Memuat suara alarm
        sound_path = os.path.join(
            BASE_DIR,
            "sounds",
            "alarm.wav"
        )

        self.alarm_sound = SoundLoader.load(sound_path)

        if self.alarm_sound:
            self.alarm_sound.loop = True

        self.active_alarm_popup = None
        self.alarm_popup_event = None

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
            if self.active_alarm_popup is None:
                self.show_alarm_popup(alarm_time)

    def show_alarm_popup(self, alarm_time):

        # Mengaktifkan kamera
        self.show_screen(self.camera_screen)
        self.camera_screen.start_camera()

        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        message = Label(
            text=f"ALARM BERBUNYI!\nWaktu: {alarm_time}",
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=65
        )

        popup_camera = Image(
            allow_stretch=True,
            keep_ratio=True
        )

        status_label = Label(
            text="Menunggu deteksi mata...",
            size_hint_y=None,
            height=40
        )

        stop_button = Button(
            text="BUKA MATA UNTUK MEMATIKAN",
            size_hint_y=None,
            height=55,
            disabled=True
        )

        content.add_widget(message)
        content.add_widget(popup_camera)
        content.add_widget(status_label)
        content.add_widget(stop_button)

        popup = Popup(
            title="SMARTWAKE",
            content=content,
            size_hint=(0.9, 0.85),
            auto_dismiss=False
        )

        self.active_alarm_popup = popup

        open_count = {"value": 0}

        def update_alarm_preview(dt):

            popup_camera.texture = self.camera_screen.preview.texture

            eye_status = self.camera_screen.eye_status.text
            status_label.text = eye_status

            if eye_status.startswith("MATA TERBUKA"):
                open_count["value"] += 1
            else:
                open_count["value"] = 0

            if open_count["value"] >= 10:
                stop_button.disabled = False
                stop_button.text = "MATIKAN ALARM"
            else:
                stop_button.disabled = True
                stop_button.text = "BUKA MATA UNTUK MEMATIKAN"

        def stop_alarm(instance):

            if stop_button.disabled:
                return

            if self.alarm_sound:
                self.alarm_sound.stop()

            if self.alarm_popup_event:
                self.alarm_popup_event.cancel()
                self.alarm_popup_event = None

            popup.dismiss()
            self.active_alarm_popup = None

            self.camera_screen.stop_camera()
            self.show_screen(self.home)

            print("Alarm berhasil dimatikan!")

        stop_button.bind(on_press=stop_alarm)

        if self.alarm_sound:
            self.alarm_sound.play()

        popup.open()

        self.alarm_popup_event = Clock.schedule_interval(
            update_alarm_preview,
            0.1
        )

    def on_stop(self):

        if self.alarm_popup_event:
            self.alarm_popup_event.cancel()
            self.alarm_popup_event = None

        if self.alarm_sound:
            self.alarm_sound.stop()

        self.camera_screen.stop_camera()


if __name__ == "__main__":
    SmartWakeApp().run()
