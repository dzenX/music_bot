from random import random


def prop_deco(func):
	def prop_deco_wrap(self, *args, **kwargs):
		func(self, *args, **kwargs)
		return self.ctx.get(func.__name__)

	return prop_deco_wrap


class Song:
	def __init__(self, url=None):
		self.url = url
		self._skip = False
		self.ctx = self._download()
		self.buffer = None
		self.description = self._get_description()
		self.player = self._get_player()

	def start(self):
		if not self.skip:
			self.player.start()

	@property
	def skip(self):
		return self._skip

	@skip.setter
	def skip(self, value: bool = True):
		self._skip = value

	@prop_deco
	@property
	def name(self):
		return

	@prop_deco
	@property
	def duration(self):
		return

	def _download(self):
		"""
			Method to get download song and description via  ytdl lib

		:return: Dictionary with all downloaded info
		"""
		return 1

	def _get_description(self):
		"""
			Method to get all onfo about song from self.ctx.
			Like: ' "Some song name" uploaded by "Super youtuber 228" - (13:37)'

		:return: String with all info
		"""
		return 1

	def __str__(self):
		return self.description

	def _get_player(self):
		return


class Playlist:
	Songs = []

	def __init__(self, id, name=None):
		self.name = name
		self.id = id

	def __str__(self):
		string = 'Playlist № {} : "{}":\n'
		for i in range(1, len(self.Songs)):
			string += 'Id: {}. {}.\n'.format(i, self.Songs[i])
		# songs = '\n'.join(song for song in self.Songs)
		return string

	def shuffle(self):
		random.shuffle(self.Songs)

	def run(self):
		for song in self.Songs:
			pass

	def _up(self, id):
		buff = self.Songs[id - 1]
		self.Songs[id - 1] = self.Songs[id]
		self.Songs[id] = buff

	def _down(self, id):
		buff = self.Songs[id + 1]
		self.Songs[id + 1] = self.Songs[id]
		self.Songs[id] = buff


class PlaylistControl:
	Lists = {}

	def __init__(self):
		pass

	def _get_min_free_id(self):
		seq = [x['the_key'] for x in self.Lists]
		for i in range(1, len(self.Lists) + 1):
			if i not in seq:
				return i

	def _get_list_by_name(self, name):
		for list in self.Lists:
			if list.name.lower() == name.lower():
				return list

	def _get_list_by_id(self, id):
		return self.Lists.get(id)

	def _create_list(self, name=None):
		id = self._get_min_free_id()
		self.Lists[id] = Playlist(id, name)
		return self.Lists[id]

	def _delete_list(self, id):
		return self.Lists.pop(id, None)
