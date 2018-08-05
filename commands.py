import os
import sys

from utils import Say


def onlyonserver(func):
	async def wrap(self, *args, **kwargs):
		if not kwargs['Server']:
			Say.error(22)
		await func(self, *args, **kwargs)

	return wrap


class Command:
	def __init__(self, client):
		self.Client = client
		self.Settings = self.Client.Settings
		self.Player = self.Client.Player
		self.Connect = self.Client.Connect

	async def ex(self, *args, **kwargs):
		if args:
			command = self.commands_arr.get(args[0].lower())
			if not command:
				Say.error(17)  # 'No such command'
			command = '_cmd_' + command
			args = args[1:]
			await getattr(self, command)(*args, **kwargs)
		else:
			Say.error(19)  # 'What are you hesitant.. Command me dont be a p&&sy, Meow!'

	commands_arr = {
		'hello': 'hello',
		'invite': 'invite',
		################
		'connect': 'connect',
		'summon': 'connect',
		################
		'disconnect': 'disconnect',
		'gtfo': 'disconnect',
		################
		'kys': 'shutdown',
		'shutdown': 'shutdown',
		# ################
		# 'play': 'play',
		# ################
		# 'pause': 'pause',
		# 'resume': 'resume',
		# 'stop': 'stop',
		# 'volume': 'volume',
		# 'now': 'now',
		# ################
		# 'loop': 'loop',
		# ################
		'reload': 'reload',
		'rel': 'reload',
		# ################
		# 'set': 'set_settings',
		# 'settings': 'show_settings',
		# 'reset': 'reset_settings',
		# ################
		't': 'test',
		################
	}

	async def _cmd_hello(self, **kwargs):
		author = kwargs['Author']
		if author.id == '193741119140528129':
			Say.success('Hello {0.mention}, wanna some anime?'.format(author))
		else:
			Say.success('Hello {0.mention}, wanna some music?'.format(author))

	async def _cmd_invite(self):
		if self.Client.InviteLink:
			Say.success(self.Client.InviteLink)
		else:
			Say.error(20)  # 'No invite link was provided'

	@onlyonserver
	async def _cmd_connect(self, *args, **kwargs):
		channel_name = ' '.join(args)
		server = kwargs['Server']
		if channel_name:
			await self._connect_by_name(server, channel_name)
		else:
			await self._connect_by_author(server, kwargs['Author'])

	@onlyonserver
	async def _cmd_disconnect(self, **kwargs):
		if not await self.Connect.leave(kwargs['Server']):
			Say.error(2)  # 'I`m already homeless :('

	async def _cmd_shutdown(self, **kwargs):
		await self.Client.send_file(kwargs['Channel'], 'content\\shutdown.jpg')
		await self.Client.logout()

	# exit(0)

	async def _cmd_reload(self, **kwargs):
		os.system('cls')
		print('Don`t look there stranger! I`m fucking changi..ahem..reloading, meow!! ')
		print('------')
		await self.Client.send_file(kwargs['Channel'], 'content\\reload.png')
		await self.Client.logout()
		os.execl(sys.executable, 'python', 'bot.py', *sys.argv[1:])

	async def _cmd_test(self, *args, **kwargs):
		print('I got: ', args, ' and a bit of: ', kwargs)
		server = kwargs['Server']

	# async def _cmd_play(self):
	# 	if self.args:
	# 		url = self.args[0]
	# 		client = self.ctx['Client']
	# 		server = self.ctx['Server']
	# 		connect = self.ctx['Connect']
	# 		if is_youtube_link(url):
	# 			if Client.is_voice_connected(client, server):
	# 				await self.start_solo_song(msg, url)
	# 			else:
	# 				await self.connect_voice_channel_by_author(msg)
	# 				await self.start_solo_song(msg, url)
	# 		# else:
	# 		#	await self.Error(6, msg) # 'It`s not a single song!'
	# 		else:
	# 			await self.error(5, msg)  # 'Not valid link'
	# 	else:
	# 		await self.error(12, msg)  # 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.'
	#
	# ############################################
	# async def cmd_stop(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	player = await self.get_server_player(msg.server.id)
	# 	if player:
	# 		player.stop()
	# 	else:
	# 		await self.error(4, msg)  # 'Nothing is being played'
	#
	# ############################################

	# ############################################
	# # TODO: Check param method
	# async def cmd_volume(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	if args:
	# 		try:
	# 			v = float(args[0])
	# 		except:
	# 			await self.error(7, msg)  # 'Not valid volume value'
	# 		else:
	# 			if v > 2:
	# 				await self.error(11, msg)  # 'RIP ears'
	# 				v = 2
	# 			elif v < 0:
	# 				await self.error(16, msg)  # 'Is there life below 0?'
	# 				v = 0
	# 			self.set_attributes(msg.server.id, Volume=v)
	# 			player = await self.get_server_player(msg.server.id)
	# 			if player:
	# 				player.volume = v
	# 	else:
	# 		await self.error(10, msg)  # 'Invalid params, just like you'
	#
	# ############################################
	# async def cmd_now(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	player = await self.get_server_player(msg.server.id)
	# 	if player:
	# 		minutes = player.duration // 60
	# 		seconds = player.duration % 60
	# 		message = 'Now plaing:\n\t"{}"\t({}:{}).\nUploaded by:\n\t"{}"\nUrl:\n\t{}'
	# 		message = message.format(player.title, minutes, seconds, player.uploader, player.url)
	# 		await self.send_message(msg.channel, message)
	# 	else:
	# 		await self.error(4, msg)  # 'Nothing is being played'
	#
	# ############################################
	# async def cmd_pause(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	player = await self.get_server_player(msg.server.id)
	# 	if player:
	# 		if player.is_done():
	# 			await self.error(13, msg)  # 'Your song already ended'
	# 		elif not player.is_playing():
	# 			await self.error(15, msg)  # 'The song is already paused, dont you hear this quality silence?'
	# 		else:
	# 			player.pause()
	# 	else:
	# 		await self.error(4, msg)  # 'Nothing is being played'
	#
	# ############################################
	# async def cmd_resume(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	player = await self.get_server_player(msg.server.id)
	# 	if player:
	# 		if player.is_done():
	# 			await self.error(13, msg)  # 'Your song already ended'
	# 		elif player.is_playing():
	# 			await self.error(14, msg)  # 'The song is already playing, dont you hear?'
	# 		else:
	# 			player.resume()
	# 	else:
	# 		await self.error(4, msg)  # 'Nothing is being played'
	#
	# ############################################

	# ############################################
	# async def cmd_loop(self, *args, **kwargs):
	# 	pass
	#
	# ############################################
	# # TODO: Make it userfriendly
	# async def cmd_set_settings(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	cfg = {}
	# 	for arg in args:
	# 		cfg.update(self.get_dict(*arg.split(':')))
	# 	self.set_attributes(msg.server.id, **cfg)
	#
	# ############################################
	# async def cmd_reset_settings(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	self.reset_settings(msg.server.id)
	#
	# ############################################
	# async def cmd_show_settings(self, *args, **kwargs):
	# 	msg = kwargs.get('msg')
	# 	cfg = self.get_cfg_from_list(msg.server_id)
	# 	if not cfg:
	# 		await self.error(21, msg)  # 'No setting saved for your server'
	# 	else:
	# 		await self.send_message(msg.channal, cfg)
	#
	# ############################################
	async def _connect_by_author(self, server, author):
		if author.voice_channel:
			if not await self.Connect.connect(server, author.voice_channel):
				Say.error(18)  # 'I\'m already with you, my blind kitten, MEOW!'
			Say.success('I\'m here  ***Summoner***!')
		else:
			Say.error(1)  # 'You\'re not on the voice channel'

	async def _connect_by_name(self, server, channel_name):
		channel = self.Connect.find_voice_channel(server, channel_name)
		if channel:
			if not await self.Connect.connect(server, channel):
				Say.error(9)  # 'I\'m already here, dont you see me?'
			Say.success('It\'s been a long way, but I did it')
		else:
			Say.error(8)  # 'Create such a channel first'
