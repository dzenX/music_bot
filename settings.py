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
		:return: Link to the new cfg dictionary in self.Settings
		"""
		cfg = self._add_cfg_to_list(server_id, cfg)
		self._save_cfg_to_file(server_id, cfg)
		return cfg

	def _reset_server_settings(self, server_id):
		"""
			Method to reset setting associated with given server id, incuding local files.

		:param server_id: Takes string with server id
		:return: None
		"""
		self._remove_cfg_from_list(server_id)
		self._remove_settings_file(server_id)

	@staticmethod
	def valid_cfg(cfg):
		"""
			Method to check if given object is dictionary. If not raises TypeError.
			Used in public methods to check input.

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
	# TODO: Should i use @serverid deoorator or just valid_server()
	def get_cfg(self, server):
		"""
			Public method to get cfg dictionary associated with given server id.

		:param server: Takes server object ot just server id string
		:return: Cfg dictionary
		"""
		server = valid_server(server)
		return self._get_cfg_from_list(server)

	# if not cfg:
	# 	cfg = self._get_cfg_from_file(server)

	def set_cfg(self, server, cfg):
		"""
			Public method to set given config dictionary in associate with given server id.
			This method almost relace existed cfg with new given.

		:param server: Takes server object ot just server id string
		:param cfg: Takes cfg dictionary
		:return: Link to the cfg dictionary in the self.Settings
		"""
		cfg = self.valid_cfg(cfg)
		server = valid_server(server)
		self._reset_server_settings(server)
		return self._update_server_cfg(server, cfg)

	def update_cfg(self, server, cfg):
		"""
			Public method to update current config dictionary in associate with given server id with new given cfg.
			This method just update old config with new given.

		:param server: Takes server object ot just server id string
		:param cfg: Takes cfg dictionary
		:return: Link to the cfg dictionary in the self.Settings
		"""
		cfg = self.valid_cfg(cfg)
		server = valid_server(server)
		return self._update_server_cfg(server, cfg)

	def reset_cfg(self, server):
		"""
			Public method to reser settings associated with given server.

		:param server: Takes server object ot just server id string
		:return: None
		"""
		server = valid_server(server)
		self._reset_server_settings(server)

	def set_attr(self, server, attribute, value):
		"""
			Public method to set some given attribute in cfg associated with given server to new given value.
			This method just update old config with new given.

		:param server: Takes server object ot just server id string
		:param attribute: Takes string with attribute name
		:param value: Takes new value for given attribute
		:return: Link to the cfg dictionary in the self.Settings
		"""
		attribute = str(attribute)
		server = valid_server(server)
		return self._update_server_cfg(server, get_dict(attribute, value))

	def get_attr(self, server, attribute):
		"""
			Public method to get the value of some given attribute in cfg associated with given server.

		:param server: Takes server object ot just server id string
		:param attribute: Takes string with attribute name
		:return: Value of given attribute if exist, else - None
		"""
		attribute = str(attribute)
		cfg = self.get_cfg(server)
		if cfg:
			return cfg.get(attribute)

	def reset_attr(self, server, attribute):
		"""
			Public method to reset the value of some given attribute in cfg associated with given server.

		:param server: Takes server object ot just server id string
		:param attribute: Takes string with attribute name
		:return: Value of given attribute if exist, else - None
		"""
		attribute = str(attribute)
		cfg = self.get_cfg(server)
		if cfg:
			return cfg.pop(attribute, None)
