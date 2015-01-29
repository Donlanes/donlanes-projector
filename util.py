import os
import time
from datetime import datetime

def path_filter(path, text):
	dir_list = os.listdir(path)
	ports = filter(lambda x: text in x, dir_list)
	paths = map(lambda port : os.path.join(path, port), ports)
	return paths

def log_to_file(msg):
	LOGFILE_PATH = '/home/slug/Projector/log.log'
	with open(LOGFILE_PATH, 'a') as logfile:
		preamble = "{} [{}]: ".format(
			datetime.fromtimestamp(time.time()).strftime("%D %H:%M"),
			os.getpid())
		logfile.write("{}{}".format(preamble, msg))
