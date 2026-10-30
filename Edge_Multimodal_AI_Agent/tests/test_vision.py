# tests/test_vision.py
import unittest
import cv2
import numpy as np
from vision.person_detector import PersonDetector
from vision.pose_detector import PoseDetector

class TestVisionPipeline(unittest.TestCase):
    def setUp(self):
        """
        Initializes core sub-modules before running logical mock verification.
        """
        self.person_detector = PersonDetector()
        self.pose_detector = PoseDetector()
        
        # Creating a blank synthetic black image matrix frame for mock inputs
        self.mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_empty_buffer_handling(self):
        """
        Verifies that passing an empty frame buffer does not trigger unexpected runtime exceptions.
        """
        status, boxes = self.person_detector.detect(None)
        self.assertFalse(status)
        self.assertEqual(len(boxes), 0)

    def test_synthetic_frame_processing(self):
        """
        Ensures that synthetic dark matrix profiles evaluate securely to normal states.
        """
        metrics = self.pose_detector.analyze_posture(self.mock_frame)
        self.assertIn("status", metrics)
        self.assertFalse(metrics.get("slouching_detected", True))

if __name__ == "__main__":
    unittest.main()