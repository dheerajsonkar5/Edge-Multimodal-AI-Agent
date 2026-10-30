import cv2

from core.logger import logger


class ObjectDetector:

    def __init__(self):

        self.bg = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=25,
            detectShadows=False
        )

    def detect(self, frame):

        if frame is None:
            return []

        try:

            mask = self.bg.apply(frame)

            # Noise remove
            kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT,
                (3, 3)
            )

            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_OPEN,
                kernel
            )

            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            objects = []

            for contour in contours:

                if cv2.contourArea(contour) < 1200:
                    continue

                x, y, w, h = cv2.boundingRect(contour)

                objects.append(
                    (
                        int(x),
                        int(y),
                        int(w),
                        int(h)
                    )
                )

            return objects

        except Exception as e:

            logger.exception(e)

            return []