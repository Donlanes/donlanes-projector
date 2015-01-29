"""
Lounge Light Controller

Command Line Usage:
	python light.py on
	python light.py off

Python Usage:
	l = Light()
	l.set_state(True)  # turns lights on
	l.set_state(False) # turns lights off
"""

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
		
		light_controller = light_controller_list[0]
		BAUDRATE = 9600

		self.serial = serial.Serial(port=light_controller, baudrate=BAUDRATE)

	def set_state(self, state):
		""" `state` must be boolean """
		code = {
			True: '0',
			False: '1',
		}
		self.serial.write(code[state])
		self.serial.flushInput()
		self.serial.close()


if __name__ == '__main__':
	l = Light()
	YES = ['true', 'yes', 'on', '1']
	NO = ['false', 'no', 'off', '0']
	print "Would you like to turn the lights on or off?"

	if len(sys.argv) == 2:
		command = sys.argv[1].lower()
		print ">", command
	else:
		command = raw_input("> ").lower()

	if command in YES:
		print "turning on"
		l.set_state(True)
	elif command in NO:
		print "turning off"
		l.set_state(False)
	else:
		print "huh?"
