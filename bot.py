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


# import atexit

# @atexit.register
# def goodbye():
# 	main.save_setting_to_files(main)

class main(discord.Client):


	############################################
	#
	#	__init__ Block
	#
################################################
	def __init__(self):
		super().__init__()
		self.__load_defaults()
		self.__load_opus()
		self.__load_token()
		self.__load_settings()
		self.__start_bot()
	############################################
	Defaults = {
		'SettingsFolder':'settings',
		'TokenFile':'my.token',
		'InviteLink': None,
		'OpusFile': 'libopus-0.x86.dll',
		'Prefix':'!',
		'Volume':'0.1',
		'AdminRole':'DJ',
		'ConfigFile': 'config.yml',
	}
	def __load_defaults(self):
		print('[INFO] Loading default settings')
		mode = 'r' if os.path.isfile(self.Defaults['ConfigFile']) else 'w+'
		with open('config.yml', mode) as file:
			self.cfg = yaml.load(file)
			#-------------------------------------------------------#
			self.SettingsFolder = self.cfg.get('SettingsFolder', self.Defaults['SettingsFolder']) + '/'
			self.TokenFile = self.cfg.get('TokenFile', self.Defaults['TokenFile'])
			self.InviteLink = self.cfg.get('InviteLink', self.Defaults['InviteLink'])
			self.OpusFile = self.cfg.get('OpusFile', self.Defaults['OpusFile'])
			#-------------------------------------------------------#
			self.Prefix = self.cfg.get('Prefix', self.Defaults['Prefix'])
			self.Volume = self.cfg.get('Volume', self.Defaults['Volume'])
			self.AdminRole = self.cfg.get('AdminRole', self.Defaults['AdminRole'])
		print('[INFO] Defaults succesfully loaded')
		print('------')
	############################################
	def __load_opus(self):
		print('[INFO] Trying to load OpusLib:')
		if not discord.opus.is_loaded():
			discord.opus.load_opus(self.OpusFile)
			if discord.opus.is_loaded():
				print ('[INFO] Opus loaded from file:' + self.OpusFile)
			else:
				print('[ERROR] An error occured while loading opus!')
				exit(1)
		else:
			print("[INFO] Opus already loaded!")
		print('------')
	############################################
	def __load_token(self):
		print('[INFO] Trying to load token')
		if os.path.isfile(self.TokenFile):
			with open(self.TokenFile, 'r') as file:
				self.Token = file.read()
			print('[INFO] Token succesfully loaded from token file')
		else: 
			print('[WARNING] Token file not found')
			self.Token = self.cfg.get('Token', None)
			if self.Token:
				print('[INFO] Token succesfully loaded from config')
			else:
				print("Please enter your bot token:")
				token = input()
				print("[INFO] Saving token...")
				with open(self.TokenFile, "w") as f:
					f.write(token)
				print("[INFO] Token succesfully saved")
		print('------')
	############################################
	def __load_settings(self):
		print('[INFO] Trying to load saved settings')
		if not os.path.isdir(self.SettingsFolder):
			os.makedirs(self.SettingsFolder)
			print('[WARNING] No saved settings directory found, so ill create it')
		else:
			print('[INFO] Loading settings from files')
			files = os.listdir(self.SettingsFolder)
			files = list(filter(lambda x: x.endswith('.yml'), files))
			if not files:
				print('[WARNING] No saved settings found in \'{}\' directory'.format(self.SettingsFolder))
			else:
				self._update_cfg_from_files(files)
				print('[INFO] Settings succesfully loaded')
		print('------')
	############################################
	def _update_cfg_from_files(self, files):
		for file in files:
			with open(self.SettingsFolder + file, 'r') as f:
				self.add_cfg_to_list(file[:-4], yaml.load(f))
	############################################
	def __start_bot(self, **kwargs):
		self.loop.run_until_complete(self.start(self.Token, **kwargs))
	############################################
	async def on_ready(self):
		print('[INFO] Logged in as:')
		print('\t' + self.user.name)
		print('\t' + self.user.id)
		await self.change_presence(game = discord.Game(name = "Blue Cat, Meow !!!"))
		servers = "\n- ".join([s.name + " (" + s.id + ")" for s in self.servers])
		prnt = "-----------------------------------\n    SYK Bot\n    discord.py version: {}\n    Running on servers:\n- {}\n-----------------------------------".format(discord.__version__, servers)
		print(prnt)
		print('Bot loaded succesfully at {}.'.format(datetime.now().strftime('%H:%M:%S')))
		print('-----------------------------------')
		
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
		################
		'disconnect': 'cmd_disconnect',
		'gtfo': 'cmd_disconnect',
		################
		'kys': 'cmd_shutdown',
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
		'rel': 'cmd_reload',
		'relaod': 'cmd_reload',
		################
		'set': 'cmd_set_settings',
		'settings': 'cmd_show_settings',
		'reset': 'cmd_reset_settings',
		################
		't': 'cmd_test',
		################
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
						await self.start_solo_song(msg, url)	
					else:
						await self.connect_voice_channel_by_author(msg)
						await self.start_solo_song(msg, url)	
				else:
					await self.Error(6, msg) # 'It`s not a single song!'
			else:
				await self.Error(5, msg) # 'Not valid link'
		else:
			await self.Error(12, msg) # 'Enter this f*&*ing song url here. Don\'t make me nervous, you mongol kid.'
	############################################
	async def cmd_stop(self, *args, **kwargs):
		msg = kwargs.get('msg')
		player = await self.get_server_player(msg.server.id)
		if player:
			player.stop()
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
				self.set_attributes(msg.server.id, Volume = v)
				player = await self.get_server_player(msg.server.id)
				if player:
					player.volume = v
		else:
			await self.Error(10, msg) # 'Invalid params, just like you'
	############################################
	async def cmd_now(self, *args, **kwargs):
		msg = kwargs.get('msg')
		player = await self.get_server_player(msg.server.id)
		if player:
			minutes = player.duration // 60
			seconds = player.duration % 60
			message = 'Now plaing:\n\t"{}"\t({}:{}).\nUploaded by:\n\t"{}"\nUrl:\n\t{}'
			message = message.format(player.title, minutes, seconds, player.uploader, player.url)
			await self.send_message(msg.channel, message)
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_pause(self, *args, **kwargs):
		msg = kwargs.get('msg')
		player = await self.get_server_player(msg.server.id)
		if player:
			if player.is_done():
				await self.Error(13, msg) # 'Your song already ended'
			elif not player.is_playing():
				await self.Error(15, msg) # 'The song is already paused, dont you hear this quality silence?'
			else:
				player.pause()
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_resume(self, *args, **kwargs):
		msg = kwargs.get('msg')
		player = await self.get_server_player(msg.server.id)
		if player:
			if player.is_done():
				await self.Error(13, msg) # 'Your song already ended'
			elif player.is_playing():
				await self.Error(14, msg) # 'The song is already playing, dont you hear?'
			else:
				player.resume()
		else:
			await self.Error(4, msg) # 'Nothing is being played'
	############################################
	async def cmd_invite(self, *args, **kwargs):
		msg = kwargs.get('msg')
		if self.InviteLink:
			await self.send_message(msg.channel, self.InviteLink)
		else:
			await Errors(20, msg) # 'No invite link was provided'
	############################################
	async def cmd_loop(self, *args, **kwargs):
		pass
	############################################
	# TODO: Make it userfriendly
	async def cmd_set_settings(self, *args, **kwargs):
		msg = kwargs.get('msg')
		cfg = {}
		for arg in args:
			cfg.update(self.get_dict(*arg.split(':')))
		self.set_attributes(msg.server.id,**cfg)
	############################################
	async def cmd_reset_settings(self, *args, **kwargs):
		msg = kwargs.get('msg')
		self.reset_settings(msg.server.id)
	############################################
	async def cmd_show_settings(self, *args, **kwargs):
		msg = kwargs.get('msg')
		cfg = self.get_cfg_from_list(msg.server_id)
		if not cfg:
			await self.Error(21, msg) # 'No setting saved for your server'
		else: 
			await self.send_message(msg.channal, cfg)
	############################################


	############################################
	async def cmd_test(self, *args, **kwargs):
		msg = kwargs.get('msg')
		print('--------')
		print('[TEST]')
		sid = msg.server.id
		# try:
		# 	player = await super().voice_client_in(msg.server).create_ytdl_player(args[0])
		# except Exception as e:
		# 	print('fdlkgjeifjahefihlfoewh;foawhef;kwahjf;klawhdflkahfdlk')
		# else:
		# 	player.start()
		# cfg = {'gg': 'ez'}
		# print(cfg)
		#print(self.Settings)
		# print(self.get_cfg_from_file(sid))
		#await self.send_message(msg.server.get_member('370641997238894602'), self.arts[0])
		# self.add_cfg_to_list(sid,cfg)
		# print(self.Settings)
		# self.set_attributes(sid, gg = 'wp', sht = 12)
		# print(self.Settings)
		# print(self.get_cfg_from_list(sid))
		# cf = self.get_cfg_from_list(sid)
		# print('Set-----')
		# self.set_attributes(sid, gg = 'wp', sht = 12)
		# print(self.get_cfg_from_list(sid))
		# print(cf)
		print('--------')
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
		# if not msg.content: 
		# 	pass
		# elif msg.author == self.user:
		# 	await self.chat_log(msg)
		if msg.content.startswith(self.Prefix) and not msg.author == self.user:
			#await self.chat_log(msg)
			mess_arr = msg.content[len(self.Prefix):].split()
			if mess_arr:
				cmd = mess_arr[0].lower()
				args = mess_arr[1:]
				if self.commands_arr.__contains__(cmd):
					command = self.commands_arr.get(cmd)
					await getattr(self, command)(*args, msg = msg)
				else:
					await self.Error(17, msg) # 'No such command'
			else:
				await self.Error(19,msg) # 'What are you hesitant.. Command me dont be a p&&sy, Meow!'

	############################################
