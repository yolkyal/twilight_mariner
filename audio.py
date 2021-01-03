import pygame


class SoundManager:
	def __init__(self):
		self.sounds = {}
		
	def put(self, key, sound):
		self.sounds[key] = sound
		
	def play(self, key):
		self.sounds[key].play()