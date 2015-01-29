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

import os
import serial
import sys
import time
from util import path_filter, log_to_file

class LightNotConnected(Exception): pass

class Light(object):
	"""
	Controller for room lights.
	"""
	def __init__(self):
		path = "/dev/"
		light_controller_list = path_filter("/dev/", "ACM")
		if len(light_controller_list)  != 1:
			print "I don't know which light controller to open"
			raise LightNotConnected()
		
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

	def sevlev(self):
		"""
		Query the light controller about some sevlevin.
		Returns True if there is an unacknowledged 7.
		Returns False if no pending 7 or no response.
		"""
		l = self.serial
		l.flushInput()
		l.write('7')
		time.sleep(.5)
		if(l.inWaiting()):
			res = l.readline()
			log_to_file('711.recv.{}\n'.format(res[0]))

			seven_received = res[0] == '7'
			log_to_file(seven_received)
			return seven_received
		else:
			return False


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
