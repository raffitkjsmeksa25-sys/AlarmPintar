
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup


class AddAlarm:
    def __init__(self, app):
        self.app = app

    def open(self):
        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="PILIH WAKTU ALARM",
            font_size="20sp"
        )

        time_layout = BoxLayout(spacing=10)

        hour = Spinner(
            text="07",
            values=[f"{i:02d}" for i in range(24)]
        )

        minute = Spinner(
            text="00",
            values=[f"{i:02d}" for i in range(60)]
        )

        time_layout.add_widget(hour)
        time_layout.add_widget(minute)

        save_button = Button(
            text="SIMPAN ALARM"
        )

        content.add_widget(title)
        content.add_widget(time_layout)
        content.add_widget(save_button)

        popup = Popup(
            title="Tambah Alarm",
            content=content,
            size_hint=(0.85, 0.5)
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
