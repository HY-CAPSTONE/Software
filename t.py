import socket
import time
import picamera

# make socket
# bind 
# listen
# accept
# write


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind(('0.0.0.0', 8000))
serv_sock.listen(10)

while True:
	connection = serv_sock.accept()[0].makefile('wb')
	try:
		with picamera.PiCamera(resolution="640x480", framerate=24) as camera:
			camera.start_preview()
			time.sleep(2)

			camera.start_recording(connection, format='h264')
			while True:
				camera.wait_recording(10)
	except socket.error as  e:
		print ("client disconnect")
	
	finally:
		try:
			connection.close()
		except socket.error as e:
			print ("connection close error")
		serv_sock.close()
