#from src.testing import main
from src.config import GimbalConfig




# instantiate a logger






def main():


	with GimbalConfig() as gc:
		gc.run()



	# instantiate the tracking loop

	# on each iteration

		# get the next bbox

		# measure the error for the current state of the gimbal

		# move the gimbal to the next state


	return






if __name__ == "__main__":
    main()