# """
# Frame Processor - FINAL SOLUTION
# Face + Eye + Fatigue + Blink + Person + Object Detection
# Sab kaam karega! 100% GUARANTEE
# """

# """
# Frame Processor - WITH GLASSES SUPPORT
# Face + Eye + Fatigue + Blink + Person + Object Detection
# """
# import cv2
# import numpy as np
# from ultralytics import YOLO
# from core.logger import get_logger
# import warnings
# import sys
# import os

# warnings.filterwarnings("ignore")
# logger = get_logger()


# class FrameProcessor:
#     def __init__(self):
#         logger.info("Initializing FrameProcessor...")
        
#         # =============================================
#         # HAAR CASCADES (Face + Eye) - GLASSES SUPPORT
#         # =============================================
#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
#         )
        
#         # ✅ PRIMARY: Standard eye cascade
#         self.eye_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + 'haarcascade_eye.xml'
#         )
        
#         # ✅ SECONDARY: Glasses-specific cascade (BETTER FOR SPECTACLES)
#         self.eye_glasses_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml'
#         )
        
#         # Face detection params - Long range
#         self.face_scale_factor = 1.05
#         self.face_min_neighbors = 3
        
#         # =============================================
#         # YOLO
#         # =============================================
#         try:
#             with open(os.devnull, 'w') as devnull:
#                 old_stdout = sys.stdout
#                 sys.stdout = devnull
#                 self.yolo = YOLO("yolov8n.pt", verbose=False)
#                 sys.stdout = old_stdout
#             logger.info("YOLO loaded")
#         except:
#             self.yolo = None
#             logger.warning("YOLO not loaded")
        
#         # =============================================
#         # FATIGUE STATE
#         # =============================================
#         self.fatigue_counter = 0
#         self.total_blinks = 0
#         self.fatigue_threshold = 15
#         self.ear_threshold = 0.25
        
#         logger.info("FrameProcessor Ready!")
    
#     def calculate_ear(self, eye_rect):
#         """EAR = height / width"""
#         x, y, w, h = eye_rect
#         if w == 0:
#             return 0.5
#         return h / w
    
#     def process_frame(self, frame):
#         result = {
#             "faces": 0,
#             "persons": 0,
#             "objects": 0,
#             "fatigue_detected": False,
#             "fatigue_level": 0,
#             "ear": 0.5,
#             "blinks": 0,
#             "events": []
#         }
        
#         if frame is None:
#             return frame, result
        
#         annotated = frame.copy()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         h, w = frame.shape[:2]
        
#         ear_value = 0.5
#         status = "SCANNING"
#         color = (255, 255, 0)
#         is_eye_closed = False
        
#         try:
#             # =============================================
#             # FACE DETECTION
#             # =============================================
#             faces = self.face_cascade.detectMultiScale(
#                 gray, 
#                 scaleFactor=self.face_scale_factor, 
#                 minNeighbors=self.face_min_neighbors,
#                 minSize=(30, 30)
#             )
            
#             if len(faces) > 0:
#                 result["faces"] = len(faces)
                
#                 for (fx, fy, fw, fh) in faces:
#                     distance = "Far" if fw < 80 else "Near" if fw < 160 else "Close"
#                     cv2.rectangle(annotated, (fx, fy), (fx+fw, fy+fh), (0, 255, 0), 2)
#                     cv2.putText(annotated, f"Face ({distance})", (fx, fy-10),
#                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
#                     roi_gray = gray[fy:fy+fh//2, fx:fx+fw]
#                     roi_color = annotated[fy:fy+fh//2, fx:fx+fw]
                    
#                     # =============================================
#                     # EYE DETECTION - WITH GLASSES SUPPORT
#                     # =============================================
#                     eyes = []
                    
