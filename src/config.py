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
    def __init__(self, channels=16, address=0x40, size=(640, 480)):
        """Initialize parameters needed for setup."""
        self.channels = channels
        self.address = address
        self.size = size
        self.logger = logging.getLogger(__name__)
        self.tracker = None
        self.picam2 = None
        self.servo_kit = None
        self.current_frame = None
        self.config = None

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
		self.picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": self.size}, transform=Transform(hflip=True, vflip=True)))
		self.picam2.start()




		return self.config  # This value is bound to the 'as' variable



	def get_current_frame(self):


		return


	def get_next_frame(self):


		return


	def get_error(self):

		return


	def update_state(self):

		return

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Clean up the resource, regardless of errors."""
		logger.info("Exiting GimbalConfig")
		self.connection = None

		if exc_type is not None:
			logger.error(f"An error occurred: {exc_val}")
			# Return True to suppress the exception, False to let it propagate
			return False

		logger.info("Closing Window")

