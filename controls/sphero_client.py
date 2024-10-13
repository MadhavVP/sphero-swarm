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
	toy = scanner.find_toy(toy_name='SB-76B3')
	print(toy)
	with SpheroEduAPI(toy) as api:
		try:
			api.calibrate_compass()
			magBase = api.get_compass_direction()
			client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			direction = 0
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
				if (serverMsg == ('w')):
					# move forward

					api.set_heading(magBase)
					api.set_speed(100)
				elif (serverMsg == ('s')):
					# move back

					api.set_heading(magBase + 180)
					api.set_speed(100)
				elif (serverMsg == ('a')):
					# move left

					api.set_heading(magBase + 270)
					api.set_speed(100)
				elif (serverMsg == ('d')):
					# move right

					api.set_heading(magBase + 90)
					api.set_speed(100)
				elif (serverMsg == ('z')):
					api.set_speed(0)
				# else:
				# 	# stop

				# 	api.set_speed(0)
				if (serverMsg == "CALIBRATE"):
					api.calibrate_compass() # not perfect - need feedback
					magBase = api.get_compass_direction()
					api.set_main_led(choosenColor)
				elif (serverMsg[0] == "M"): #MOVE:XXX:YYY    - Moves in preset direction at XXX speed for YYY seconds
					api.roll(magBase + direction, int(serverMsg[2:4]), float(serverMsg[6:]))
					#time.sleep(0.5)
				elif (serverMsg[0] == "R"): #ROTATE: R:XXX
					direction += int(serverMsg[2:])
                    # probably need to graph sphero turning in order to get a good idea of what the rotate command should be
				elif (serverMsg[0] == "C"): #COLOR CHANGE: C:RRR:GGG:BBB    - sets color to these rgb vals
					choosenColor = Color(r = int(serverMsg[2:4]), g = int(serverMsg[6:8]), b = int(serverMsg[10:12]))
					api.set_main_led(choosenColor)
					api.set_front_led(choosenColor)
					api.set_back_led(choosenColor)
				elif (serverMsg[0] == "D"):
					time.sleep(float(serverMsg[2:]))
				else:
					print(serverMsg + " in ball {} is an invalid command!".format(id))
				
			# close the connection
			s.close()
		except:
			print("error")
			sys.exit()

if __name__ == '__main__':
	Main()
