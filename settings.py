import os

import yaml

from utils import get_dict, silent_remove, valid_server


class Settings:
	"""
		Class to stoge and control settings for different servers.
	"""

	Settings = {}  # Store in


	def __init__(self, settings_folder):
		"""
			Constructor method for Settings class.

		:param settings_folder: Takes setting directory to store setting in *.yml format in it
		"""
		self.SettingsFolder = settings_folder
		self.__load_settings()

	def __load_settings(self):
		"""
			Method to create settings directory if not exist and control the settings loading process.

		:return: None
		"""
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
		"""
			Method to collect all config files from the self.SettingsFolder directory.

		:return: List of settings files
		"""
		files = os.listdir(self.SettingsFolder)
		files = list(filter(lambda x: x.endswith('.yml'), files))
		return files

	def _update_cfg_from_files(self, files):
		"""
			Method to load settings to list from given files.

		:param files: Takes list of settings files
		:return: None
		"""
		for file in files:
			with open(self.SettingsFolder + file, 'r') as f:
				self._add_cfg_to_list(file[:-4], yaml.load(f))

	def _add_cfg_to_list(self, server_id, cfg):
		"""
			Method to store cfg dictionary in self.Settings dictionary in association with server id.

		:param server_id: Takes string with server id
		:return: Link to the cfg stored in self.Settings
		"""
		self.Settings.update(get_dict(server_id, cfg))
		return self.Settings.get(server_id)

	def _remove_cfg_from_list(self, server_id):
		"""
			Method to remove cfg associated with given server id from self.Settings dictionary.

		:param server_id: Takes string with server id
		:return: True if cfg associated with given server id was in list, else - None.
		"""
		return True if self.Settings.pop(server_id, None) else False

	def _get_cfg_from_list(self, server_id):
		"""
			Method to get cfg dictionary associated with given server id.

		:param server_id: Takes string with server id
		:return: Cfg dictionary if exist, else - None
		"""
		return self.Settings.get(server_id)

	def _save_cfg_to_file(self, server_id, cfg):
		"""
			Method to save cfg dictionary to yml file.

		:param server_id: Takes string with server id
		:param cfg: Takes cfg dictionary
		:return: None
		"""
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
		"""
			Method to remove local file assotiated with given id.

		:param server_id: Takes string with server id
		:return: None
		"""
		silent_remove(self.SettingsFolder + '{}.yml'.format(server_id))

	def _update_server_cfg(self, server_id, cfg):
		"""
			Method to update cfg associated with given server id  from given cfg.

		:param server_id: Takes string with server id
		:param cfg: Cfg to update server settings from
		:return: New cfg dictionary file
		"""
		cfg = self._add_cfg_to_list(server_id, cfg)
		self._save_cfg_to_file(server_id, cfg)
		return cfg

	def _reset_server_settings(self, server_id):
		"""
			Method to reset setting associated with gived server id, incuding local files.

		:param server_id: Takes string with server id
		:return: None
		"""
		self._remove_cfg_from_list(server_id)
		self._remove_settings_file(server_id)

	@staticmethod
	def valid_cfg(cfg):
		"""
			Method to check if given object is dictionary. If not raises TypeError

		:param cfg: Object to check
		:return: Given object
		"""
		if not isinstance(cfg, dict):
			raise TypeError('Config should be a python dictionary')
		return cfg

	#########################################
	#
	#   Public member methods
	#
	#########################################
	# TODO: Should i check files for settings or just list. If all setting load during init, and all new auto save hm..
	def get_cfg(self, server):
		server = valid_server(server)
		return self._get_cfg_from_list(server)

	# if not cfg:
	# 	cfg = self._get_cfg_from_file(server)

	def set_cfg(self, server, cfg):
		cfg = self.valid_cfg(cfg)
		server = valid_server(server)
		self._reset_server_settings(server)
		self._update_server_cfg(server, cfg)

	def update_cfg(self, server, cfg):
		cfg = self.valid_cfg(cfg)
		server = valid_server(server)
		self._update_server_cfg(server, cfg)

	def reset_cfg(self, server):
		server = valid_server(server)
		self._reset_server_settings(server)

	def set_attr(self, server, key, value):
		key = str(key)
		server = valid_server(server)
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
