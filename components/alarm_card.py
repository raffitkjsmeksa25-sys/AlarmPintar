
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class AlarmCard(BoxLayout):
    def __init__(self, alarm, index, app, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=60,
            spacing=10,
            **kwargs
        )

        self.alarm = alarm
        self.index = index
        self.app = app

        self.time_label = Label(
            text=alarm["time"],
            font_size="20sp"
        )

        self.status_button = Button(
            text="AKTIF" if alarm["active"] else "NONAKTIF",
            size_hint_x=0.4
        )

        self.status_button.bind(
            on_press=self.toggle_alarm
        )

        delete_button = Button(
            text="HAPUS",
            size_hint_x=0.3
        )

        delete_button.bind(
            on_press=self.delete_alarm
        )

        self.add_widget(self.time_label)
        self.add_widget(self.status_button)
        self.add_widget(delete_button)

    def toggle_alarm(self, instance):
        self.app.toggle_alarm(self.index)

    def delete_alarm(self, instance):
        self.app.remove_alarm(self.index)
