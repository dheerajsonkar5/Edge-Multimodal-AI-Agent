import cv2


class FaceDetector:

    def __init__(self):
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return self.detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )