
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class AlarmCard(BoxLayout):
    def __init__(self, alarm, index, app, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=75,
            padding=10,
            spacing=10,
            **kwargs
        )

        self.alarm = alarm
        self.index = index
        self.app = app

        with self.canvas.before:
            Color(0.09, 0.14, 0.23, 1)
            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        self.time_label = Label(
            text=alarm["time"],
            font_size="26sp",
            bold=True,
            color=(1, 1, 1, 1)
        )

        self.status_button = Button(
            text="AKTIF" if alarm["active"] else "NONAKTIF",
            font_size="12sp",
            bold=True,
            size_hint_x=0.4,
            background_normal="",
            background_color=(
                (0.05, 0.55, 0.35, 1)
                if alarm["active"]
                else (0.4, 0.4, 0.45, 1)
            )
        )

        self.status_button.bind(
            on_press=self.toggle_alarm
        )

        delete_button = Button(
            text="HAPUS",
            font_size="12sp",
            bold=True,
            size_hint_x=0.3,
            background_normal="",
            background_color=(0.75, 0.16, 0.2, 1)
        )

        delete_button.bind(
            on_press=self.delete_alarm
        )

        self.add_widget(self.time_label)
        self.add_widget(self.status_button)
        self.add_widget(delete_button)

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def toggle_alarm(self, instance):
        self.app.toggle_alarm(self.index)

    def delete_alarm(self, instance):
        self.app.remove_alarm(self.index)
