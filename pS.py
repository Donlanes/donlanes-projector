import serial, sys, re, os, argparse, time
from Tkinter import *
from datetime import datetime
from util import path_filter

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




def sevlev_mail():
	print "sending 711 email"
	import smtplib, string, time

#	from email.MIMEMultipart import MIMEMultipart
#	from email.MIMEText import MIMEText
#	from email.MIMEImage import MIMEImage
#
#	# check to see when the last time the button was pressed
#	lastTime = os.path.getmtime('/home/slug/Projector/sevenElevenTouch')
#	
#	print (time.time() - lastTime)
#	os.system("streamer -c /dev/video0 -b 32 -s 640x480 -o 7-eleven.jpeg")
#	if (time.time() - lastTime) > 60:
#		os.system("touch /home/slug/Projector/sevenElevenTouch")
#		
#		# always take a picture as soon as the button is pressed
#		# take a photo with the camera
#		
#		
#		# rotate the image and draw a box around the button-presser
#		os.system('convert 7-eleven.jpeg -rotate -90 -fill none -stroke red -strokewidth 5 -draw "rectangle 250,200,450,450" 7-eleven2.jpeg')
#
#		# Send an HTML email with an embedded image and a plain text message for
#		# email clients that don't want to display the HTML.
#
#	
#
#		# Define these once; use them twice!
#		strFrom = '7-eleven@mit.edu'
#		strTo = '7-eleven@mit.edu'
#
#		# Create the root message and fill in the from, to, and subject headers
#		msgRoot = MIMEMultipart('related')
#		msgRoot['host'] = 'outgoing.mit.edu'
#		msgRoot['Subject'] = '[7-eleven] Now, Goodale <eom>'
#		msgRoot['From'] = strFrom
#		msgRoot['To'] = strTo
#		msgRoot.preamble = 'This is a multi-part message in MIME format.'
#
#		# Encapsulate the plain and HTML versions of the message body in an
#		# 'alternative' part, so message agents can decide which they want to display.
#		msgAlternative = MIMEMultipart('alternative')
#		msgRoot.attach(msgAlternative)
#
#		msgText = MIMEText('')
#		msgAlternative.attach(msgText)
#
#		# We reference the image in the IMG SRC attribute by the ID we give it below
#		msgText = MIMEText('<img src="cid:image1">', 'html')
#		msgAlternative.attach(msgText)
#
#		# This example assumes the image is in the current directory
#		fp = open('7-eleven3.jpeg', 'rb')
#		msgImage = MIMEImage(fp.read())
#		fp.close()
#
#		# Define the image's ID as referenced above
#		msgImage.add_header('Content-ID', '<image1>')
#		msgRoot.attach(msgImage)
#
#		# Send the email (this example assumes SMTP authentication is required)
#		server = smtplib.SMTP(msgRoot["host"])
#		server.sendmail(strFrom, strTo, msgRoot.as_string())
#		server.quit()
#
#		 "subject": "[7-eleven] Now, Goodale (" + str(int(time.mktime(time.gmtime()))) + ") <eom>",

	msg = {
		"host": "outgoing.mit.edu",
		"subject": "[7-eleven] Now, Goodale <eom>",
		"from": "7-eleven@mit.edu",
		"to": ["7-eleven@mit.edu"],
		"body": '' }
	
	
	msg_raw = string.join((
		"From: %s" % msg["from"],
		"To: %s" % ', '.join(msg["to"]),
		"Subject: %s" % msg["subject"] ,
		"",
		msg["body"]
		), "\r\n")
	
	server = smtplib.SMTP(msg["host"])
	server.sendmail(msg["from"], msg["to"], msg_raw)
	server.quit()

def no_projector_message():
	root = Tk()
	root.title('**PROJECTOR ALERT**')
	Message(root, text="**ALERT** \n \n The USB cable to the projector may be unplugged or need to be reset.  Please unplug the 'BLUE' USB cable from the back of donlanes (This computer) and plug it back in.\n \n Thank you", bg='black',fg='white', relief=GROOVE).pack(padx=30, pady=10)
	root.mainloop()



def main():
	desc = "Control the lounge NEC projector"
	port_list = path_filter("/dev/", "USB")
	if not port_list:
		projector_message()
	else:
		port = port_list[0]

	command = sys.argv[1]
	baudrate = 9600
	light_controller_list = path_filter("/dev/", "ACM")
	if light_controller_list:
		light_controller = light_controller_list[0]
		l = serial.Serial(port=light_controller, baudrate=baudrate)
		time.sleep(.5)
		if command == 'ON' :
		        l.write('1')
		elif command == 'OFF' :
		      l.write('0')
		elif command == '711':
			# file = open('/home/slug/Projector/log.log', 'w')
			# file.write('711.check\n')
			
			l.flushInput()
			l.write('7')
			time.sleep(.5)
			if(l.inWaiting()):
				res = l.readline()
				print res
				if (res[0] == '7'):
					sevlev_mail()
                if(command == '711-force'):
                        sevlev_mail()

	if (COMMANDS.has_key(command)):
		s = serial.Serial(port=port,baudrate=baudrate)
		s.write(COMMANDS[command])

if __name__ == '__main__':
	main()