from random import random


class Song:
	def __init__(self, url=None):
		self.url = url
		self._download()
		self._skip = False
		self._downloaded = False
		self.is_playing = False
		self._ctx = {}
		self.buffer = None
		self.description = self._get_description()

	@property
	def skip(self):
		return self._skip

	@skip.setter
	def skip(self, value: bool = True):
		self._skip = value

	@property
	def name(self):
		return self._ctx.get('name')

	@property
	def duration(self):
		return self._ctx.get('duration')

	@property
	def ready(self):
		return True if self._downloaded and not self.is_playing else False

	def _download(self):
		"""
			Method to get download song and description via  ytdl lib

		:return: Dictionary with all downloaded info
		"""
		if not self.skip:
			pass
		pass
		self.buffer = None
		self.ctx = {}
		self._downloaded = True
		return

	def _get_description(self):
		"""
			Method to get all onfo about song from self.ctx.
			Like: ' "Some song name" uploaded by "Super youtuber 228" - (13:37)'

		:return: String with all info
		"""
		return ''

	def __str__(self):
		return self.description


class Playlist:
	Songs = []

	def __init__(self, id, name=None, songs=None):
		if songs:
			self.Songs = songs
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

	def __init__(self, lists=None):
		if not lists:
			self.Lists = {}
		else:
			self.Lists = lists

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
