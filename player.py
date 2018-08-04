import asyncio

from discord import Client

from utils import valid_server


def serverid(func):
	"""
		Decorator for class methods to transform incoming Server object to string with his Server.id.
		It will search for Server in kwargs: func(server=Server_Obj/Server_Id).
		If dont exist it'll try to transform first incoming argument except 'self': self.method(server).
		If first argument isnt Server_Obj it wont change anything.
		:return: It calls decorated function with changed arguments
	"""

	def serverid_wrap(self, *args, **kwargs):
		server = kwargs.get('server')
		if not server:
			if args:
				argz = list(args)
				argz[0] = valid_server(argz[0])
				args = tuple(argz)
		else:
			kwargs['server'] = valid_server(server)
		func(self, *args, **kwargs)

	return serverid_wrap


def getplayer(func):
	"""
		Decorator for class Play  methods to get 'player' object to function if it accept just 'server' or 'server_id'
		Itll search for server or player in kwargs if 'player' found  it will just pass it to decorated method.
		Else if atleast 'server' found, it will use 'get_method' method from class Play to get player
		and then will pass to decorated method.
	"""

	def getplayer_wrap(self, *args, **kwargs):
		server = kwargs.get('server')
		player = kwargs.get('player')
		if not player and not server:
			return
		elif not player and server:
			player = self.get_player(valid_server(server))
			if player:
				kwargs['player'] = player
		func(self, *args, **kwargs)

	return getplayer_wrap


class Play:
	Players = {}

	def __init__(self, client):
		self.client = client

	def _get_player(self, server_id):
		"""
			Method to get player object assotiated with given server id from list

		:param server_id: Takes string with server id
		:return: Player object assotiated with given server id if exist. Else - None
		"""
		return self.Players.get(server_id)

	def _set_player(self, server_id, player):
		"""
			Method to save given player assotiated with given server id to list

		:param server_id: Takes string with server id
		:param player:  Takes player object. You can generate it with '_create_player_method'
		:return: None
		"""
		self.Players[server_id] = player

	def _remove_player(self, server_id):
		"""
			Method to remove player assotiated with given server id object from list

		:param server_id: Takes string with server id
		:return: Returns player object for given server id if exist. Else - None
		"""
		return self.Players.pop(server_id, None)

	async def _create_youtube_player(self, server_id, url):
		"""
			Method to create player object for given server with given youtube url

		:param server_id: Takes string with server id
		:param url: Takes youtube solo song or playlist urk
		:return: Returns generated player object
		"""
		server = Client.get_server(self.client, server_id)
		if not server:  # Log cant find server
			return
		return await Client.voice_client_in(self.client, server).create_ytdl_player(url)

	#########################################
	#
	#   Public memner methods
	#
	#########################################
	@serverid
	def get_player(self, server):
		"""
			Public method to get player object assotiated with given server from list

		:param server: Takes server object ot just server id string
		:return: Returns player object if exist. Else - None
		"""
		return self._get_player(server)

	@getplayer
	def start(self, server=None, player=None):
		if player:
			player.start()
			return True

	@getplayer
	def stop(self, server=None, player=None):
		if player:
			player.stop()
			return True

	@getplayer
	def resume(self, server=None, player=None):
		if player:
			player.resume()
			return True

	@getplayer
	def pause(self, server=None, player=None):
		if player:
			player.pause()
			return True

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
