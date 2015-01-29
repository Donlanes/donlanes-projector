import os, serial, sys
from util import path_filter

class Light(object):
	"""
	Controller for room lights.
	"""
	def __init__(self):
		path = "/dev/"
		light_controller_list = path_filter("/dev/", "ACM")
		if len(light_controller_list)  != 1:
			print "I don't know which light controller to open"
			sys.exit(1)
		
		self.light_controller = light_controller_list[0]
		self.state = False

	@property
	def state(self):
		return self.state

	@state.setter
	def set_state(self, state):
		self.state = state

		l = serial.Serial(port=light_controller, baudrate=baudrate)
		l.write(str(int(state)))
		l.write()
		l.flushInput()
		l.close()


if __name__ == '__main__':
	# Example Usage:
	l = Light()
	l.state = False # turns lights off
	l.state = True # turns lights on
