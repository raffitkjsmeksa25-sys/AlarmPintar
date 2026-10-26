
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class SmartWakeApp(App):
    def build(self):
        self.title = "SmartWake"

        Window.clearcolor = (0.06, 0.09, 0.15, 1)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="SMARTWAKE",
            font_size="28sp",
            bold=True,
            color=(0.4, 0.7, 1, 1)
        )

        self.clock_label = Label(
            text="00:00:00",
            font_size="42sp",
            bold=True
        )

        description = Label(
            text="Smart Alarm Application",
            font_size="16sp"
        )

        status = Label(
            text="Selamat datang di SmartWake!",
            font_size="14sp"
        )

        layout.add_widget(title)
        layout.add_widget(self.clock_label)
        layout.add_widget(description)
        layout.add_widget(status)

        Clock.schedule_interval(self.update_clock, 1)

        return layout

    def update_clock(self, dt):
        self.clock_label.text = datetime.now().strftime("%H:%M:%S")


if __name__ == "__main__":
    SmartWakeApp().run()
