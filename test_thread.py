# thread TEST

import threading
import time

class Worker(threading.Thread):
	def __init__(self, name):
		super().__init__()
		self.name = name
	def run(self):
		for i in range(10):
			print("this is sub thread")
			time.sleep(1)


print("main start")

name = "aaaaa"
t = Worker(name)
t.daemon = True
t.start()

for i in range(100):
	print("maining")
	time.sleep(0.1)

print("main end")
