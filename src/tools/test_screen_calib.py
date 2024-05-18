import cv2
import numpy as np
import os

def capture_and_estimate_camera_position(num_images=10, pattern_size=(7, 10), square_size=1.0):
    obj_points = []
    img_points = []

    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[1], 0:pattern_size[0]].T.reshape(-1, 2)
    objp *= square_size

    # GStreamer pipeline string
    pipeline = (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12 ! "
        "nvvidconv ! "
        "video/x-raw, width=1280, height=720, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
    )

    # Create a VideoCapture object using the GStreamer pipeline
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
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
            cv2.drawChessboardCorners(frame, pattern_size, corners, ret)
            cv2.putText(frame, f"Checkerboard detected. Press 'c' to capture", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        else:
            cv2.putText(frame, f"Move the checkerboard into view. Press 'q' to quit", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Calibration', frame)

        # Wait for user to press 'c' to capture the next image or 'q' to quit...
        key = cv2.waitKey(1)
        if key == ord('c') and ret:
            print(f"Checkerboard detected for image {count + 1}")
            img_points.append(corners)
            obj_points.append(objp)
            count += 1
        elif key == ord('q'):
            break

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
