import cv2


class EyeDetector:

    def __init__(self):
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

    def detect(self, gray):
        return self.detector.detectMultiScale(gray)