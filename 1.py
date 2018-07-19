import asyncio
import os
g = 13
async def foo():
	print('Running in foo')
	while True:
		global g
		if g == 0:
			break
		print(g)
		await asyncio.sleep(1)
	print('Explicit context switch to foo again')


async def bar():
	global g
	print('Explicit context to bar')
	await asyncio.sleep(5)
	g = 0
	print('Implicit context switch back to bar')

os.system('cls')
ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()