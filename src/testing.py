import cv2



def main():
    # Initialize the CSRT tracker
    tracker = cv2.TrackerCSRT_create()

    # Read the video stream or video file
    video = cv2.VideoCapture(0)

    # Read the very first frame
    success, frame = video.read()
    if not success:
        print("Failed to read video")
        exit()

    # Manually select the bounding box (ROI) on the first frame
    # Press ENTER or SPACE after selecting the box
    bbox = cv2.selectROI("Tracking Window", frame, fromCenter=False, showCrosshair=True)

    # Initialize the tracker with the selected bounding box
    tracker.init(frame, bbox)

    while True:
        success, frame = video.read()
        if not success:
            break
            
        # Update the tracker with the new frame
        success, bbox = tracker.update(frame)
        
        # If the object is tracked successfully, draw the rectangle
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        # Display the output
        cv2.imshow("Tracking Window", frame)
        
        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()