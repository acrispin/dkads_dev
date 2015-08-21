# logginghandler
from datetime import datetime

PATH_LOG_FILE = "logs/info.log"

cad_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getFileName():
	cad_period = datetime.now().strftime("%Y-%m-%d")
	return PATH_LOG_FILE + "." + cad_period

def info(msg):
	cad_time = datetime.now().strftime("%H:%M:%S")
	msg_format = "Time {0} : INFO {1}\n".format(cad_time,msg)
	with open(getFileName(), "a") as f:
		f.write(msg_format)

def error(msg):
	cad_time = datetime.now().strftime("%H:%M:%S")
	msg_format = "Time {0} : ERROR {1}\n".format(cad_time,msg)
	with open(getFileName(), "a") as f:
		f.write(msg_format)

def debug(msg):
	cad_time = datetime.now().strftime("%H:%M:%S")
	msg_format = "Time {0} : DEBUG {1}\n".format(cad_time,msg)
	with open(getFileName(), "a") as f:
		f.write(msg_format)
	
#info("info de test")
#print 'logger iniciado'

# to call methos from this module in others
# import logginghandler as mylogger
