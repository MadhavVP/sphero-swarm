import socket
from spherov2 import scanner # turning works on relative direction, need to update code to match
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import multiprocessing
import threading
import time
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISC_MSG = '!DISC!'

def Main():
	toy = scanner.find_toy()
	with SpheroEduAPI(toy) as api:
        try:
            api.calibrate_compass()
        except:
            print("error")
            sys.exit()
			
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		# connect to server on local computer
		client.connect(ADDR)
		print(f"Connected {IP}:{PORT}")
		connected = True
		msg = "RECIEVED"
		controlQueue = []
		while connected:

			data = client.recv(1024)
			serverMsg = data.decode('ascii')
			if serverMsg == "STOP":
				break
			controlQueue.append(serverMsg)
			print(serverMsg)
			client.send(msg.encode('ascii'))
			
		# close the connection
		s.close()

if __name__ == '__main__':
	Main()
