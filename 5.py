# music player simulator

import asyncio
import os

class player():
	def __init__(self):
		self.stop_var = 0
		self.indicate_var = 13
		self.loop = asyncio.get_event_loop()
		print("self.loop created")
		task = self.loop.create_task(self.client())
		
		task = self.loop.create_task(self.pl_song())
		self.loop.create_task(task)
		print("task play song created")
		self.loop.create_task(self.__loop())
		print("task _loop created")
		print("self.loop runned")
		self.loop.run_until_complete(task)
		self.loop.close()
		print("loop closed")
		
	async def pl_song(self):
		print("Play song: Started")
		print("Play song: End")
		
	async def __loop(self):
		print("Loop: Started")
		while True:
			if self.indicate_var == self.stop_var:
				break
		print("Loop: End")
		
	async def client(self):
		print("Client: Start")
		for i in range(1,5):
			print("Client: /")
			await asyncio.sleep(1)
		print("Client: End")
		
player()	