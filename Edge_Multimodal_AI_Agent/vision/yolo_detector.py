"""
YOLOv11 Detector
----------------
Detects:
- Person
- Laptop
- Mobile
- Monitor
- Keyboard
- Mouse
- Bottle
- Chair
"""

from ultralytics import YOLO
import cv2


class YOLODetector:

    def __init__(self,
                 model_path="models/yolov11n.pt",
                 confidence=0.50):

        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                conf = float(box.conf[0])

                cls = int(box.cls[0])

                label = self.model.names[cls]

                detections.append({

                    "label": label,

                    "confidence": round(conf, 2),

                    "bbox": [x1, y1, x2, y2]

                })

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )

        return frame, detections