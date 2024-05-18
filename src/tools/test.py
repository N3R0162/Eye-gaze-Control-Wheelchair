import cv2

# Define the GStreamer pipeline
pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12 ! "
    "nvvidconv ! "
    "video/x-raw, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
)

# Create a VideoCapture object
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame from camera.")
        break

    # Display the frame
    cv2.imshow('CSI Camera', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