################################################


	############################################
	#
	#	Utils Block
	#
################################################
	############################################
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
			'19': 'What are you hesitant.. Command me dont be a p&&sy, Meow!',
			'20': 'No invite link was provided',
			'21': 'No setting saved for your server',
			}
		message = Errors.get(str(error_id), 'Unknown error')
		await self.send_message(msg.channel, embed=discord.Embed(color=discord.Color.red(), description=(message)))
			#await self.send_message(msg.channel, message)
	############################################
	def is_youtube_list(self, url):
		#return True if str.startswith('https://www.youtube.com/playlist?list=') or str.startswith('www.youtube.com/playlist?list=') else False
		return True if 'list=' in url else False
	############################################
	def is_youtube_link(self, url):
		#return True if str.startswith('https://youtu.be/') or str.startswith('www.youtube.com/') or str.startswith('https://www.youtube.com/') else False
		return True if 'youtu.be' or 'youtube.com' in url else False
	############################################
	# TODO: Log system
	async def chat_log(self, msg):
		log = '[CHATLOG] ({}) [{}] <{}> {}: {}'
		log = log.format(msg.timestamp, msg.server.name, msg.channel.name, msg.author.display_name, msg.content)
		print(log)
	############################################
################################################

	############################################
	#
	#	Settings Block
	#
