"""
Controller for lounge NEC Projector.

Command Line Usage:
	python projector.py # Lists options and prompts.
	python projector.py ON
	python projector.py OFF

Python Usage:
	l = Light()
	l.run_cmd('ON')  # Turns the projector on
	l.run_cmd('OFF') # Turns the projector off
"""

import sys
import serial
from util import path_filter

# Projector RS232 control commands.
# See this docunt: bottom of page 10, section 4 "list of commands"
# http://www.necdisplay.com/documents/UserManuals/RS232_PJ_ControlCommands.pdf
# Also see nec-rs232-table.txt for a table of values extracted from that document.
PROJECTOR_COMMANDS = {
	# Projector power
	'ON'                 : '\x02\x00\x00\x00\x00\x02',
	'OFF'                : '\x02\x01\x00\x00\x00\x03',

	# Project input selection
	'RGB1'               : '\x02\x03\x00\x00\x02\x01\x01\x09',
	'RGB2'               : '\x02\x03\x00\x00\x02\x01\x02\x0a',
	'VIDEO'              : '\x02\x03\x00\x00\x02\x01\x06\x0e',
	'SVIDEO'             : '\x02\x03\x00\x00\x02\x01\x0b\x13',
	'DVI'                : '\x02\x03\x00\x00\x02\x01\x1a\x22',
	'VIEWER'             : '\x02\x03\x00\x00\x02\x01\x1f\x27',

	'PIC_MUTE_ON'        : '\x02\x10\x00\x00\x00\x12',
	'PIC_MUTE_OFF'       : '\x02\x11\x00\x00\x00\x13',
	'SOUND_MUTE_ON'      : '\x02\x12\x00\x00\x00\x14',
	'SOUND_MUTE_OFF'     : '\x02\x13\x00\x00\x00\x15',
	'ON_SCREEN_MUTE_ON'  : '\x02\x14\x00\x00\x00\x16',
	'ON_SCREEN_MUTE_OFF' : '\x02\x15\x00\x00\x00\x17'
}

class Projector(object):
	def __init__(self):
		port_list = path_filter("/dev/", "USB")
		if not port_list:
			no_projector_message()
		elif len(port_list) != 1:
			print "WARNING: Multiple potential projector ports detected. Choosing first."
			print port_list
			port = port_list[0]
		else:
			port = port_list[0]
		BAUDRATE = 9600
		self.serial = serial.Serial(port=port, baudrate=BAUDRATE)

	def run_cmd(self, command):
		"""
		Send the projector a command.
		`command` must be a string in PROJECTOR_COMMANDS
		"""
		code = PROJECTOR_COMMANDS[command]
		self.serial.write(code)


if __name__ == '__main__':
	proj = Projector()
	print PROJECTOR_COMMANDS.keys()
	print "What would you like the projector to do?"
	print "Choices are listed above."

	if len(sys.argv) == 2:
		command = sys.argv[1]
		print ">", command
	else:
		command = raw_input("> ")

	if command in PROJECTOR_COMMANDS:
		proj.run_cmd(command)
		print "Command sent."
	else:
		print "Invalid command."
		print "No action taken."
