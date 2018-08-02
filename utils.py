import os
from datetime import datetime


class Error(Exception):
	def __init__(self, message, content=None, embed=True, file=False):
		self.message = message
		self.content = content
		self.embed = embed
		self.isfile = file
		self.time = datetime.now()
# def __str__(self):
# 	return self.message


class Success(Exception):
	def __init__(self, message, content=None, embed=False, file=False):
		self.message = message
		self.content = content
		self.embed = embed
		self.isfile = file
		self.time = datetime.now()
# def __str__(self):
# 	return self.message

class Say:
	__errors = {
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
		'22': 'Do not try to deceive me and slowly, so that I see your hands, come to my server',
	}

	@classmethod
	def error(cls, code):
		message = cls.__errors.get(str(code), 'Unknown error')
		raise Error(message)

	@classmethod
	def success(cls, message, *args):
		raise Success(message, *args)


def silent_remove(filename):
	try:
		os.remove(filename)
	except OSError:
		pass


def get_dict(key, value):
	try:
		result = float(value)
	except:
		result = value
	return dict([(key, result)])


# TODO: Log system
def chat_log(msg):
	log = '[CHATLOG] ({}) [{}] <{}> {}: {}'
	log = log.format(msg.timestamp, msg.server.name, msg.channel.name, msg.author.display_name, msg.content)
	print(log)


def is_youtube_list(url):
	return True if ('youtu.be' or 'youtube.com' in url) and ('list=' in url) else False


def is_youtube_link(url):
	return True if 'youtu.be' or 'youtube.com' in url else False
