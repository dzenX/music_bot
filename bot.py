import discord
import yaml
import youtube_dl
import asyncio
import os
import sys
from datetime import datetime

#TODO: help RUTULIA
#self = discord.self()

ytdl_format_options = {
	'format': 'bestaudio/best',
	'extractaudio': True,
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
#	'ignoreerrors': True,
#	'logtostderr': False,
#	'quiet': True,
	'verbose': False,
#	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0',
}


class main(discord.Client):


	############################################
	#
	#	__init__ Block
	#
################################################
	def __init__(self):
		super().__init__()
		self.curr_song = None
		self.link = 'https://discordapp.com/oauth2/authorize?client_id=462304443954888724&scope=bot'
		self.__load_cfg()
		self._load_opus()
		self.__start_bot(self.token)
	############################################
	def __load_cfg(self):
		with open('config.yml', 'r') as file:
			self.cfg = yaml.load(file)
			self.Prefix = self.cfg['Prefix']
			self.Volume = self.cfg['Volume']
		with open('my.token', 'r') as file:
			self.token = file.read()
	############################################
	def _load_opus(self):
		print('Trying to load OpusLib:')
		if not discord.opus.is_loaded():
			discord.opus.load_opus(self.cfg['Opusfile'])
			if discord.opus.is_loaded():
				print ('Opus loaded from file:' + self.cfg['Opusfile'])
				print('------')
			else:
				print('An error occured while loading opus!')
				print('------')
				exit(1)
		else:
			print("Opus already loaded!")
			print('------')
	############################################
	def __start_bot(self,token,**kwargs):
		self.loop.run_until_complete(self.start(token, **kwargs))
	############################################
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		print('Bot loaded succesfully at {}.'.format(datetime.now().strftime('%H:%M:%S')))
		await self.change_presence(game = discord.Game(name = "Blue Cat, Meow !!!"))
		print('------')
################################################


	############################################
	#
	#	Commands block
	#
