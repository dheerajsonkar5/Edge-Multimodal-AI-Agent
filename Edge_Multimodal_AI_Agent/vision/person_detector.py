import cv2

from core.logger import logger


class PersonDetector:

    def __init__(self):

        self.hog = cv2.HOGDescriptor()

        self.hog.setSVMDetector(
            cv2.HOGDescriptor_getDefaultPeopleDetector()
        )

    def detect(self, frame):

        if frame is None:
            return []

        try:

            boxes, _ = self.hog.detectMultiScale(
                frame,
                winStride=(8, 8),
                padding=(8, 8),
                scale=1.05
            )

            persons = []

            for (x, y, w, h) in boxes:

                persons.append(
                    (
                        int(x),
                        int(y),
                        int(w),
                        int(h)
                    )
                )

            return persons

        except Exception as e:

            logger.exception(e)

            return []