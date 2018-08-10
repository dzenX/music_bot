from threading import Thread
from time import sleep


class MyThread(Thread):

	def __init__(self, st):
		Thread.__init__(self)
		self.st = st

	def run(self):
		for i in range(20):
			print(self.st + '--' + str(i))
			sleep(0.222)


c = MyThread('11')
b = MyThread('222222')
# b.daemon = True
c.start()
sleep(2)
b.start()
c.join()
print("finish")
