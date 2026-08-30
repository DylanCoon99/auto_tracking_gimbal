import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

# this is the file that will interface with the servos
# this will be transparent to my main code



'''
MIN_US = 500
MAX_US = 2500
PERIOD_US = 1_000_000 / pca.frequency


def set_angle(channel: int, angle: float) -> None:
    angle = max(0.0, min(180.0, angle))
    pulse_us = MIN_US + (MAX_US - MIN_US) * (angle / 180.0)
    pca.channels[channel].duty_cycle = int(pulse_us / PERIOD_US * 0xFFFF)
'''

def servo_kit_setup(channels, address):

	kit = ServoKit(channels=channels, address=address)

	TILT = 0    # PCA9685 channel index for the pan axis
	PAN = 1   # PCA9685 channel index for the tilt axis

	# Calibrate to the specific servo. Many hobby servos require a wider
	# range than the library default of 750-2250 us to reach full travel.
	for ch in (PAN, TILT):
		kit.servo[ch].set_pulse_width_range(500, 2500)
		kit.servo[ch].actuation_range = 180
		kit.servo[ch].angle = 0

	return kit


def update_servos(kit, error, kp, kd, PAN=0, TILT=1):

	# determine change in x, y (PAN, TILT)
	(dx, dy) = (kp * error[0], kp * error[1])

	# determine absolute angles for servos and update
	kit.servo[PAN].angle = max(0, min(180, kit.servo[PAN].angle - dx)) # this works
	kit.servo[TILT].angle = max(0, min(180, kit.servo[TILT].angle - dy))

	return


def reset(kit):

	kit.servo[0].angle = 0
	kit.servo[1].angle = 65

	return