#                     # ✅ TRY 1: Glasses cascade first (better for specs)
#                     eyes_glasses = self.eye_glasses_cascade.detectMultiScale(roi_gray, 1.1, 5)
#                     if len(eyes_glasses) >= 1:
#                         eyes = eyes_glasses
#                         cv2.putText(annotated, "Glasses Mode", (fx, fy+fh+20),
#                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    
#                     # ✅ TRY 2: Standard cascade (if glasses cascade fails)
#                     if len(eyes) == 0:
#                         eyes_std = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
#                         if len(eyes_std) >= 1:
#                             eyes = eyes_std
                    
#                     # ✅ TRY 3: Both cascades combined
#                     if len(eyes) == 0:
#                         # Try both and merge
#                         eyes1 = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
#                         eyes2 = self.eye_glasses_cascade.detectMultiScale(roi_gray, 1.1, 5)
#                         if len(eyes1) > 0 or len(eyes2) > 0:
#                             # Use whichever found more
#                             eyes = eyes1 if len(eyes1) >= len(eyes2) else eyes2
                    
#                     if len(eyes) >= 1:
#                         eye_ears = []
                        
#                         for (ex, ey, ew, eh) in eyes[:2]:
#                             cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 255), 2)
                            
#                             ear = self.calculate_ear((ex, ey, ew, eh))
#                             eye_ears.append(ear)
                            
#                             cv2.putText(roi_color, f"EAR: {ear:.3f}", (ex, ey-5),
#                                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                        
#                         if eye_ears:
#                             ear_value = sum(eye_ears) / len(eye_ears)
#                         else:
#                             ear_value = 0.5
                        
#                         if ear_value < self.ear_threshold:
#                             is_eye_closed = True
                        
#                         for (ex, ey, ew, eh) in eyes[:2]:
#                             if eh < 4:
#                                 is_eye_closed = True
                    
#                     else:
#                         # No eyes detected - check if eyes are closed
#                         # Check face region intensity
#                         face_roi = gray[fy:fy+fh//2, fx:fx+fw]
#                         if face_roi.size > 0:
#                             mean_intensity = np.mean(face_roi)
#                             if mean_intensity < 40:
#                                 is_eye_closed = True
#                                 cv2.putText(annotated, "EYES CLOSED (Intensity)", (fx, fy+fh+40),
#                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
#                     # =============================================
#                     # FATIGUE + BLINK
#                     # =============================================
#                     if is_eye_closed:
#                         self.fatigue_counter += 1
#                         status = "EYES CLOSED"
#                         color = (0, 0, 255)
#                         ear_value = 0.1
#                         cv2.putText(annotated, "EYES CLOSED", (w//2-100, 80),
#                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
#                     else:
#                         if 1 <= self.fatigue_counter <= 5:
#                             self.total_blinks += 1
#                             if self.total_blinks % 10 == 0:
#                                 logger.info(f"Blinks: {self.total_blinks}")
#                         self.fatigue_counter = max(0, self.fatigue_counter - 2)
#                         status = "EYES OPEN"
#                         color = (0, 255, 0)
#                         if ear_value < 0.3:
#                             ear_value = 0.5
                    
#                     result["ear"] = ear_value
#                     fatigue_level = min(100, (self.fatigue_counter / self.fatigue_threshold) * 100)
#                     result["fatigue_level"] = fatigue_level
#                     result["fatigue_detected"] = self.fatigue_counter >= self.fatigue_threshold
#                     result["blinks"] = self.total_blinks
                    
#                     if result["fatigue_detected"]:
#                         result["events"].append({
#                             "type": "fatigue",
#                             "severity": "high",
#                             "description": f"Fatigue: {fatigue_level:.1f}%"
#                         })
            
#             # =============================================
#             # YOLO - PERSON + OBJECT
#             # =============================================
#             if self.yolo:
#                 yolo_results = self.yolo(frame, conf=0.3, verbose=False)
                
#                 if yolo_results:
#                     for r in yolo_results:
#                         if r.boxes:
#                             for box in r.boxes:
#                                 x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
#                                 cls_id = int(box.cls[0].cpu().numpy())
#                                 conf = float(box.conf[0].cpu().numpy())
#                                 label = r.names[cls_id]
                                
