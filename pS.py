"""
Controls room lights and the lounge NEC projector
Possibly other things.
"""
import serial, sys, re, os, argparse, time
from Tkinter import *
from util import path_filter, log_to_file
from projector import Projector, ProjectorNotConnected
from light import Light, LightNotConnected

ENABLE_SEVLEV_EMAIL = False

def send_sevlev_mail():
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

	time_str = time.strftime("%Y-%m-%d %I:%M %p", time.localtime())

	msg = {
		"host": "outgoing.mit.edu",
		"subject": "[7-eleven] Sevlev! Leaving from Goodale",
		"from": "711-button@mit.edu",
		"to": ["7-eleven@mit.edu"],
		"body": time_str + "\nAdd or remove yourself: https://groups.mit.edu/webmoira/list/7-eleven",
	}

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
	msg = "**ALERT** \n \n The USB cable to the projector may be unplugged or need to be reset.  Please unplug the 'BLUE' USB cable from the back of donlanes (This computer) and plug it back in.\n \n Thank you"
	Message(root, text=msg, bg='black', fg='white', relief=GROOVE).pack(padx=30, pady=10)
	root.mainloop()

def get_last_email_sent_time():
	try:
		with open('last_sent_time', 'r') as f:
			return int(f.read())
	except IOError:
		return 0

def save_last_email_sent_time():
	with open('last_sent_time', 'w') as f:
		f.write(str(int(time.time())))

def main():
	try:
		projector = Projector()
	except ProjectorNotConnected:
		no_projector_message()
		sys.exit(-1)

	light = Light()

	if len(sys.argv) <= 1:
		print "Command required."
		sys.exit(-1)
	command = sys.argv[1]

	time.sleep(.5)

	# Control light.
	if command == 'ON' :
		light.set_state(False)
	elif command == 'OFF' :
		light.set_state(True)
	elif command == '711':
		if not ENABLE_SEVLEV_EMAIL:
			log_to_file('711.mail.disabled\n')

		if light.sevlev() and ENABLE_SEVLEV_EMAIL:
			SEVLEV_EMAIL_INTERVAL = 30*60 # 30 minutes
			if int(time.time()) - get_last_email_sent_time() > SEVLEV_EMAIL_INTERVAL:
				log_to_file('711.mail.sending\n')
				send_sevlev_mail()
				save_last_email_sent_time()
			else:
				log_to_file('711.mail.ignoring\n')
	elif (command == '711-force'):
		send_sevlev_mail()

	# Control projector.
	if projector.is_valid_cmd(command):
		projector.run_cmd(command)

if __name__ == '__main__':
	main()
