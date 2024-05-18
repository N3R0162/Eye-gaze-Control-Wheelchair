import cv2
import numpy as np
import os
import time

def capture_calibration_images(num_images=10, pattern_size=(7, 10), save_dir='/home/kyv/Desktop/Capstone/WebCamGazeEstimation/src/tools/calibration_images/'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
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
            filename = f"{save_dir}/calib_{count}.png"  # Fixed the file path format
            cv2.imwrite(filename, frame)
            print(f"Saved calibration image: {filename}")

        cv2.imshow('Calibration', frame)
        
        # Wait for user to press 'c' to capture the next image
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

capture_calibration_images()
