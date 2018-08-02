# import youtube_dl it was unused btw
import asyncio
import os
from datetime import datetime

import discord
import yaml

# TODO: help RUTULIA
# self = discord.self()
from commands import Command
from settings import Settings
from utils import Error, Success

""""
	Settings for creating youtube stream
"""
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

class Main(discord.Client):
	""""
		Class represents discord bot work and functions
	"""
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
		self.Settings = Settings(self.SettingsFolder)
		self.__start_bot()

	############################################
	""""
		Default settings for bot in case
		there is no config file
	"""
	Defaults = {
		'SettingsFolder': 'settings',
		'TokenFile': 'my.token',
		'InviteLink': None,
		'OpusFile': 'libopus-0.x86.dll',
		'Prefix': '!',
		'Volume': '0.1',
		'AdminRole': 'DJ',
		'ConfigFile': 'config.yml',
	}

	############################################
	def __load_defaults(self):
		print('[INFO] Loading default settings')
		mode = 'r' if os.path.isfile(self.Defaults['ConfigFile']) else 'w+'
		with open('config.yml', mode) as file:
			self.cfg = yaml.load(file)
			# -------------------------------------------------------#
			self.SettingsFolder = self.cfg.get('SettingsFolder', self.Defaults['SettingsFolder']) + '/'
			self.TokenFile = self.cfg.get('TokenFile', self.Defaults['TokenFile'])
			self.InviteLink = self.cfg.get('InviteLink', self.Defaults['InviteLink'])
			self.OpusFile = self.cfg.get('OpusFile', self.Defaults['OpusFile'])
			# -------------------------------------------------------#
			self.Prefix = self.cfg.get('Prefix', self.Defaults['Prefix'])
			self.Volume = self.cfg.get('Volume', self.Defaults['Volume'])
			self.AdminRole = self.cfg.get('AdminRole', self.Defaults['AdminRole'])
		print('[INFO] Defaults succesfully loaded')
		print('------')

	############################################
	def __load_opus(self):
		""""
			Loading codec
		"""
		print('[INFO] Trying to load OpusLib:')
		if not discord.opus.is_loaded():
			discord.opus.load_opus(self.OpusFile)
			if discord.opus.is_loaded():
				print('[INFO] Opus loaded from file:' + self.OpusFile)
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
	def __start_bot(self, **kwargs):
		self.loop.run_until_complete(self.start(self.Token, **kwargs))

	############################################
	async def on_ready(self):
		print('[INFO] Logged in as:')
		print('\t' + self.user.name)
		print('\t' + self.user.id)
		await self.change_presence(game=discord.Game(name="Blue Cat, Meow !!!"))
		servers = "\n- ".join([s.name + " (" + s.id + ")" for s in self.servers])
		prnt = "-----------------------------------\n	SYK Bot\n	discord.py version: {}\n	"
		prnt = prnt + "Running on servers:\n- {}\n-----------------------------------"
		print(prnt.format(discord.__version__, servers))
		print('Bot loaded successfully at {}.'.format(datetime.now().strftime('%H:%M:%S')))
		print('-----------------------------------')

	################################################
	#
	#	On_Message block
	#
	################################################
	async def on_message(self, msg: discord.Message):
		await super().wait_until_ready()
		# TODO: Fix exception when commands called from private chat (check if msg.server is not None)
		if msg.content.startswith(self.Prefix) and not msg.author == self.user:
			await self._command(msg)

	async def _command(self, msg):
		msg_arr = msg.content[len(self.Prefix):].split()
		ctx = dict(Author=msg.author, Server=msg.server, Channel=msg.channel, Client=self)
		try:
			await Command(msg_arr, ctx).ex()
		except Error as e:
			if e.isfile:
				await self.send_file(msg.channel, str(e))
			elif e.embed:
				embed = discord.Embed(color=discord.Color.red(), description=str(e))
				await self.send_message(msg.channel, embed=embed)
			else:
				await self.send_message(msg.channel, str(e))
		except Success as e:
			if e.isfile:
				await self.send_file(msg.channel, str(e))
			elif e.embed:
				embed = discord.Embed(color=discord.Color.green(), description=str(e))
				await self.send_message(msg.channel, embed=embed)
			else:
				await self.send_message(msg.channel, str(e))
		else:  # TODO: what should he do if command dont need to print anything
			await self.send_message(msg.channel, 'Idk whats happening here')

	################################################
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
		await asyncio.sleep(20)
		# player.volume = self.get_attr(msg.server.id,'Volume')
		await self.add_player_to_list(msg.server.id, player)
		# await self.timer(msg)
		player.start()

	############################################
	async def timer(self, msg):
		message = 'Your song starts in: 10'
		curr_msg = await self.send_message(msg.channel, message)
		for i in range(1, 10):
			await asyncio.sleep(1)
			message = 'Your song starts in: {}'.format(10 - i)
			await self.edit_message(curr_msg, message)
		await asyncio.sleep(1)
		message = 'BOOOOOOOM!!!!'
		await self.edit_message(curr_msg, message)
		await self.delete_message(curr_msg)

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
# ========================================================#
Main()  # Main Part of Your Bot	!!!				          #
# ========================================================#
##########################################################
