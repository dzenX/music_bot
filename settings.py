import os

import yaml
from discord import Server

from utils import get_dict, silent_remove


class Settings:
	Settings = {}

	def __init__(self, settings_folder):
		self.SettingsFolder = settings_folder
		self.__load_settings()

	def __load_settings(self):
		print('[INFO] Trying to load saved settings')
		if not os.path.isdir(self.SettingsFolder):
			os.makedirs(self.SettingsFolder)
			print('[WARNING] No saved settings directory found, so ill create it')
		else:
			print('[INFO] Loading settings from files')
			files = self._get_settings_files()
			if not files:
				print('[WARNING] No saved settings found in \'{}\' directory'.format(self.SettingsFolder))
			else:
				self._update_cfg_from_files(files)
				print('[INFO] Settings successfully loaded')
		print('------')

	def _get_settings_files(self):
		files = os.listdir(self.SettingsFolder)
		files = list(filter(lambda x: x.endswith('.yml'), files))
		return files

	def _update_cfg_from_files(self, files):
		for file in files:
			with open(self.SettingsFolder + file, 'r') as f:
				self._add_cfg_to_list(file[:-4], yaml.load(f))

	def _add_cfg_to_list(self, server_id, cfg):
		self.Settings.update(get_dict(server_id, cfg))
		return self.Settings.get(server_id)

	def _remove_cfg_from_list(self, server_id):
		return True if self.Settings.pop(server_id, None) else False

	def _get_cfg_from_list(self, server_id):
		return self.Settings.get(server_id)

	def _save_cfg_to_file(self, server_id, cfg):
		file = self.SettingsFolder + '{}.yml'.format(server_id)
		with open(file, 'w') as f:
			yaml.dump(cfg, f, default_flow_style=False)

	# def _get_cfg_from_file(self, server_id):
	# 	file = self.SettingsFolder + '{}.yml'.format(server_id)
	# 	if os.path.isfile(file):
	# 		with open(file, 'r') as f:
	# 			cfg = yaml.load(f)
	# 		return cfg

	def _remove_settings_file(self, server_id):
		silent_remove(self.SettingsFolder + '{}.yml'.format(server_id))

	def _update_server_cfg(self, server_id, cfg):
		cfg = self._add_cfg_to_list(server_id, cfg)
		self._save_cfg_to_file(server_id, cfg)

	def _reset_server_settings(self, server_id):
		self._remove_cfg_from_list(server_id)
		self._remove_settings_file(server_id)

	@staticmethod
	def valid_server(server):
		if isinstance(server, Server):
			return server.id
		return server

	@staticmethod
	def valid_cfg(cfg):
		if not isinstance(cfg, dict):
			raise TypeError('Config should be a python dictionary')
		return cfg

	#########################################
	#
	#   Public functions
	#
	#########################################
	# TODO: Should i check files for settings or just list. If all setting load during init, and all new auto save hm..
	def get_cfg(self, server):
		server = self.valid_server(server)
		return self._get_cfg_from_list(server)

	# if not cfg:
	# 	cfg = self._get_cfg_from_file(server)

	def set_cfg(self, server, cfg):
		cfg = self.valid_cfg(cfg)
		server = self.valid_server(server)
		self._reset_server_settings(server)
		self._update_server_cfg(server, cfg)

	def update_cfg(self, server, cfg):
		cfg = self.valid_cfg(cfg)
		server = self.valid_server(server)
		self._update_server_cfg(server, cfg)

	def reset_cfg(self, server):
		server = self.valid_server(server)
		self._reset_server_settings(server)

	def set_attr(self, server, key, value):
		key = str(key)
		server = self.valid_server(server)
		self._update_server_cfg(server, get_dict(key, value))

	def get_attr(self, server, key):
		key = str(key)
		cfg = self.get_cfg(server)
		if cfg:
			return cfg.get(key)

	def reset_attr(self, server, key):
		key = str(key)
		cfg = self.get_cfg(server)
		if cfg:
			return cfg.pop(key, None)
