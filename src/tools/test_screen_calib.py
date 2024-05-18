import cv2
import numpy as np
import os
import time

def capture_and_estimate_camera_position(num_images=10, pattern_size=(7, 10), square_size=1.0):
    obj_points = []
    img_points = []

    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[1], 0:pattern_size[0]].T.reshape(-1, 2)
    objp *= square_size

    cap = cv2.VideoCapture(0)  # Adjust the index to your camera
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        return

    count = 0
    print("Capturing calibration images...")

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from camera.")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            print(f"Checkerboard detected for image {count + 1}")
            count += 1
            cv2.drawChessboardCorners(frame, pattern_size, corners, ret)
            img_points.append(corners)
            obj_points.append(objp)
            cv2.imshow('Calibration', frame)

        # Wait for user to press 'c' to capture the next image or 'q' to quit...
        print("Press 'c' to capture the next image or 'q' to quit...")
        while True:
            key = cv2.waitKey(1)
            if key == ord('c'):
                break
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                print("Calibration image capture complete.")
                return

        time.sleep(1)  # Optional: Add a delay to give time to reposition the checkerboard

    cap.release()
    cv2.destroyAllWindows()
    print("Calibration image capture complete.")

    if not obj_points or not img_points:
        print("Error: No valid checkerboard detections.")
        return None

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    
    if ret:
        rvec, tvec = rvecs[0], tvecs[0]
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        camera_position = -rotation_matrix.T @ tvec

        return camera_position
    else:
        raise RuntimeError("Calibration failed")

camera_position = capture_and_estimate_camera_position()
if camera_position is not None:
    print(f"Camera Position: {camera_position}")
else:
    print("Camera position estimation failed.")
