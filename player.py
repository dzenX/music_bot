import asyncio

from discord import Client

from utils import valid_server


def serverid(func):
	def wrap(self, server=None, *args, **kwargs):
		print(server)
		print(*args, '---', **kwargs)
		if server:
			server = valid_server(server)
		func(self, server=server, *args, **kwargs)

	return wrap


def getplayer(func):
	def wrap(self, server=None, player=None):
		print(server, player)
		if not player and not server:
			return
		elif server:
			player = self.get_player(valid_server(server))
			if not player:
				return
		print(player)
		func(self, player=player)

	return wrap


class Play:
	Players = {}

	def __init__(self, client):
		self.client = client

	@serverid
	def get_player(self, server):
		print(self.Players.get(server))
		return self.Players.get(server)

	def _set_player(self, server_id, player):
		self.Players[server_id] = player

	def _remove_player(self, server_id):
		return self.Players.pop(server_id, None)

	async def _create_player(self, server_id, url):
		server = Client.get_server(self.client, server_id)
		if not server:  # Log cant find server
			return
		return await Client.voice_client_in(self.client, server).create_ytdl_player(url)

	@serverid
	def start(self, server=None, player=None):
		if not player:
			player = self.get_player(server)
			if not player:
				return False
		player.start()
		return True

	@getplayer
	def stop(self, server=None, player=None):
		print(server, player)
		player.stop()

	@serverid
	def resume(self, server=None, player=None):
		if not player:
			player = self.get_player(server)
		player.resume()

	@serverid
	def pause(self, server=None, player=None):
		if player:
			player.pause()
		else:
			player = self.get_player(server)
			player.pause()

	@staticmethod
	async def timer(client, channel):
		message = 'Your song starts in: 10'
		curr_msg = await Client.send_message(client, channel, message)
		for i in range(1, 10):
			await asyncio.sleep(1)
			message = 'Your song starts in: {}'.format(10 - i)
			await Client.edit_message(client, curr_msg, message)
		await asyncio.sleep(1)
		message = 'BOOOOOOOM!!!!'
		await Client.edit_message(client, curr_msg, message)
		await Client.delete_message(client, curr_msg)
