from contextlib import suppress
import socket
import time
import picamera
import threading

# make socket
# bind 
# listen
# accept
# write

def Videostreaming(camera, connection):
	try:
		print("start thread")
		camera.start_preview()
		time.sleep(2)
		camera.start_recording(connection, format='h264')
		while True:
			camera.wait_recording(10)
	except socket.error as e:
		print("term thread")
		camera.stop_recording()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
#	serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv_sock.bind(('0.0.0.0', 8000))
	serv_sock.listen(10)
	with picamera.PiCamera(resolution="640x480", framerate=24) as camera:
		camera.start_preview()
		time.sleep(1)
		while True:
			print("start loop")
			connection = serv_sock.accept()[0].makefile('wb')
			print("connection accepted")
			th1 = threading.Thread(target=Videostreaming , args=(camera, connection))
			th1.start()
			th1.join()
			print('join succeed')
			#camera.stop_recording()
			#connection.close()
			#camera.stop_recording()
			

