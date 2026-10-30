import cv2

from core.config import settings
from core.logger import logger


class CameraService:

    def __init__(self):
        self.camera = None

    # ------------------------------------
    # Open Camera
    # ------------------------------------
    def open(self):

        if self.camera is not None and self.camera.isOpened():
            return

        logger.info(f"Opening Camera Index : {settings.CAMERA_INDEX}")

        # Try DirectShow first
        self.camera = cv2.VideoCapture(
            settings.CAMERA_INDEX,
            cv2.CAP_DSHOW
        )

        # Fallback
        if not self.camera.isOpened():

            logger.warning("DirectShow failed. Trying default backend...")

            self.camera.release()

            self.camera = cv2.VideoCapture(settings.CAMERA_INDEX)

        if not self.camera.isOpened():

            raise RuntimeError(
                f"Unable to open camera index {settings.CAMERA_INDEX}"
            )

        # Camera warm-up
        for _ in range(20):
            self.camera.read()

        logger.info("Camera opened successfully.")

    # Backward compatibility
    start = open

    # ------------------------------------
    # Read Frame
    # ------------------------------------
    def read(self):

        if self.camera is None:
            return False, None

        ret, frame = self.camera.read()

        if not ret:

            # Retry once
            ret, frame = self.camera.read()

        return ret, frame

    # ------------------------------------
    # Read Frame Only
    # ------------------------------------
    def read_frame(self):

        ret, frame = self.read()

        if ret:
            return frame

        return None

    # ------------------------------------
    # Release Camera
    # ------------------------------------
    def release(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None

            cv2.destroyAllWindows()

            logger.info("Camera released.")

    # Backward compatibility
    stop = release

    # ------------------------------------
    # Camera Status
    # ------------------------------------
    def is_open(self):

        return (
            self.camera is not None
            and self.camera.isOpened()
        )