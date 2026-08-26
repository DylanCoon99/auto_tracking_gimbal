from gpiozero import Servo
from time import sleep


def main():

	# Initialize servo on GPIO 18
	servo = Servo(18)

	try:
		while True:
			servo.min()  # Move to minimum position (-1)
			sleep(1)
			servo.mid()  # Move to middle position (0)
			sleep(1)
			servo.max()  # Move to maximum position (1)
			sleep(1)
	finally:
		servo.detach()

	return