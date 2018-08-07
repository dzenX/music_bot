import asyncio

from discord import Client

from utils import valid_server


# def serverid(func):
# 	"""
# 		Decorator for class methods to transform incoming Server object to string with his Server.id.
# 		It will search for Server in kwargs: func(server=Server_Obj/Server_Id).
# 		If dont exist it'll try to transform first incoming argument except 'self': self.method(server).
# 		If first argument isnt Server_Obj it wont change anything.
# 	"""
#
# 	def serverid_wrap(self, *args, **kwargs):
# 		server = kwargs.get('server')
# 		if not server:
# 			if args:
# 				argz = list(args)
# 				argz[0] = valid_server(argz[0])
# 				args = tuple(argz)
# 		else:
# 			kwargs['server'] = valid_server(server)
# 		func(self, *args, **kwargs)
#
# 	return serverid_wrap


# def getplayer(func):
# 	"""
# 		Decorator for class Play  methods to get 'player' object to function if it accept just 'server' or 'server_id'.
# 		Itll search for server or player in kwargs if 'player' found  it will just pass it to decorated method.
# 		Else if atleast 'server' found, it will use 'get_method' method from class Play to get player
# 		and then will pass to decorated method.
# 	"""
#
# 	def getplayer_wrap(self, *args, **kwargs):
# 		server = kwargs.get('server')
# 		player = kwargs.get('player')
# 		if not player and not server:
# 			return
# 		elif not player and server:
# 			player = self.get_player(valid_server(server))
# 			if player:
# 				kwargs['player'] = player
# 		func(self, *args, **kwargs)
#
# 	return getplayer_wrap


class Player:
	Players = {}

	def __init__(self, client):
		self.Client = client

	def _get_player(self, server_id):
		"""
			Method to get player object assotiated with given server id from list.

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
			Method to remove player assotiated with given server id object from list.

		:param server_id: Takes string with server id
		:return: Player object for given server id if exist. Else - None
		"""
		return self.Players.pop(server_id, None)

	async def _create_youtube_player(self, server_id, url):
		"""
			Method to create player object for given server with given youtube url.

		:param server_id: Takes string with server id
		:param url: Takes youtube solo song or playlist urk
		:return: Generated player object
		"""
		server = self.Client.get_server(server_id)
		if not server:  # Log cant find server
			return
		return await self.Client.voice_client_in(server).create_ytdl_player(url)

	def _start(self, server_id):
		"""
			Method to start player associated with given server id.
			Call it if u are sure that player for gived server id exist and not started yet.

		:param server_id: Takes string with server id
		:return: None
		"""
		self._get_player(server_id).start()

	def _stop(self, server_id):
		"""
			Method to stop player associated with given server id.
			Call it if u are sure that player for gived server id exist and not player.is_done().

		:param server_id: Takes string with server id
		:return: None
		"""
		self._get_player(server_id).stop()

	def _resume(self, server_id):
		"""
			Method to resume player associated with given server id.
			Call it if u are sure that player for gived server id exist and player.is_playing().

		:param server_id: Takes string with server id
		:return: None
		"""
		self._get_player(server_id).resume()

	def _pause(self, server_id):
		"""
			Method to resume player associated with given server id.
			Call it if u are sure that player for gived server id exist and
			not player.is_playing() and not player.is_done().

		:param server_id: Takes string with server id
		:return: None
		"""
		self._get_player(server_id).pause()

	def _action(self, server_id, action):
		"""
			Method to execute given attribute of Player object associated with given server id
			without raising exception.

		:param server_id: Takes sntring with server id
		:param action: Takes string with player method to execute
		:return: True no exception occuped, else - None
		"""
		player = self._get_player(server_id)
		if player:
			try:
				getattr(player, action)()
			except:
				return
			else:
				return True

	#########################################
	#
	#   Public member methods
	#
	#########################################

	def get_player(self, server):
		"""
			Public method to get player object assotiated with given server from list.

		:param server: Takes server object ot just server id string
		:return: Player object if exist. Else - None
		"""
		return self._get_player(valid_server(server))

	def start(self, server):
		"""
			Public method to start player associated with given server or server id
			without getting exception if something wrong.

		:param server: Takes server object ot just server id str
		:return: True if no exception occuped, else - None
		"""
		return self._action(valid_server(server), 'start')

	def stop(self, server):
		"""
			Public method to stop player associated with given server or server id
			without getting exception if something wrong.

		:param server: Takes server object ot just server id str
		:return: True if no exception occuped, else - None
		"""
		return self._action(valid_server(server), 'stop')

	def resume(self, server):
		"""
			Public method to resume player associated with given server or server id
			without getting exception if something wrong.

		:param server: Takes server object ot just server id str
		:return: True if no exception occuped, else - None
		"""
		return self._action(valid_server(server), 'resume')

	def pause(self, server):
		"""
			Public method to pause player associated with given server or server id
			without getting exception if something wrong.

		:param server: Takes server object ot just server id str
		:return: True if no exception occuped, else - None
		"""
		return self._action(valid_server(server), 'pause')

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