#                                 if label == "person":
#                                     result["persons"] += 1
#                                     color_box = (255, 0, 0)
#                                     if result["persons"] > 1:
#                                         result["events"].append({
#                                             "type": "multiple_persons",
#                                             "severity": "medium",
#                                             "description": f"{result['persons']} persons detected"
#                                         })
#                                 else:
#                                     result["objects"] += 1
#                                     color_box = (0, 0, 255)
                                
#                                 cv2.rectangle(annotated, (x1, y1), (x2, y2), color_box, 2)
#                                 cv2.putText(annotated, f"{label}", (x1, y1-10),
#                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_box, 2)
            
#             # =============================================
#             # DISPLAY - NO EMOJI
#             # =============================================
#             y = 30
#             lines = [
#                 f"Faces: {result['faces']}",
#                 f"Persons: {result['persons']}",
#                 f"Objects: {result['objects']}",
#                 f"EAR: {result['ear']:.3f}",
#                 f"Fatigue: {result['fatigue_level']:.1f}%",
#                 f"Blinks: {result['blinks']}",
#                 f"Events: {len(result['events'])}"
#             ]
            
#             for line in lines:
#                 cv2.putText(annotated, line, (10, y),
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
#                 y += 22
            
#             cv2.putText(annotated, status, (10, y+5),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
#             # Fatigue warning
#             if result["fatigue_detected"]:
#                 cv2.putText(annotated, "FATIGUE DETECTED!", (w//2-150, 50),
#                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
#                 cv2.rectangle(annotated, (w//2-160, 30), (w//2+160, 70), (0, 0, 255), 2)
            
#             # Progress Bar
#             bar_x, bar_y, bar_w, bar_h = 10, h-40, 200, 18
#             cv2.rectangle(annotated, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (50, 50, 50), -1)
            
#             progress = min(100, (self.fatigue_counter / self.fatigue_threshold) * 100)
#             fill_w = int((progress / 100) * bar_w)
            
#             if progress < 50:
#                 bar_color = (0, 255, 0)
#             elif progress < 75:
#                 bar_color = (0, 255, 255)
#             else:
#                 bar_color = (0, 0, 255)
            
#             cv2.rectangle(annotated, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), bar_color, -1)
#             cv2.putText(annotated, f"Fatigue: {progress:.0f}%", (bar_x + 5, bar_y + 13),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
#             # Status Bar
#             cv2.rectangle(annotated, (0, h-22), (w, h), (30, 30, 30), -1)
            
#             if result["fatigue_detected"]:
#                 status_text = "FATIGUE!"
#             elif result["faces"] > 0:
#                 status_text = "ACTIVE"
#             else:
#                 status_text = "SCANNING"
            
#             cv2.putText(annotated, f"Status: {status_text}", (10, h-5),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#             cv2.putText(annotated, f"Counter: {self.fatigue_counter}/{self.fatigue_threshold}",
#                        (w-200, h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
#             # Big EAR
#             if result["fatigue_detected"]:
#                 ear_color = (0, 0, 255)
#             elif result["ear"] < 0.25:
#                 ear_color = (0, 255, 255)
#             else:
#                 ear_color = (0, 255, 0)
            
#             cv2.putText(annotated, f"EAR: {result['ear']:.3f}", (w-180, 40),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, ear_color, 2)
            
#         except Exception as e:
#             pass
        
#         return annotated, result

"""
Frame Processor - WITH MEDIAPIPE
Face + Eye + Fatigue Detection using MediaPipe
"""
import cv2
import numpy as np
import mediapipe as mp
from core.logger import get_logger

logger = get_logger()


