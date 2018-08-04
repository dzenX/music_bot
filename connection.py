from discord import Channel, Client

from utils import Say


class Connect:
	def __init__(self, **kwargs):
		self.client = kwargs.get('Client')
		self.server = kwargs.get('Server')
		self.author = kwargs.get('Author')

	# print('[INFO] Joined channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
	# print('[ERROR] No such channel: \'{}\' on server: \'{}\''.format(channel_name, server))
	# print('[INFO] Moved to channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
	# print('[INFO] Disconnected from channel: \'{}\'. On server: \'{}\'.'.format(voiceClient.channel, msg.server))
	# TODO I dont really like talking methods.. Should we better do smth like return err_code here mhmm..
	async def connect_voice_channel_by_author(self):
		if self.author.voice_channel:
			if not await self.__connect_voice_channel(self.author.voice_channel):
				Say.error(18)  # 'I\'m already with you, my blind kitten, MEOW!'
			Say.success('I\'m here  ***Summoner***!')
		else:
			Say.error(1)  # 'You\'re not on the voice channel'

	async def connect_voice_channel_by_name(self, channel_name):
		channel = self.find_voice_channel(self.server, channel_name)
		if channel:
			if not await self.__connect_voice_channel(channel):
				Say.error(9)  # 'I\'m already here, dont you see me?'
			Say.success('It\'s been a long way, but I did it')
		else:
			Say.error(8)  # 'Create such a channel first'

	async def __connect_voice_channel(self, channel):
		if not self.client.is_voice_connected(self.server):
			await Client.join_voice_channel(self.client, channel)
		else:
			voiceClient = Client.voice_client_in(self.client, self.server)
			if voiceClient.channel == channel:
				return
			await voiceClient.move_to(channel)
		return True

	async def leave_voice(self):
		if self.client.is_voice_connected(self.server):
			voiceClient = Client.voice_client_in(self.client, self.server)
			await voiceClient.disconnect()
			return True

	@staticmethod
	def find_voice_channel(server, channel_name):
		if isinstance(channel_name, Channel):
			channel_name = channel_name.name
		for channel in server.channels:
			if str(channel.type) == "voice" and channel.name.lower() == channel_name.lower():
				return channel
