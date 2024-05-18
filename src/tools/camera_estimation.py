import glob
import numpy as np
import cv2

def estimate_camera_position(pattern_size=(7, 10), square_size=1.0, calibration_images_path='/home/kyv/Desktop/Capstone/WebCamGazeEstimation/src/tools/calibration_images/*.png'):
    obj_points = []
    img_points = []

    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[1], 0:pattern_size[0]].T.reshape(-1, 2)
    objp *= square_size

    images = glob.glob(calibration_images_path)
    if not images:
        print("Error: No calibration images found.")
        return None

    for fname in images:
        img = cv2.imread(fname)
        if img is None:
            print(f"Error: Unable to load image {fname}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            print(f"Checkerboard detected in image {fname}")
            img_points.append(corners)
            obj_points.append(objp)
        else:
            print(f"Checkerboard not detected in image {fname}")

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

camera_position = estimate_camera_position()
if camera_position is not None:
    print(f"Camera Position: {camera_position}")
else:
    print("Camera position estimation failed.")