################################################
	commands_arr = {
		'hello' : 'cmd_hello',
		'invite': 'cmd_invite',
		################
		'connect': 'cmd_connect',
		'summon': 'cmd_connect',
		'disconnect': 'cmd_disconnect',
		'shutdown': 'cmd_shutdown',
		################
		'play': 'cmd_play',
		################
		'pause': 'cmd_pause',
		'resume': 'cmd_resume',
		'stop': 'cmd_stop',
		'volume': 'cmd_volume',
		'now': 'cmd_now',
		################
		'loop': 'cmd_loop',
		################
		'reload': 'cmd_reload',
		}
	############################################
	async def cmd_hello(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if msg.author.id == '193741119140528129':
			message = 'Hello {0.author.mention}, wanna some anime?'.format(msg)
		else:
			message = 'Hello {0.author.mention}, wanna some music?'.format(msg)
		await self.send_message(msg.channel, message)
	############################################
	async def cmd_connect(self, *args, **kwargs):
		msg = kwargs.get('msg')
		channel_name = ' '.join(args)
		if channel_name:
			await self.connect_voice_channel_by_name(msg, channel_name)
		else:
			await self.connect_voice_channel_by_author(msg)
	############################################
	async def cmd_disconnect(self, *args, **kwargs):
		msg = kwargs.get('msg')
		leaved = await self.leave_voice_by_server(msg)
		if not leaved:
			await self.Error(2, msg) # 'I`m already homeless :('
	############################################
	async def cmd_shutdown(self, *args, **kwargs):
		msg = kwargs.get('msg')
		await self.leave_voice_by_server(msg)
		await self.send_file(msg.channel, 'content\\shutdown.jpg')
		exit(0)
	############################################
	async def cmd_play(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if args:
			url = args[0]
			if self.is_youtube_link(url):
				if not self.is_youtube_list(url):
					if self.is_voice_connected(msg.server):
						await self.start_solo_song(msg)	
					else:
						await self.connect_voice_channel_by_author(msg)
						await self.start_solo_song(msg)	
				else:
					await self.Error(6, msg) # 'It`s not a single song!'
			else:
				await self.Error(5, msg) # 'Not valid link'
		else:
			await self.Error(12, msg) # 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.'
	############################################
	async def cmd_stop(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if self.curr_song:
			self.curr_song.stop()
			self.curr_song = None
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_reload(self, *args, **kwargs):
		msg = kwargs.get('msg')
		await self.leave_voice_by_server(msg)
		os.system('cls')
		print('Don`t look there stranger! I`m fucking changi..ahem..reloading, meow!! ')
		print('------')
		await self.send_file(msg.channel, 'content\\reload.png')
		os.execl(sys.executable, 'python', 'bot.py', *sys.argv[1:])
	############################################
	# TODO: Check param method
	async def cmd_volume(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if args:
			try:
				v = float(args[0])
			except Exception:
				await self.Error(7, msg) # 'Not valid volume value'
			else: 
				if v > 2:
					await self.Error(11, msg) # 'RIP ears'
					v = 2
				elif v < 0:
					await self.Error(16, msg) # 'Is there life below 0?'
					v = 0
				self.Volume = v
				if self.curr_song:
					self.curr_song.volume = v
		else:
			await self.Error(10, msg) # 'Invalid params, just like you'
	############################################
	async def cmd_now(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if self.curr_song:
			minutes = self.curr_song.duration // 60
			seconds = self.curr_song.duration % 60
			message = 'Now plaing:\n\t"{}"\t({}:{}).\nUploaded by:\n\t"{}"\nUrl:\n\t{}'
			message = message.format(self.curr_song.title, minutes, seconds, self.curr_song.uploader, self.curr_song.url)
			await self.send_message(msg.channel, message)
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_pause(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if self.curr_song:
			if self.curr_song.is_done():
				await self.Error(13, msg) # 'Your song already ended'
			elif not self.curr_song.is_playing():
				await self.Error(15, msg) # 'The song is already paused, dont you hear this quality silence?'
			else:
				self.curr_song.pause()
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_resume(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if self.curr_song:
			if self.curr_song.is_done():
				await self.Error(13, msg) # 'Your song already ended'
			elif self.curr_song.is_playing():
				await self.Error(14, msg) # 'The song is already playing, dont you hear?'
			else:
				self.curr_song.resume()
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_invite(self, *args, **kwargs):
		msg = kwargs.get('msg')
		await self.send_message(msg.channel, self.link)
	############################################
	async def cmd_loop(self, *args, **kwargs):
		msg = kwargs.get('msg')
	############################################
################################################


	############################################
	#
	#	On_Message block
	#
################################################
	############################################
	async def on_message(self, msg: discord.Message):
		await super().wait_until_ready()
		if not msg.content:
			return
		elif msg.author == self.user:
			await self.chat_log(msg)
			return
		elif msg.content.startswith(self.Prefix):
			await self.chat_log(msg)
			mess_arr = msg.content[len(self.Prefix):].split()
			cmd = mess_arr[0].lower()
			args = mess_arr[1:]
			if self.commands_arr.__contains__(cmd):
				command = self.commands_arr.get(cmd)
				await getattr(self, command)(*args, msg = msg)
			else:
				await self.Errors(17, msg) # 'No such command'
		else:
			return
	############################################
################################################


	############################################
	#
	#	Utils Block
	#
################################################
	# TODO: Same succes message system
	async def Error(self, error_id, msg):
		Errors = {
			'1': 'You\'re not on the voice channel',
			'2': 'I`m already homeless :(',
			'3': 'Unable to connect',
			'4': 'Nothing is being played',
			'5': 'Not valid link',
			'6': 'It`s not a single song!',
			'7': 'Not valid volume value',
			'8': 'Create such a channel first, motherfucker',
			'9': 'I\'m already here, dont you see me?',
			'10': 'Invalid params, just like you',
			'11': 'RIP ears\n{}'.format(datetime.now().strftime('%Y-%m-%d')),
			'12': 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.',
			'13': 'Your song already ended',
			'14': 'The song is already playing, dont you hear?',
			'15': 'The song is already paused, dont you hear this quality silence?',
			'16': 'Is there life below 0?',
			'17': 'No such command',
			'18': 'I\'m already with you, my blind kitten, MEOW!',
			}
		try:
			message = Errors[str(error_id)]
		except KeyError as e:
			print('Undefined Error Key: {}'.format(e.args[0]))
		else:
			print('Error: Code: {}. {}'.format(error_id,message))
			await self.send_message(msg.channel, embed=discord.Embed(color=discord.Color.red(), description=(message)))
			#await self.send_message(msg.channel, message)
	############################################
	def is_youtube_list(self,str):
		return True if str.startswith('https://www.youtube.com/playlist?list=') or str.startswith('www.youtube.com/playlist?list=') else False
	############################################
	def is_youtube_link(self,str):
		return True if str.startswith('https://youtu.be/') or str.startswith('www.youtube.com/') or str.startswith('https://www.youtube.com/') else False
	############################################
	# TODO: Log system
	async def chat_log(self, msg):
		log = '[CHATLOG] ({}) [{}] <{}> {}: {}'
		log = log.format(msg.timestamp, msg.server.name, msg.channel.name, msg.author.display_name, msg.content)
		print(log)
################################################


	############################################
	#
	#	Play block
	#
################################################
	async def start_solo_song(self,msg):
		if self.curr_song:
			self.curr_song.stop()
		self.curr_song = await super().voice_client_in(msg.server).create_ytdl_player(msg.content.split()[1])
		self.curr_song.volume = self.Volume
		#await self.timer(msg)
		self.curr_song.start()
	############################################
	async def timer(self, msg):
		message = 'Your song starts in: 10'
		curr_msg = await self.send_message(msg.channel, message)
		for i in range (1, 10):
			await asyncio.sleep(1)
			message = 'Your song starts in: {}'.format(10-i)
			await self.edit_message(curr_msg, message)
		await asyncio.sleep(1)
		message = 'BOOOOOOOM!!!!'
		await self.edit_message(curr_msg, message)
		await self.delete_message(curr_msg)
################################################


	############################################
	#
	#	Connect block
	#
################################################# 
	# TODO: Remove msg args, just server or channel
	############################################
	async def connect_voice_channel_by_author(self, msg):
		if msg.author.voice_channel:
			await self.connect_voice_channel(msg, msg.author.voice_channel)
		else:
			await self.Error(1, msg) # 'You\'re not on the voice channel'
	############################################
	async def connect_voice_channel_by_name(self, msg, channel_name):
		channel = self.find_voice_channel_by_name(msg.server, channel_name)
		if channel:
			await self.connect_voice_channel(msg, channel)
		else:
			await self.Error(8, msg) # 'Create such a channel first'
	############################################
	# TODO: Whats is faster to compare .channel or .channel.name :thinking:
	async def connect_voice_channel(self, msg, channel):
		if not self.is_voice_connected(msg.server):
			await super().join_voice_channel(channel)
			print('Joined channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
		else:
			voiceClient  = super().voice_client_in(msg.server)
			if not voiceClient.channel == channel:
				await voiceClient.move_to(channel)
				print('Moved to channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
			else:
				await self.Error(18, msg) # 'I\'m already with you, my blind kitten, MEOW!'
	############################################
	def find_voice_channel_by_name(self, server, channel_name):
		for channel in server.channels:
			if str(channel.type) == "voice" and channel.name.lower() == channel_name.lower():
				return channel
		print('No such channel: \'{}\' on server: \'{}\''.format(channel_name, server))
		return None
	############################################
	async def leave_voice_by_server(self, msg):
		if self.is_voice_connected(msg.server):
			voiceClient = super().voice_client_in(msg.server)
			print('Disconnected from channel: \'{}\'. On server: \'{}\'.'.format(voiceClient.channel, msg.server))
			await voiceClient.disconnect()
			return True
		else:
			return False

################################################


##########################################################	
#========================================================#
main()#			 Main Part of Your Bot	!!!				 #
#========================================================#
##########################################################