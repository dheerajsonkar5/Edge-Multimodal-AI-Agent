# test_camera.py
import cv2

print("Testing camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found!")
    print("Try:")
    print("  - Check camera is connected")
    print("  - Try index 1: cap = cv2.VideoCapture(1)")
    print("  - Check Windows Camera app works")
else:
    print("✅ Camera opened successfully!")
    ret, frame = cap.read()
    if ret:
        print("✅ Frame captured successfully!")
        cv2.imwrite("test.jpg", frame)
        print("📸 Saved test.jpg")
    else:
        print("❌ Could not read frame")
    cap.release()