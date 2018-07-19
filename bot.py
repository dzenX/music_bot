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
	'ignoreerrors': True,
	'logtostderr': False,
	'quiet': True,
	'verbose': False,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0',
}

class codek(discord.Client):
	############################################
	def __load_cfg(self):
		self.Reconnect = False
		with open("config.yml", "r") as file:
			self.cfg = yaml.load(file)
			self.Reconnect = self.cfg['AutoReconnect']
			self.Prefix = self.cfg['Prefix']
			self.Volume = self.cfg['Volume']
	############################################
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		print('Bot loaded succesfully at {}.'.format(datetime.now().strftime('%H:%M:%S')))
		print('------')
	############################################
	# TODO: Do we need this exception ? :thinking:
	async def Error(self,error_id,msg):
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
			}
		try:
			message = Errors[str(error_id)]
		except KeyError as e:
			print('Undefined Error Key: {}'.format(e.args[0]))
		# This
		except Exception as e:
			print('Unknown error with self.error')
			print(e)
		else:
			print('Error: Code: {}. {}.'.format(error_id,message))
			await self.send_message(msg.channel, message)
	############################################	
	async def start_solo_song(self,msg):
		if self.curr_song is not None:
			self.curr_song.stop()
		self.curr_song = await self.voiceClient.create_ytdl_player(msg.content.split()[1], ytdl_options = ytdl_format_options)
		self.curr_song.volume = self.Volume
		message = 'Your song starts in: 10'
		curr_msg = await self.send_message(msg.channel, message)
		for i in range (1,10):
			await asyncio.sleep(1)
			message = 'Your song starts in: {}'.format(10-i)
			await self.edit_message(curr_msg, message)
		await asyncio.sleep(1)
		message = 'BOOOOOOOM!!!!'
		await self.edit_message(curr_msg, message)
		await self.delete_message(curr_msg)
		self.curr_song.start()
	############################################
	def is_youtube_list(self,str):
		return True if str.startswith('https://www.youtube.com/playlist?list=') or str.startswith('www.youtube.com/playlist?list=') else False
	############################################
	def is_youtube_link(self,str):
		return True if str.startswith('https://youtu.be/') or str.startswith('www.youtube.com/') or str.startswith('https://www.youtube.com/') else False
	############################################
	def check_channel(self, msg, channel_name):
		for chn in msg.server.channels:
			if str(chn.type) == "voice" and chn.name.lower() == channel_name.lower():
				return chn
		return None
	############################################
	async def __connect(self, msg, channel_name = None):
		if self.voiceClient is not None:
			if channel_name is not None and channel_name.lower() == self.voiceClient.channel.name.lower():
				await self.Error(9, msg)  # 'I\'m already here, dont you see me?'
				return
			elif channel_name is None and msg.server.get_member(msg.author.id).voice_channel.name.lower() == self.voiceClient.channel.name.lower():
				await self.Error(9, msg)  # 'I\'m already here, dont you see me?'
				return
			else:
				await self.voiceClient.disconnect()
		if channel_name is not None:
			chn = self.check_channel(msg,channel_name)
			if chn is not None:
				try:
					self.voiceClient = await super().join_voice_channel(chn)
				except Exception as e:
					print(e)
					await self.Error(1,msg) # 'You're not on the voice channel'
			else:
				await self.Error(8,msg) # 'Create such a channel first'
		else:
			mbm = msg.server.get_member(msg.author.id)
			try:
				self.voiceClient = await super().join_voice_channel(mbm.voice_channel)
			except Exception as e:
				print(e)
				await self.Error(1,msg) # 'You're not on the voice channel'
	############################################
	async def on_message(self, msg: discord.Message):
		await super().wait_until_ready()
		#================================================================================================#
		if msg.author == self.user or msg.content == "":
			return
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'hello'):
			if msg.author.id == '193741119140528129':
				message = 'Hello {0.author.mention}, wanna some anime?'.format(msg)
			else:
				message = 'Hello {0.author.mention}, wanna some music?'.format(msg)
			await self.send_message(msg.channel, message)
		#================================================================================================#	
		elif msg.content.startswith(self.Prefix + 'connect'):
			msg_arr = msg.content.split()
			if len(msg_arr) > 1:
				str = ' '.join(msg_arr[1:])
				await self.__connect(msg, str)
			else:
				await self.__connect(msg)
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'disconnect'):
			if self.voiceClient is not None:
				await self.voiceClient.disconnect()
				self.voiceClient = None
			else:
				await self.Error(2,msg) # 'I`m already homeless :('
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'shutdown'):
			if self.voiceClient is not None:
				await self.voiceClient.disconnect()
			exit(0)
		#================================================================================================#	
		elif msg.content.startswith(self.Prefix + 'play'):
			if len(msg.content.split()) >= 2:
				url = msg.content.split()[1]
				if self.is_youtube_link(url):
					if not self.is_youtube_list(url):
						if self.is_voice_connected(msg.server):
							await self.start_solo_song(msg)	
						else:
							mbm = msg.server.get_member(msg.author.id)
							try:
								channel = mbm.voice_channel
								self.voiceClient = await super().join_voice_channel(channel)
							except Exception as e:
								print(e)
								await self.Error(1,msg) # 'You are not in voice channel'
							else:
								await self.start_solo_song(msg)	
					else:
						await self.Error(6,msg) # 'It`s not a single song!'
				else:
					await self.Error(5,msg) # 'Not valid link'
			else:
				await self.Error(12,msg) # 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.'
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'stop'):
			if self.curr_song is not None:
				self.curr_song.stop()
				self.curr_song = None
			else:
				await self.Error(4,msg) # 'Nothing is being played'
		#================================================================================================#
		# TODO: Make music for reload
		# TODO: Do we need 'cls' on reload or just some '\n'?
		elif msg.content.startswith(self.Prefix + 'reload'):
			if self.voiceClient is not None:
				await self.voiceClient.disconnect()
				self.voiceClient = None
			os.system('cls')
			# print('\n\n\n\n\n')
			print('Don`t look there stranger! I`m fucking changi..ahem..reloading, meow!! ')
			print('------')
			os.execl(sys.executable, 'python', 'bot.py', *sys.argv[1:])
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'cl'):
			os.system('cls')
		#================================================================================================#
		# TODO: Fix volume. So max value is 2.0
		elif msg.content.startswith(self.Prefix + 'volume'):
			if len(msg.content.split()) == 2:
				try:
					v = float(msg.content.split()[1])
				except Exception as e:
					await self.Error(7,msg)
				else:
					if v > 2:
						await self.Error(11,msg) # 'RIP ears'
						v = 2
					elif v < 0:
						await self.Error(16,msg) # 'Is there life below 0?'
						v = 0
					self.Volume = v
					if self.curr_song is not None:
						self.curr_song.volume = v
			else:
				await self.Error(10,msg)  # 'Invalid params, just like you'
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'now'):
			if self.curr_song is not  None:
				minutes = self.curr_song.duration // 60
				seconds = self.curr_song.duration % 60
				message = 'Now plaing:\n\t"{}"\t({}:{}).\nUploaded by:\n\t"{}"\nUrl:\n\t{}'.format(self.curr_song.title, minutes, seconds, self.curr_song.uploader, self.curr_song.url)
				await self.send_message(msg.channel, message)
			else:
				await self.Error(4,msg) # 'Nothing is being played'
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'pause'):
			if self.curr_song is not None:
				if self.curr_song.is_done():
					await self.Error(13,msg) # 'Your song already ended'
				elif not self.curr_song.is_playing():
					await self.Error(15,msg) # 'The song is already paused, dont you hear this quality silence?'
				else:
					self.curr_song.pause()
			else:
				await self.Error(4,msg) # 'Nothing is being played'
		#================================================================================================#
		elif msg.content.startswith(self.Prefix + 'resume'):
			if self.curr_song is not None:
				if self.curr_song.is_done():
					await self.Error(13,msg) # 'Your song already ended'
				elif self.curr_song.is_playing():
					await self.Error(14,msg) # 'The song is already playing, dont you hear?'
				else:
					self.curr_song.resume()
			else:
				await self.Error(4,msg) # 'Nothing is being played'

		#================================================================================================#
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
	def __init__(self):
		super().__init__()
		self.voiceClient = None
		self.curr_song = None
		self.__load_cfg()
		self._load_opus()
		self.__start_bot(self.cfg['Token'])
	
codek()

