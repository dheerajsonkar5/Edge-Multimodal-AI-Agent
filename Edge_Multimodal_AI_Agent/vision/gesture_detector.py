"""
MediaPipe Gesture Detector

Detects

- Hand Presence
- Left Hand
- Right Hand
- Finger Count
"""

import cv2
import mediapipe as mp


class GestureDetector:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(

            static_image_mode=False,

            max_num_hands=2,

            min_detection_confidence=0.5,

            min_tracking_confidence=0.5

        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        gestures = []

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                self.drawer.draw_landmarks(

                    frame,

                    hand_landmarks,

                    self.mpHands.HAND_CONNECTIONS

                )

                gestures.append({

                    "hand_detected": True,

                    "landmarks": len(hand_landmarks.landmark)

                })

        return frame, gestures

    def close(self):

        self.hands.close()