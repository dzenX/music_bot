from datetime import datetime

import discord
import yaml

#
#     LOOP BRANCH
#

# TODO: help RUTULIA
# self = discord.self()

ytdl_format_options = {
	'format': 'bestaudio/best',
	'extractaudio': True,
	# 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	# 'restrictfilenames': True,
	# 'noplaylist': True,
	# 'nocheckcertificate': True,
	# 'ignoreerrors': True,
	# 'logtostderr': False,
	# 'quiet': True,
	# 'verbose': False,
	# 'no_warnings': True,
	# 'default_search': 'auto',
	# 'source_address': '0.0.0.0',
}


class main(discord.Client):
	############################################
	def __load_cfg(self):
		with open("config.yml", "r") as file:
			self.cfg = yaml.load(file)
			self.Prefix = self.cfg['Prefix']
		with open('token.txt', 'r') as file:
			self.token = file.read()

	############################################
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		print('Bot loaded succesfully at {}.'.format(datetime.now().strftime('%H:%M:%S')))
		print('------')

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
			'17': 'I\'ll multiply your life on this number! Meow !!!',
		}
		await self.send_message(msg.channel, Errors[str(error_id)])

	def check_channel(self, msg, channel_name):
		for chn in msg.server.channels:
			if str(chn.type) == "voice" and chn.name.lower() == channel_name.lower():
				return chn
		return None

	async def __connect(self, msg, channel_name=None):
		if self.voiceClient is not None:
			if channel_name is not None and channel_name.lower() == self.voiceClient.channel.name.lower():
				await self.Error(9, msg)  # 'I\'m already here, dont you see me?'
				return
			elif channel_name is None and msg.server.get_member(
					msg.author.id).voice_channel.name.lower() == self.voiceClient.channel.name.lower():
				await self.Error(9, msg)  # 'I\'m already here, dont you see me?'
				return
			else:
				await self.voiceClient.disconnect()
		if channel_name is not None:
			chn = self.check_channel(msg, channel_name)
			if chn is not None:
				try:
					self.voiceClient = await super().join_voice_channel(chn)
				except Exception as e:
					print(e)
					await self.Error(1, msg)  # 'You're not on the voice channel'
			else:
				await self.Error(8, msg)  # 'Create such a channel first'
		else:
			try:
				self.voiceClient = await super().join_voice_channel(msg.author.voice_channel)
			except Exception as e:
				print(e)
				await self.Error(1, msg)  # 'You're not on the voice channel'

	async def start_solo_song(self, msg):
		player = await  self.create_player(msg.content.split()[1], self.voice_client_in(msg.server))
		print('gg')
		player.start()

	async def create_player(self, url, voice, **kwargs):
		import youtube_dl

		ydl = youtube_dl.YoutubeDL(ytdl_format_options)
		import functools
		func = functools.partial(ydl.extract_info, url, download=False)
		info = await voice.loop.run_in_executor(None, func)
		# print(info)
		# for st in info['entries']:
		# 	print(st)
		# print('-----------------------------------------------------------------------------')
		# for key,value in info.items():
		# 	print(key,'  =====  ', value)
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		# print('-----------------------------------------------------------------------------')
		for key, value in info['entries'][0].items():
			print(key, '  =====  ', value)

		if "entries" in info:
			info = info['entries'][0]
		print(info)
		download_url = info['url']
		player = voice.create_ffmpeg_player(download_url, **kwargs)

		# set the dynamic attributes from the info extraction
		player.download_url = download_url
		player.url = url
		player.yt = ydl
		player.views = info.get('view_count')
		player.is_live = bool(info.get('is_live'))
		player.likes = info.get('like_count')
		player.dislikes = info.get('dislike_count')
		player.duration = info.get('duration')
		player.uploader = info.get('uploader')
		player.title = info.get('title')
		player.description = info.get('description')

		return player

	async def on_message(self, msg: discord.Message):
		await super().wait_until_ready()
		if msg.content.startswith(self.Prefix + 'hello'):
			if msg.author.id == '193741119140528129':
				message = 'Hello {0.author.mention}, wanna some anime?'.format(msg)
			else:
				message = 'Hello {0.author.mention}, wanna some music?'.format(msg)
			await self.send_message(msg.channel, message)
		elif msg.content.startswith(self.Prefix + 'play'):
			if len(msg.content.split()) >= 2:
				if self.is_voice_connected(msg.server):
					await self.start_solo_song(msg)
				else:
					try:
						self.voiceClient = await super().join_voice_channel(msg.author.voice_channel)
					except:
						await self.Error(1, msg)  # 'You are not in voice channel'
					else:
						await self.start_solo_song(msg)
			else:
				await self.Error(12, msg)  # 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.'

	def _load_opus(self):
		print('Trying to load OpusLib:')
		if not discord.opus.is_loaded():
			discord.opus.load_opus(self.cfg['Opusfile'])
			if discord.opus.is_loaded():
				print('Opus loaded from file:' + self.cfg['Opusfile'])
				print('------')
			else:
				print('An error occured while loading opus!')
				print('------')
				exit(1)
		else:
			print("Opus already loaded!")
			print('------')

	def __start_bot(self, token, **kwargs):
		self.loop.run_until_complete(self.start(token, **kwargs))

	def __init__(self):
		super().__init__()
		self.voiceClient = None
		self.curr_song = None
		self.__load_cfg()
		self._load_opus()
		self.__start_bot(self.token)


main()