################################################
	Settings = {}
	############################################

	# main part

	############################################
	def get_attr(self, server_id, attr):
		cfg = self.get_cfg_from_list(server_id)
		return cfg.get(attr) if cfg else getattr(self, attr)
	############################################
	def set_attributes(self, server_id, **kwargs):
		cfg = self.get_cfg_from_list(server_id)
		if not cfg: 
			cfg = self.add_cfg_to_list(server_id, {})
		cfg.update(kwargs)
		self.save_cfg_to_file(server_id, cfg)
	############################################
	def reset_settings(self, server_id):
		self.remove_cfg_from_list(server_id)
		self.remove_settings_file(server_id)
	############################################


	############################################

	# list conrol

	############################################
	def add_cfg_to_list(self, server_id, cfg):
		self.Settings.update(self.get_dict(server_id,cfg))
		return self.Settings.get(server_id)
	############################################
	def remove_cfg_from_list(self, server_id):
		return True if self.Settings.pop(server_id, None) else False
	############################################
	def get_cfg_from_list(self, server_id):
		return self.Settings.get(server_id)
	############################################


	############################################

	# file control

	# ############################################
	# def save_setting_to_files(self):
	# 	for server_id, cfg in self.Settings.items():
	# 		self.save_cfg_to_file(server_id, cfg)
	# ############################################
	def save_cfg_to_file(self, server_id, cfg):
		file = self.SettingsFolder + '{}.yml'.format(server_id)
		with open(file, 'w') as f:
			yaml.dump(cfg, f, default_flow_style=False)
	############################################	
	def get_cfg_from_file(self, server_id):
		file = self.SettingsFolder + '{}.yml'.format(server_id)
		if os.path.isfile(file):
			with open(file, 'r') as f:
				cfg = yaml.load(f)
			return cfg
	############################################
	def remove_settings_file(self, server_id):
		self.silent_remove(self.SettingsFolder + '{}.yml'.format(server_id))
	############################################


	############################################

	# utils

	############################################
	def silent_remove(self, filename):
		try:
			os.remove(filename)
		except OSError:
			pass
	############################################
	def get_dict(self, key, value):
		try:
			result = float(value)
		except:
			result = value
		return dict([(key,result)])
	############################################	
