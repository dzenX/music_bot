import asyncio
import os


#
# 1.py только обернут в клас + тестовая ггвп
#


class goo():
	def __init__(self):
		os.system('cls')
		self.g = 13
		self.loop = asyncio.get_event_loop()
		tasks = [self.loop.create_task(self.fo()), self.loop.create_task(self.bar())]
		wait_tasks = asyncio.wait(tasks)
		self.loop.run_until_complete(wait_tasks)
		self.loop.close()

	async def fo(self):
		print('FO: Running in foo')
		while True:
			if self.g == 0:
				break
			print('FO: ' + str(self.g))
			await asyncio.sleep(1)
		print('FO: Explicit context switch to foo again')

	async def gg_wp(self):
		print('GGWP: Running')
		for x in range(1,10):
			print('GGWP: '+ str(x))
			await asyncio.sleep(1)

	async def bar(self):
		print('BAR: Running in BAR')
		await asyncio.sleep(5)
		self.g = 0
		print('BAR: Implicit context switch back to bar')
		await self.gg_wp()
		print('BAR: ggwp')

goo()