import socket
import random
from proto3f import recognition
def getSerial():
        serial = "0"
        try:
                file = open ('/proc/cpuinfo','r')
#                print('found it')
                for lines in file:
                        #p = file.readline()
                        if lines[0:6]=='Serial':
                                serial=lines[10:26]
                file.close()
        except:
                serial = "ERROR"
        return serial


SERIAL = str(getSerial())
TCP_IP = 'Ameens-Macbook-Air.local'
TCP_PORT =5005
BUFFER = 1024
MESSAGE = 'REQUESTING CONNECTION'
MESSAGE = MESSAGE.encode()
THRESHOLD = 0.451
#MESSAGE = 'REQUESTING CONNECTION'
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
s.send(MESSAGE)
EXIT=0
#MATCHY= 'MATCH'
USER_REQUESTED =0
im = '/media/ameen/B301-16DE/IITD Database/001/02_L.bmp' #2,4 JUNK 9 needs bigg$
#template = 'codes/CODE1_L.bmp'
USER_NUMBER=0
SESSION_REQUEST=False
SEED = ""
ID = ""
FIRST = ""
SECOND = ""
THIRD = ""

while True:
	data=s.recv(BUFFER).decode() #response from PC
	print('PC RESPONSE: ',data)
	if data=='ACK' and USER_REQUESTED==0:
		MESSAGE = SERIAL #'SENDING SERIAL NUMBER...'
	elif data== 'VERIFIED SERIAL NUMBER':
		MESSAGE = 'SESSION REQUEST'
		SESSION_REQUEST=True
	elif SESSION_REQUEST==True:
		SEED = int(data)
		random.seed(SEED-1)
		FIRST = str(int(1000*random.random()))
		random.seed(SEED)
		SECOND = str(int(1000*random.random()))
		random.seed(SEED+1)
		THIRD = str(int(1000*random.random()))
		ID = FIRST+SECOND+THIRD
		MESSAGE = ID
		print('ID: ',ID)
		SESSION_REQUEST=False
	elif data == 'SESSION ID CONFIRMED':
		MESSAGE = 'USER NUMBER?'
		#EXIT=1
		USER_REQUESTED=1
	elif USER_REQUESTED ==1 and  data.isnumeric():
		USER_NUMBER  = str(data)
		print('VERIFYING...')
		#im = '/media/ameen/B301-16DE/IITD Database/001/02_L.bmp' #2,4 JUNK 9 needs bigg$
		template = 'codes/CODE'+USER_NUMBER+'_L.bmp'
		HD,found = recognition(im,template,1,0)
		if HD<=THRESHOLD:
			MESSAGE = 'MATCH'
		elif HD>THRESHOLD:
			MESSAGE = 'NOT MATCH'
	elif data == 'ACCESS GRANTED':
		print(':)')
		EXIT=1
	elif data=='ACCESS DENIED':
		print('IMPOSTER')
		EXIT=1

	else:
		MESSAGE = ':('
		EXIT=1
	if EXIT==1:
		break

	MESSAGE=MESSAGE.encode()
	s.send(MESSAGE)
print('DONE')
s.close()
