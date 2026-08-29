import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

# this is the file that will interface with the servos
# this will be transparent to my main code


i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x40)
pca.frequency = 50

MIN_US = 500
MAX_US = 2500
PERIOD_US = 1_000_000 / pca.frequency


def set_angle(channel: int, angle: float) -> None:
    angle = max(0.0, min(180.0, angle))
    pulse_us = MIN_US + (MAX_US - MIN_US) * (angle / 180.0)
    pca.channels[channel].duty_cycle = int(pulse_us / PERIOD_US * 0xFFFF)


def sweep(channel, start, end, step=1.0, delay=0.02):
    direction = 1 if end > start else -1
    angle = start
    while (angle - end) * direction < 0:
        set_angle(channel, angle)
        angle += step * direction
        time.sleep(delay)
    set_angle(channel, end)


def main():
    kit = ServoKit(channels=16, address=0x40)

    TILT = 0    # PCA9685 channel index for the pan axis
    PAN = 1   # PCA9685 channel index for the tilt axis

    # Calibrate to the specific servo. Many hobby servos require a wider
    # range than the library default of 750-2250 us to reach full travel.
    for ch in (PAN, TILT):
        kit.servo[ch].set_pulse_width_range(500, 2500)
        kit.servo[ch].actuation_range = 180

    for i in range(3):
	    kit.servo[PAN].angle = 90     # center
	    kit.servo[TILT].angle = 90     # center
	    time.sleep(1)
	    kit.servo[PAN].angle = 45
	    kit.servo[TILT].angle = 45
	    time.sleep(1)
	    kit.servo[PAN].angle = 135
	    kit.servo[TILT].angle = 135
	    time.sleep(1)
	    kit.servo[PAN].angle = 90
	    kit.servo[TILT].angle = 90

