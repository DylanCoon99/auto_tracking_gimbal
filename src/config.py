# create a data class that stores the state of our gimbal
import logging
import cv2
from libcamera import Transform
from picamera2 import Picamera2



'''

Attributes
	tracker
	pi camera
	servo kit
	logger


Methods
	__init__
	__enter__
	__exit__
	current_frame
	get_next_frame
	error (gets the error for the current frame)
	update_servos


make it a context manager class: when in closes clear the window, exit and set the servos to origin



'''


class GimbalConfig:
	def __init__(self, channels=16, address=0x40, size=(640, 480), P=0, D=0):
		"""Initialize parameters needed for setup."""
		self.channels = channels
		self.address = address
		self.size = size
		self.logger = logging.getLogger(__name__)
		self.tracker = None
		self.picam2 = None
		self.servo_kit = None
		self.current_frame = None
		self.P = P
		self.D = D

		# Configures the root logger globally
		logging.basicConfig(
			level=logging.INFO,
			format="%(asctime)s - %(levelname)s - %(message)s",
			handlers=[logging.StreamHandler()]
		)

		self.logger.info("Initializing GimbalConfig with parameters")
		self.logger.info(f"channels: {self.channels}")
		self.logger.info(f"address: {self.address}")
		self.logger.info(f"size: {self.size}")



	def __enter__(self):
		"""Set up the resource and return the target variable."""
		self.tracker = cv2.TrackerCSRT_create()

		# Initialize Pi camera
		self.picam2 = Picamera2()
		self.picam2.configure(self.picam2.create_preview_configuration(main={"format": "RGB888", "size": self.size}, transform=Transform(hflip=True, vflip=True)))
		self.picam2.start()

		# Read the very first frame
		self.current_frame = self.picam2.capture_array()
		if self.current_frame is None:
			self.logger.error("Failed to read video")
			exit()

		# Manually select the bounding box (ROI) on the first frame
		# Press ENTER or SPACE after selecting the box
		bbox = cv2.selectROI("Tracking Window", self.current_frame, fromCenter=False, showCrosshair=True)

		# Initialize the tracker with the selected bounding box
		self.tracker.init(self.current_frame, bbox)

		return self


	def run(self):

		while True:
			frame = self.picam2.capture_array()
			self.current_frame = frame
			if frame is None:
				break

			# Update the tracker with the new frame
			success, bbox = self.tracker.update(frame)

			# If the object is tracked successfully, draw the rectangle
			if success:
				x, y, w, h = [int(v) for v in bbox]
				self.logger.info(f"BBOX ERROR: {self._get_error(bbox)}")
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
			else:
				cv2.putText(frame, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			
			# Display the output
			cv2.imshow("Tracking Window", frame)

			# Exit loop if 'q' key is pressed
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		return

	def _get_error(self, bbox):
		# gets the error of the current frame
		x, y, w, h = [int(v) for v in bbox]

		frame_center = (self.size[0] / 2, self.size[1] / 2)
		bbox_center = (x + w/2, y + h/2)

		error_x = (bbox_center[0] - frame_center[0]) / (self.size[0] / 2)
		error_y = (bbox_center[1] - frame_center[1]) / (self.size[1] / 2)

		return (error_x, error_y)


	def _update_servo_state(self):
		# interfaces with the servo kit (servo.py)
		# updates the servo state



		return

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Clean up the resource, regardless of errors."""
		self.logger.info("Exiting GimbalConfig")
		self.connection = None

		if exc_type is not None:
			self.logger.error(f"An error occurred: {exc_val}")
			# Return True to suppress the exception, False to let it propagate
			return False

		self.logger.info("Closing Window")

