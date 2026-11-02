
from datetime import datetime

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from components.alarm_card import AlarmCard


class HomeScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=30,
            spacing=15,
            **kwargs
        )

        self.app = app

        title = Label(
            text="SMARTWAKE",
            font_size="28sp",
            bold=True,
            color=(0.4, 0.7, 1, 1),
            size_hint_y=None,
            height=50
        )

        self.clock_label = Label(
            text="00:00:00",
            font_size="42sp",
            bold=True,
            size_hint_y=None,
            height=70
        )

        description = Label(
            text="Smart Alarm Application",
            font_size="16sp",
            size_hint_y=None,
            height=35
        )

        self.status_label = Label(
            text="Selamat datang di SmartWake!",
            font_size="14sp",
            size_hint_y=None,
            height=35
        )

        add_alarm_button = Button(
            text="TAMBAH ALARM",
            font_size="18sp",
            size_hint_y=None,
            height=55
        )

        add_alarm_button.bind(
            on_press=self.open_add_alarm
        )

        alarm_title = Label(
            text="DAFTAR ALARM",
            font_size="20sp",
            bold=True,
            size_hint_y=None,
            height=40
        )

        self.alarm_list = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )

        self.alarm_list.bind(
            minimum_height=self.alarm_list.setter("height")
        )

        scroll = ScrollView()

        scroll.add_widget(self.alarm_list)

        self.add_widget(title)
        self.add_widget(self.clock_label)
        self.add_widget(description)
        self.add_widget(self.status_label)
        self.add_widget(add_alarm_button)
        self.add_widget(alarm_title)
        self.add_widget(scroll)

        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, dt):
        self.clock_label.text = datetime.now().strftime("%H:%M:%S")

    def open_add_alarm(self, instance):
        self.app.open_add_alarm()

    def refresh_alarm_list(self):
        self.alarm_list.clear_widgets()

        alarms = self.app.alarm_manager.get_alarms()

        for index, alarm in enumerate(alarms):
            card = AlarmCard(
                alarm=alarm,
                index=index,
                app=self.app
            )

            self.alarm_list.add_widget(card)
