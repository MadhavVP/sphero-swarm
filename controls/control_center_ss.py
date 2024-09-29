# import socket programming library
import socket

# import thread module
from _thread import *
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISC_MSG = '!DISC!'


def handle_client(conn, addr):
	print(f"Connected {addr}")
	connected = True
	while connected:
		msg = input("> ")		
		if msg == DISC_MSG:
			connected = False
		print(f"[{addr}] {msg}")
		conn.send(msg.encode(FORMAT))

def Main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(ADDR)
	server.listen(5)
	print(f"Listening on {IP}:{PORT}")

	while True:
		con, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(con, addr))
		thread.start()



if __name__ == '__main__':
	Main()
