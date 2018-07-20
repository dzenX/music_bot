import asyncio
import os
#
# Траю теорию
#


class goo():
	def __init__(self):
		#os.system('cls')
		self.g = 13
		self.stop = 0
		self.loop = asyncio.get_event_loop()
		#self.loop2= asyncio.get_event_loop()
		self.tasks = [self.loop.create_task(self.fo()), self.loop.create_task(self.bar())]
		wait_tasks = asyncio.wait(self.tasks)
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
			await asyncio.sleep(2)
		# while True:
		# 	if self.stop == 1:
		# 		break
		print('GGWP: End')

	async def bar(self):
		print('BAR: Running in BAR')
		#await self.start_l2()
		#asyncio.ensure_future(self.gg_wp(),loop = self.loop)
		await asyncio.sleep(4)
		self.g = 0
		print('BAR: G=0')
		task = self.loop.create_task(self.gg_wp())
		print('BAR: TASK')
		self.tasks.append(task)
		print('BAR: append')
		asyncio.wait(self.tasks)
		print('BAR: await')
		self.stop = 1
		
		
		# await self.gg_wp()
		print('BAR: End')

	async def start_l2(self):
		print('ST_L2: Start')
		#self.loop.create_task(self.gg_wp())
		#wtask = asyncio.wait(task)
		print('ST_L2: ggwp')
		#self.loop2.run_until_complete(wtask)
		print('ST_L2: End')



goo()