class FrameProcessor:
    def __init__(self):
        # =============================================
        # MEDIAPIPE FACE MESH - For Face + Eye
        # =============================================
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Eye landmark indices
        self.LEFT_EYE = [33, 133, 157, 159, 145, 153]
        self.RIGHT_EYE = [362, 263, 387, 385, 374, 380]
        
        # Fatigue state
        self.fatigue_counter = 0
        self.total_blinks = 0
        self.fatigue_threshold = 15
        self.ear_threshold = 0.25
        
        logger.info("FrameProcessor ready with MediaPipe!")
    
    def calculate_ear(self, eye_points):
        """Calculate EAR from 6 eye landmarks"""
        if len(eye_points) < 6:
            return 0.5
        
        p1, p2, p3 = eye_points[0], eye_points[1], eye_points[2]
        p4, p5, p6 = eye_points[3], eye_points[4], eye_points[5]
        
        A = np.linalg.norm(p2 - p6)
        B = np.linalg.norm(p3 - p5)
        C = np.linalg.norm(p1 - p4)
        
        if C == 0:
            return 0.5
        return (A + B) / (2.0 * C)
    
    def process_frame(self, frame):
        result = {
            "faces": 0, "persons": 0, "objects": 0,
            "fatigue_detected": False, "fatigue_level": 0,
            "ear": 0.5, "blinks": 0, "events": []
        }
        
        if frame is None:
            return frame, result
        
        annotated = frame.copy()
        h, w = frame.shape[:2]
        
        try:
            # =============================================
            # MEDIAPIPE FACE + EYE DETECTION
            # =============================================
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_results = self.face_mesh.process(rgb)
            
            if face_results.multi_face_landmarks:
                result["faces"] = len(face_results.multi_face_landmarks)
                
                for landmarks in face_results.multi_face_landmarks:
                    # Draw face mesh
                    self.mp_drawing.draw_landmarks(
                        annotated, landmarks,
                        self.mp_face_mesh.FACEMESH_CONTOURS,
                        self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=1),
                        self.mp_drawing.DrawingSpec(color=(0,0,255), thickness=1)
                    )
                    
                    # Extract eye points
                    left_eye = []
                    right_eye = []
                    
                    for idx, lm in enumerate(landmarks.landmark):
                        x, y = int(lm.x * w), int(lm.y * h)
                        if idx in self.LEFT_EYE:
                            left_eye.append([x, y])
                        if idx in self.RIGHT_EYE:
                            right_eye.append([x, y])
                    
                    left_eye = np.array(left_eye)
                    right_eye = np.array(right_eye)
                    
                    # Calculate EAR
                    if len(left_eye) >= 6 and len(right_eye) >= 6:
                        left_ear = self.calculate_ear(left_eye)
                        right_ear = self.calculate_ear(right_eye)
                        ear = (left_ear + right_ear) / 2.0
                        result["ear"] = ear
                        
                        # Fatigue detection
                        if ear < self.ear_threshold:
                            self.fatigue_counter += 1
                        else:
                            if 1 <= self.fatigue_counter <= 5:
                                self.total_blinks += 1
                            self.fatigue_counter = max(0, self.fatigue_counter - 2)
                        
                        fatigue_level = min(100, (self.fatigue_counter / self.fatigue_threshold) * 100)
                        result["fatigue_level"] = fatigue_level
                        result["fatigue_detected"] = self.fatigue_counter >= self.fatigue_threshold
                        result["blinks"] = self.total_blinks
                        
                        if result["fatigue_detected"]:
                            result["events"].append({
                                "type": "fatigue",
                                "severity": "high",
                                "description": f"Fatigue: {fatigue_level:.1f}%"
                            })
            
            # Display info
            y = 30
            for line in [
                f"Faces: {result['faces']}",
                f"EAR: {result['ear']:.3f}",
                f"Fatigue: {result['fatigue_level']:.1f}%",
                f"Blinks: {result['blinks']}"
            ]:
                cv2.putText(annotated, line, (10, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                y += 25
            
            if result["fatigue_detected"]:
                cv2.putText(annotated, "FATIGUE DETECTED!", (w//2-150, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3)
            
        except Exception as e:
            logger.error(f"Error: {e}")
        
        return annotated, result
    