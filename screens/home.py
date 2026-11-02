
from datetime import datetime

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

from components.alarm_card import AlarmCard


class HomeScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=25,
            spacing=15,
            **kwargs
        )

        self.app = app

        with self.canvas.before:
            Color(0.04, 0.07, 0.13, 1)
            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        title = Label(
            text="[b]SMART[/b][color=33A8FF]WAKE[/color]",
            markup=True,
            font_size="30sp",
            size_hint_y=None,
            height=55
        )

        subtitle = Label(
            text="SMART ALARM APPLICATION",
            font_size="12sp",
            color=(0.55, 0.65, 0.8, 1),
            size_hint_y=None,
            height=25
        )

        self.clock_label = Label(
            text="00:00:00",
            font_size="52sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=100
        )

        self.status_label = Label(
            text="Selamat datang di SmartWake!",
            font_size="14sp",
            color=(0.4, 0.75, 1, 1),
            size_hint_y=None,
            height=35
        )

        add_alarm_button = Button(
            text="+  TAMBAH ALARM",
            font_size="18sp",
            bold=True,
            background_normal="",
            background_color=(0.1, 0.48, 0.9, 1),
            size_hint_y=None,
            height=55
        )

        add_alarm_button.bind(
            on_press=self.open_add_alarm
        )

        alarm_title = Label(
            text="[b]DAFTAR ALARM[/b]",
            markup=True,
            font_size="20sp",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=45,
            halign="left"
        )

        self.alarm_list = BoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None
        )

        self.alarm_list.bind(
            minimum_height=self.alarm_list.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.alarm_list)

        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(self.clock_label)
        self.add_widget(self.status_label)
        self.add_widget(add_alarm_button)
        self.add_widget(alarm_title)
        self.add_widget(scroll)

        Clock.schedule_interval(self.update_clock, 1)

        self.refresh_alarm_list()

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

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
