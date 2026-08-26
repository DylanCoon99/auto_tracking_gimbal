import cv2
from ultralytics import YOLO

# Load the Nano model
model = YOLO("yolo11n.pt")

# Open webcam connection (0 is typically the default built-in camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run inference on the current live frame
    results = model(frame)

    # Visualize results directly back onto the frame
    annotated_frame = results[0].plot()

    # Display image window
    cv2.imshow("YOLO Nano Real-Time Detection", annotated_frame)

    # Break out if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()