################################################


	############################################
	#
	#	Play block
	#
################################################
	players = {}
	############################################
	async def get_server_player(self, server_id):
		return self.players.get(server_id)
	############################################
	async def start_new_player(self, msg, url):
		try:
			player = await super().voice_client_in(msg.server).create_ytdl_player(url)
		except Exception as e:
			print(e)
		else:
			return player
	############################################
	async def add_player_to_list(self, server_id, player):
		self.players[server_id] = player
	############################################
	async def remove_player(self, server_id):
		self.players.pop(server_id, None)
	############################################
	async def start_solo_song(self, msg, url):
		player = await self.start_new_player(msg, url)
		player.volume = self.get_attr(msg.server.id,'Volume')
		await self.add_player_to_list(msg.server.id, player)
		#await self.timer(msg)
		player.start()
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
	############################################
################################################


	############################################
	#
	#	Connect block
	#
################################################# 
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
	async def connect_voice_channel(self, msg, channel):
		if not self.is_voice_connected(msg.server):
			await super().join_voice_channel(channel)
			#print('[INFO] Joined channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
		else:
			voiceClient  = super().voice_client_in(msg.server)
			if not voiceClient.channel == channel:
				await voiceClient.move_to(channel)
				#print('[INFO] Moved to channel: \'{}\'. On server: \'{}\'.'.format(channel, channel.server))
			else:
				await self.Error(18, msg) # 'I\'m already with you, my blind kitten, MEOW!'
	############################################
	def find_voice_channel_by_name(self, server, channel_name):
		for channel in server.channels:
			if str(channel.type) == "voice" and channel.name.lower() == channel_name.lower():
				return channel
		#print('[ERROR] No such channel: \'{}\' on server: \'{}\''.format(channel_name, server))
		return None
	############################################
	async def leave_voice_by_server(self, msg):
		if self.is_voice_connected(msg.server):
			voiceClient = super().voice_client_in(msg.server)
			#print('[INFO] Disconnected from channel: \'{}\'. On server: \'{}\'.'.format(voiceClient.channel, msg.server))
			await voiceClient.disconnect()
			return True
		else:
			return False
	############################################
	arts = [
	"""
░░░░▄███▓███████▓▓▓░░░░
░░░███░░░▒▒▒██████▓▓░░░ 
░░██░░░░░░▒▒▒██████▓▓░░
░██▄▄▄▄░░░▄▄▄▄█████▓▓░░
░██░(◐)░░░▒(◐)▒██████
░██░░░░░░░▒▒▒▒▒█████▓▓░ 
░██░░░▀▄▄▀▒▒▒▒▒█████▓▓░
░█░███▄█▄█▄███░█▒████▓▓
░█░███▀█▀█▀█░█▀▀▒█████▓
░█░▀▄█▄█▄█▄▀▒▒▒▒█████▓░ 
░████░░░░░░▒▓▓███████▓░ 
░▓███▒▄▄▄▄▒▒▒▒████████░
░▓▓██▒▓███████████████░
	""",
	]
################################################


##########################################################	
#========================================================#
main()#			 Main Part of Your Bot	!!!				 #
#========================================================#
##########################################################