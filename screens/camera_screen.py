
import cv2

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture


class CameraScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=10,
            spacing=10,
            **kwargs
        )

        self.app = app
        self.camera = None
        self.camera_event = None

        self.preview = Image(
            allow_stretch=True,
            keep_ratio=True
        )

        back_button = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=50
        )

        back_button.bind(on_press=self.go_back)

        self.add_widget(self.preview)
        self.add_widget(back_button)

    def start_camera(self):
        if self.camera is not None:
            return

        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not self.camera.isOpened():
            print("Kamera gagal dibuka!")
            self.camera.release()
            self.camera = None
            return

        print("Kamera SmartWake berhasil dibuka!")

        self.camera_event = Clock.schedule_interval(
            self.update_camera,
            1 / 20
        )

    def update_camera(self, dt):
        if self.camera is None:
            return

        success, frame = self.camera.read()

        if not success:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 0)

        height, width, channels = frame.shape

        texture = Texture.create(
            size=(width, height),
            colorfmt="rgb"
        )

        texture.blit_buffer(
            frame.tobytes(),
            colorfmt="rgb",
            bufferfmt="ubyte"
        )

        self.preview.texture = texture

    def stop_camera(self):
        if self.camera_event:
            self.camera_event.cancel()
            self.camera_event = None

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.preview.texture = None

        print("Kamera SmartWake ditutup!")

    def go_back(self, instance):
        self.stop_camera()
        self.app.back_to_home()
