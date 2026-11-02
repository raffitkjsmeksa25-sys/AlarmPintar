
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle


class AddAlarm:
    def __init__(self, app):
        self.app = app

    def open(self):
        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        with content.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            background = RoundedRectangle(
                pos=content.pos,
                size=content.size,
                radius=[15]
            )

        def update_background(instance, value):
            background.pos = instance.pos
            background.size = instance.size

        content.bind(
            pos=update_background,
            size=update_background
        )

        title = Label(
            text="[b]ATUR ALARM BARU[/b]",
            markup=True,
            font_size="22sp",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=45
        )

        description = Label(
            text="Pilih jam dan menit alarm",
            font_size="14sp",
            color=(0.6, 0.7, 0.85, 1),
            size_hint_y=None,
            height=30
        )

        time_layout = BoxLayout(
            spacing=15
        )

        hour = Spinner(
            text="07",
            values=[f"{i:02d}" for i in range(24)],
            font_size="24sp",
            background_normal="",
            background_color=(0.12, 0.35, 0.62, 1)
        )

        separator = Label(
            text=":",
            font_size="30sp",
            bold=True,
            size_hint_x=0.3
        )

        minute = Spinner(
            text="00",
            values=[f"{i:02d}" for i in range(60)],
            font_size="24sp",
            background_normal="",
            background_color=(0.12, 0.35, 0.62, 1)
        )

        time_layout.add_widget(hour)
        time_layout.add_widget(separator)
        time_layout.add_widget(minute)

        save_button = Button(
            text="SIMPAN ALARM",
            font_size="17sp",
            bold=True,
            background_normal="",
            background_color=(0.1, 0.48, 0.9, 1),
            size_hint_y=None,
            height=55
        )

        content.add_widget(title)
        content.add_widget(description)
        content.add_widget(time_layout)
        content.add_widget(save_button)

        popup = Popup(
            title="SMARTWAKE",
            title_color=(0.4, 0.75, 1, 1),
            separator_color=(0.1, 0.48, 0.9, 1),
            content=content,
            size_hint=(0.88, 0.5),
            background_color=(0.06, 0.09, 0.16, 1)
        )

        def save_alarm(instance):
            alarm_time = f"{hour.text}:{minute.text}"

            self.app.add_alarm(alarm_time)

            self.app.home.status_label.text = (
                f"Alarm berhasil disimpan: {alarm_time}"
            )

            popup.dismiss()

        save_button.bind(on_press=save_alarm)

        popup.open()
