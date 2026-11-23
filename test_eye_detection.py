
import cv2
import os
import time
import math
import mediapipe as mp

# Lokasi model deteksi wajah
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
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


# Pengaturan MediaPipe
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_faces=1
)

# Membuka kamera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Kamera gagal dibuka!")
    exit()

print("Deteksi mata SmartWake aktif!")
print("Tekan Q untuk keluar.")

try:
    with FaceLandmarker.create_from_options(options) as landmarker:

        while True:
            success, frame = camera.read()

            if not success:
                break

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

            result = landmarker.detect_for_video(
                mp_image,
                timestamp
            )

            if result.face_landmarks:
                landmarks = result.face_landmarks[0]

                left_ear = calculate_ear(
                    landmarks, LEFT_EYE, width, height
                )

                right_ear = calculate_ear(
                    landmarks, RIGHT_EYE, width, height
                )

                average_ear = (left_ear + right_ear) / 2

                if average_ear < 0.20:
                    eye_status = "MATA TERTUTUP"
                    color = (0, 0, 255)
                else:
                    eye_status = "MATA TERBUKA"
                    color = (0, 255, 0)

                cv2.putText(
                    frame,
                    eye_status,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    f"EAR: {average_ear:.3f}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

            else:
                cv2.putText(
                    frame,
                    "WAJAH TIDAK TERDETEKSI",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            cv2.imshow(
                "Tes Deteksi Mata SmartWake",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    camera.release()
    cv2.destroyAllWindows()
