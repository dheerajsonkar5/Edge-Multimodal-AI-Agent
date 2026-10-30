import cv2
import mediapipe as mp

from core.logger import logger


class PoseDetector:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def detect(self, frame):

        if frame is None:
            return None

        try:

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            rgb.flags.writeable = False

            results = self.pose.process(rgb)

            rgb.flags.writeable = True

            return results

        except Exception as e:

            logger.exception(e)

            return None

    def close(self):

        try:
            self.pose.close()
        except Exception:
            pass