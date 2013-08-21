import serial, sys, re, os, argparse, time
from Tkinter import *

COMMANDS = {
	'ON': '\x02\x00\x00\x00\x00\x02',
	'OFF': '\x02\x01\x00\x00\x00\x03',

	'RGB1': '\x02\x03\x00\x00\x02\x01\x01\x09',
	'RGB2': '\x02\x03\x00\x00\x02\x01\x02\x0a',
	'VIDEO': '\x02\x03\x00\x00\x02\x01\x06\x0e',
	'SVIDEO': '\x02\x03\x00\x00\x02\x01\x0b\x13',
	'DVI': '\x02\x03\x00\x00\x02\x01\x1a\x22',
	'VIEWER':'\x02\x03\x00\x00\x02\x01\x1f\x27',
	'PIC_MUTE_ON':'\x02\x10\x00\x00\x00\x12',
	'PIC_MUTE_OFF':'\x02\x11\x00\x00\x00\x13',
	'SOUND_MUTE_ON':'\x02\x12\x00\x00\x00\x14',
	'SOUND_MUTE_OFF':'\x02\x13\x00\x00\x00\x15',
	'ON_SCREEN_MUTE_ON':'\x02\x14\x00\x00\x00\x16',
	'ON_SCREEN_MUTE_OFF':'\x02\x15\x00\x00\x00\x17'
}

path = '/dev'
dirList = os.listdir(path)


def filterPicker(lines,regex):
	result = []
	for l in lines:
		match = re.search(regex,l)
		if match:
			result +=[l]
	return result


	lightList = filterPicker(dirList,'ACM')
	if len(lightList)==0:
		lights = path+'/'+filterPicker(dirList,'ACM')[0]
		
def main():
	desc = "Control the lounge NEC projector"
	portList = filterPicker(dirList,'USB')
	if len(portList)==0:
		root = Tk()
		root.title('**PROJECTOR ALERT**')
		Message(root, text="**ALERT** \n \n The USB cable to the projector may be unplugged or need to be reset.  Please unplug the 'BLUE' USB cable from the back of donlanes (This computer) and plug it back in.\n \n Thank you", bg='black',fg='white', relief=GROOVE).pack(padx=30, pady=10)
		root.mainloop()
	else:
		port = path+'/'+filterPicker(dirList,'USB')[0]

	command = sys.argv[1]
	baudrate = 9600
	lightList = filterPicker(dirList,'ACM')
	if len(lightList)!=0:
		lights = path+'/'+filterPicker(dirList,'ACM')[0]
		l= serial.Serial(port=lights,baudrate=baudrate)
		time.sleep(.5)
		if(command == 'ON'):
			l.write('1')
		if(command == 'OFF'):
			l.write('0')

	s = serial.Serial(port=port,baudrate=baudrate)
	s.write(COMMANDS[command])

if __name__ == '__main__':
	main()



