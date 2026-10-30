"""
Multi Camera Service
----------------------------------
Supports

✔ USB Camera
✔ Laptop Camera
✔ External Camera
✔ IP Camera
"""

import cv2


class MultiCameraService:

    def __init__(self):

        self.cameras = {}

    # --------------------------------

    def add_camera(self, camera_id=0):

        cap = cv2.VideoCapture(camera_id)

        if cap.isOpened():

            self.cameras[camera_id] = cap

            return True

        return False

    # --------------------------------

    def add_ip_camera(self, url):

        cap = cv2.VideoCapture(url)

        if cap.isOpened():

            self.cameras[url] = cap

            return True

        return False

    # --------------------------------

    def read(self, camera_id):

        if camera_id not in self.cameras:
            return False, None

        return self.cameras[camera_id].read()

    # --------------------------------

    def available_cameras(self):

        return list(self.cameras.keys())

    # --------------------------------

    def remove_camera(self, camera_id):

        if camera_id in self.cameras:

            self.cameras[camera_id].release()

            del self.cameras[camera_id]

    # --------------------------------

    def release_all(self):

        for camera in self.cameras.values():

            camera.release()

        self.cameras.clear()

        cv2.destroyAllWindows()

    # --------------------------------

    def camera_status(self):

        status = {}

        for cam_id, cap in self.cameras.items():

            status[str(cam_id)] = cap.isOpened()

        return status