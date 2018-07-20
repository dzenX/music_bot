import asyncio
import os

class goo():
	def __init__(self):
		os.system('cls')
		self.g = 13
		self.loop = asyncio.get_event_loop()
		self.loop2= asyncio.get_event_loop()
		tasks = [self.loop.create_task(self.fo()), self.loop.create_task(self.bar())]
		wait_tasks = asyncio.wait(tasks)
		self.loop.run_until_complete(wait_tasks)
		self.loop.close()

	async def fo(self):
		print('FO: Start')
		while True:
			if self.g == 0:
				break
			print('FO: ' + str(self.g))
			await asyncio.sleep(1)
		print('FO: End')

	async def gg_wp(self):
		print('GGWP: Start')
		for x in range(1,10):
			print('GGWP: '+ str(x))
			#await asyncio.sleep(1)
		print('GGWP: End')

	async def bar(self):
		print('BAR: Running in BAR')
		await asyncio.sleep(5)
		self.g = 0
		print('BAR: G=0')
		self.start_l2()
		# await self.gg_wp()
		print('BAR: End')
	def start_l2(self):
		print('ST_L2: Start')
		task = self.loop2.create_task(self.gg_wp())
		wtask = asyncio.wait(task)
		print('ST_L2: ggwp')
		self.loop2.run_until_complete(wtask)
		print('ST_L2: End')



goo()