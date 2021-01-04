import unittest
from twilight_mariner import audio
from unittest import mock


class TestAudioManager(unittest.TestCase):
	def setUp(self):
		self.sound = mock.Mock()
		self.sound_manager = audio.SoundManager()
	
	def testPutAndPlay(self):
		key = 'key'

		self.sound_manager.put(key, self.sound)
		self.sound_manager.play(key)

		self.sound.play.assert_called_once()
