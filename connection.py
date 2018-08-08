# TODO: Maybe just 3 functions should be there ? hmm..
class Connect:
	def __init__(self, client):
		self.Client = client

	# print('[INFO] Joined channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
	# print('[ERROR] No such channel: \'{}\' on server: \'{}\''.format(channel_name, server))
	# print('[INFO] Moved to channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
	# print('[INFO] Disconnected from channel: \'{}\'. On server: \'{}\'.'.format(voiceClient.channel, msg.server))
	# TODO I dont really like talking methods.. Should we better do smth like return err_code here mhmm..

	async def leave(self, server):
		"""
			Public method to leave voice channel on given server.

		:param server: Takes server object
		:return: True if leaved, None if already not connected
		"""

		return await self.Client.voice_client_in(server).disconnect()

	@staticmethod
	def find_voice_channel(server, channel_name):
		"""
			Static method to find if voice channel with given name exits in given server.

		:param server: Takes server object
		:param channel_name: Takes string with name of channel to search
		:return: Voice channel object if exist
		"""
		for channel in server.channels:
			if str(channel.type) == "voice" and channel.name.lower() == channel_name.lower():
				return channel

	async def connect(self, server, channel):
		"""
			Method to connect to given voice channel on given server

		:param server: Takes server object
		:param channel: Takes voice channel object
		:return: True if connected or moved to another, else - None
		"""
		# TODO Do we need this check if in commands we throw exception if smth wrong
		if not self.Client.is_voice_connected(server):
			await self.Client.join_voice_channel(channel)
		else:
			voiceClient = self.Client.voice_client_in(server)
			if voiceClient.channel == channel:
				return
			await voiceClient.move_to(channel)
		return True
