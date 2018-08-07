import os
import sys

import discord

from utils import Raise, is_youtube_link


def onlyonserver(func):
	async def onlyonserver_wrap(self, *args, **kwargs):
		if not kwargs['Server']:
			Raise.error(22)
		await func(self, *args, **kwargs)

	return onlyonserver_wrap


def noargs(func):
	async def noargs_wrap(self, *args, **kwargs):
		if args:
			message = 'What is it? "{}"\nWhat are you taking me for? But anyway i will do my shit work..\n'
			await self.say(kwargs['Channel'], message.format(', '.join(arg for arg in args)))
		await func(self, **kwargs)

	return noargs_wrap

class Command:
	def __init__(self, client):
		self.Client = client
		self.Settings = self.Client.Settings
		self.Player = self.Client.Player
		self.Connect = self.Client.Connect

	async def ex(self, msg_arr, ctx):
		if msg_arr:
			command = self.commands_arr.get(msg_arr[0].lower())
			if not command:
				Raise.error(17)  # 'No such command'
			command = '_cmd_' + command
			args = msg_arr[1:]
			await getattr(self, command)(*args, **ctx)
		else:
			Raise.error(19)  # 'What are you hesitant.. Command me dont be a p&&sy, Meow!'

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
		'play': 'play',
		# ################
		'pause': 'pause',
		'resume': 'resume',
		'stop': 'stop',
		'volume': 'volume',
		'now': 'now',
		# ################
		# 'loop': 'loop',
		# ################
		'reload': 'reload',
		'rel': 'reload',
		'relaod': 'reload',
		# ################
		'settings': 'show_settings',
		'reset': 'reset_settings',
		# ################
		't': 'test',
		'help': 'help'
		################
	}

	commands_descr = {
		'hello': 'Say hello to bot',
		'invite': 'Invite link for bot',
		################
		'connect': 'Connect bot to voice channel you are in, or to mentioned voice channel',
		'summon': 'Same as connect, but created for cute guys',
		################
		'disconnect': 'Disconnects from current voice channel',
		'gtfo': 'Same as connect, but created for REAL GANSTA\'S',
		################
		'kys': 'Turns off the bot with WITH REAL HATE',
		'shutdown': 'Turns off the bot',
		################
		'play': 'Plays song',
		################
		'pause': 'Pausing current playing song',
		'resume': 'Resumes current stopped song',
		'stop': 'Stops playing song',
		'volume': 'Regulate volume',
		'now': 'Shows current song',
		################
		'loop': 'Loops song',
		################
		'reload': 'Reloads bot',
		'rel': 'Reloads bot for lazy people',
		'relaod': 'Reloads bot for some iq braindead people',
		################
		'set': 'Sets bot settings',
		'settings': 'Shows bot settings',
		'reset': 'Resets bot settigs',
		################
		# 't': 'cmd_test',
		################
		'help': 'Shows this to you',
	}


	async def say(self, channel, message=None, **kwargs):
		embed = kwargs.get('embed')
		if not message:
			if not embed:
				return
			else:
				await self.Client.send_message(channel, embed=embed)
		else:
			if kwargs.get('file'):
				await self.Client.send_file(channel, message)
			else:
				if not embed:
					await self.Client.send_message(channel, message)
				else:
					color = kwargs.get('color')
					if color:
						color = getattr(discord.Color, color)()
					else:
						color = discord.Color.green()
					embed = discord.Embed(color=color, description=message)
					await self.Client.send_message(channel, embed=embed)

	@noargs
	async def _cmd_hello(self, **kwargs):
		author = kwargs['Author']
		if author.id == '193741119140528129':
			message = 'Hello {0.mention}, wanna some anime?'
		else:
			message = 'Hello {0.mention}, wanna some music?'

		await self.say(kwargs['Channel'], message.format(author))

	@noargs
	async def _cmd_help(self, **kwargs):
		channel = kwargs['Channel']
		await self.say(channel, 'I\'m powerful enough to do this:\n')
		message = '\n'.join('***' + self.Client.Prefix + key + ' ***: ' + self.commands_descr.get(key, "Can't help")
		                    for key in self.commands_arr)
		await self.say(channel, message)
		await self.say(channel, 'Choose your way stranger, and may the force be with you!')

	@noargs
	async def _cmd_invite(self, **kwargs):
		if self.Client.InviteLink:
			await self.say(kwargs['Channel'], self.Client.InviteLink)
		else:
			Raise.error(20)  # 'No invite link was provided'

	@onlyonserver
	async def _cmd_connect(self, *args, **kwargs):
		channel_name = ' '.join(args)
		if channel_name:
			if not await self._connect_by_name(channel_name, **kwargs):
				Raise.error(9)  # 'I\'m already here, dont you see me?'
			await self.say(kwargs['Channel'], 'It\'s been a long way, but I did it')
		else:
			if not await self._connect_by_author(**kwargs):
				Raise.error(18)  # 'I\'m already with you, my blind kitten, MEOW!'
			await self.say(kwargs['Channel'], 'I\'m here  ***Summoner***!')

	@onlyonserver
	@noargs
	async def _cmd_disconnect(self, **kwargs):
		if not await self.Connect.leave(kwargs['Server']):
			Raise.error(2)  # 'I`m already homeless :('

	async def _connect_by_author(self, **kwargs):
		author = kwargs['Author']
		if not author.voice_channel:
			Raise.error(1)  # 'You\'re not on the voice channel'
		return await self.Connect.connect(kwargs['Server'], author.voice_channel)

	async def _connect_by_name(self, channel_name, **kwargs):
		server = kwargs['Server']
		channel = self.Connect.find_voice_channel(server, channel_name)
		if not channel:
			Raise.error(8)  # 'Create such a channel first'
		return not await self.Connect.connect(server, channel)

	@noargs
	async def _cmd_shutdown(self, **kwargs):
		await self.Client.send_file(kwargs['Channel'], 'content\\shutdown.jpg')
		await self.Client.logout()

	@noargs
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
		self.g = server

	@onlyonserver
	async def _cmd_play(self, *args, **kwargs):
		if args:
			url = args[0]
			if is_youtube_link(url):
				if not self.Client.is_voice_connected(kwargs['Server']):
					await self._connect_by_author(**kwargs)
				await self._start_solo_song(url, **kwargs)
			else:
				Raise.error(5)  # 'Not valid link'
		else:
			Raise.error(12)  # 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.'

	async def _start_solo_song(self, url, **kwargs):
		player = self.Player.create_youtube_player(kwargs['Server'], url)
		await self.Player.timer(kwargs['Channel'], 10)
		player.start()

	@onlyonserver
	@noargs
	async def _cmd_stop(self, **kwargs):
		player = self.Player.get_player(kwargs['Server'])
		if player:
			player.stop()
		else:
			Raise.error(4)  # 'Nothing is being played'

	@onlyonserver
	async def _cmd_volume(self, *args, **kwargs):
		if args:
			try:
				v = float(args[0])
			except:
				Raise.error(7)  # 'Not valid volume value'
			else:
				if v > 2:
					Raise.error(11)  # 'RIP ears'
					v = 2
				elif v < 0:
					Raise.error(16)  # 'Is there life below 0?'
					v = 0
				server = kwargs['Server']
				player = self.Player.get_player(server)
				self.Settings.set_attr(server, 'Volume', v)
				if player:
					player.volume = v
		else:
			Raise.error(10)  # 'Invalid params, just like you'

	@onlyonserver
	@noargs
	async def _cmd_now(self, **kwargs):
		player = self.Player.get_player(kwargs['Server'])
		if player:
			minutes = player.duration // 60
			seconds = player.duration % 60
			message = 'Now plaing:\n\t"{}"\t({}:{}).\nUploaded by:\n\t"{}"\nUrl:\n\t{}'
			message.format(player.title, minutes, seconds, player.uploader, player.url)
			await self.say(kwargs['Channel'], message)
		else:
			Raise.error(4)  # 'Nothing is being played'

	@onlyonserver
	@noargs
	async def _cmd_pause(self, **kwargs):
		player = self.Player.get_player(kwargs['Server'])
		if player:
			if player.is_done():
				Raise.error(13)  # 'Your song already ended'
			elif not player.is_playing():
				Raise.error(15)  # 'The song is already paused, dont you hear this quality silence?'
			else:
				player.pause()
		else:
			Raise.error(4)  # 'Nothing is being played'

	@onlyonserver
	@noargs
	async def _cmd_resume(self, **kwargs):
		player = self.Player.get_player(kwargs['Server'])
		if player:
			if player.is_done():
				Raise.error(13)  # 'Your song already ended'
			elif player.is_playing():
				Raise.error(14)  # 'The song is already playing, dont you hear?'
			else:
				player.resume()
		else:
			Raise.error(4)  # 'Nothing is being played'

	# @onlyonserver
	# async def cmd_loop(self, *args, **kwargs):
	# 	pass
	@onlyonserver
	@noargs
	async def _cmd_reset_settings(self, **kwargs):
		self.Settings.reset_cfg(kwargs['Server'])

	@onlyonserver
	@noargs
	async def _cmd_show_settings(self, **kwargs):
		server = kwargs['Server']
		cfg = self.Settings.get_cfg(server)
		if not cfg:
			Raise.error(21)  # 'No setting saved for your server'
		message = 'Setting saved for server {}\n'.format(server)
		message += '\n'.join(key + ' : ' + str(value) for key, value in cfg.items())
		await self.say(kwargs['Channel'], message)
