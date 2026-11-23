
import cv2
import os
import time
import math
import mediapipe as mp

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture


# Lokasi model MediaPipe
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "face_landmarker.task"
)

# Titik landmark mata
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]


def calculate_ear(landmarks, eye_points, width, height):
    points = []

    for index in eye_points:
        x = landmarks[index].x * width
        y = landmarks[index].y * height
        points.append((x, y))

    vertical_1 = math.dist(points[1], points[5])
    vertical_2 = math.dist(points[2], points[4])
    horizontal = math.dist(points[0], points[3])

    if horizontal == 0:
        return 0

    return (vertical_1 + vertical_2) / (2 * horizontal)


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
        self.landmarker = None
        self.last_timestamp = 0

        self.preview = Image(
            allow_stretch=True,
            keep_ratio=True
        )

        self.eye_status = Label(
            text="Status: Kamera belum aktif",
            size_hint_y=None,
            height=40,
            font_size=18
        )

        back_button = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=50
        )

        back_button.bind(on_press=self.go_back)

        self.add_widget(self.preview)
        self.add_widget(self.eye_status)
        self.add_widget(back_button)

    def start_camera(self):
        if self.camera is not None:
            return

        if not os.path.exists(MODEL_PATH):
            self.eye_status.text = "Model deteksi tidak ditemukan!"
            print("File face_landmarker.task tidak ditemukan!")
            return

        try:
            options = mp.tasks.vision.FaceLandmarkerOptions(
                base_options=mp.tasks.BaseOptions(
                    model_asset_path=MODEL_PATH
                ),
                running_mode=mp.tasks.vision.RunningMode.VIDEO,
                num_faces=1
            )

            self.landmarker = (
                mp.tasks.vision.FaceLandmarker.create_from_options(
                    options
                )
            )

            self.camera = cv2.VideoCapture(
                0,
                cv2.CAP_DSHOW
            )

            if not self.camera.isOpened():
                print("Kamera gagal dibuka!")
                self.camera.release()
                self.camera = None
                self.landmarker.close()
                self.landmarker = None
                return

            print("Kamera SmartWake berhasil dibuka!")

            self.eye_status.text = "Mendeteksi mata..."

            self.camera_event = Clock.schedule_interval(
                self.update_camera,
                1 / 20
            )

        except Exception as error:
            print("Terjadi kesalahan:", error)
            self.eye_status.text = "Gagal memulai deteksi mata"

            if self.camera is not None:
                self.camera.release()
                self.camera = None

            if self.landmarker is not None:
                self.landmarker.close()
                self.landmarker = None

    def update_camera(self, dt):
        if self.camera is None or self.landmarker is None:
            return

        success, frame = self.camera.read()

        if not success:
            return

        height, width, _ = frame.shape

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp = time.monotonic_ns() // 1_000_000
        timestamp = max(timestamp, self.last_timestamp + 1)
        self.last_timestamp = timestamp

        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp
        )

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]

            left_ear = calculate_ear(
                landmarks,
                LEFT_EYE,
                width,
                height
            )

            right_ear = calculate_ear(
                landmarks,
                RIGHT_EYE,
                width,
                height
            )

            average_ear = (left_ear + right_ear) / 2

            if average_ear < 0.20:
                status = "MATA TERTUTUP"
                color = (0, 0, 255)
            else:
                status = "MATA TERBUKA"
                color = (0, 255, 0)

            self.eye_status.text = (
                f"{status} | EAR: {average_ear:.3f}"
            )

        else:
            status = "WAJAH TIDAK TERDETEKSI"
            color = (0, 0, 255)

            self.eye_status.text = status

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        frame = cv2.flip(frame, 0)
        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

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

        if self.landmarker is not None:
            self.landmarker.close()
            self.landmarker = None

        self.preview.texture = None
        self.eye_status.text = "Status: Kamera belum aktif"

        print("Kamera SmartWake ditutup!")

    def go_back(self, instance):
        self.stop_camera()
        self.app.back_to_home()
