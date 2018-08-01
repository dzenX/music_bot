import os
import sys

from discord import Client

from connection import Connect
from utils import Say


class Command:
	def __init__(self, **kwargs):
		self.command = '_cmd_' + self.commands_arr.get(kwargs.pop('command'))
		if not self.command:
			Say.error(17)  # 'No such command'
		self.args = kwargs.get('args')
		self.ctx = kwargs.get('ctx')

	async def ex(self):
		await getattr(self, self.command)()

	""""
		Commands for bot
		To add command write:
		'Name_of_command' : 'Name_of_function_that_implements_it',
	"""
	# TODO: command help
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

	async def _cmd_hello(self):
		author = self.ctx.get('Author')
		if author.id == '193741119140528129':
			Say.success('Hello {0.mention}, wanna some anime?'.format(author))
		else:
			Say.success('Hello {0.mention}, wanna some music?'.format(author))

	async def _cmd_invite(self):
		if self.ctx.InviteLink:
			Say.success(self.ctx.InviteLink)
		else:
			Say.error(20)  # 'No invite link was provided'

	async def _cmd_connect(self):
		channel_name = ' '.join(self.args)
		connect = Connect(**self.ctx)
		if channel_name:
			await connect.connect_voice_channel_by_name(channel_name)
		else:
			await connect.connect_voice_channel_by_author()

	async def _cmd_disconnect(self):
		connect = Connect(**self.ctx)
		leaved = await connect.leave_voice()
		if not leaved:
			Say.error(2)  # 'I`m already homeless :('

	async def _cmd_shutdown(self):
		client = self.ctx['Client']
		await Client.send_file(client, self.ctx['Channel'], 'content\\shutdown.jpg')
		await Client.logout(client)
		exit(0)

	async def _cmd_reload(self):
		os.system('cls')
		print('Don`t look there stranger! I`m fucking changi..ahem..reloading, meow!! ')
		print('------')
		client = self.ctx['Client']
		print(client.Volume)
		await Client.send_file(client, self.ctx['Channel'], 'content\\reload.png')
		await Client.logout(client)
		os.execl(sys.executable, 'python', 'bot.py', *sys.argv[1:])


# async def cmd_play(self, *args, **kwargs):
# 	msg = kwargs.get('msg')
# 	if args:
# 		url = args[0]
# 		if self.is_youtube_link(url):
# 			# if not self.is_youtube_list(url):
# 			if self.is_voice_connected(msg.server):
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
