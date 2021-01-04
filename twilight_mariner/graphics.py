import math
import pygame


class ImageManager:
	def __init__(self):
		self.images = {}

	def put(self, k, image_filepath, size):
		image = pygame.image.load(image_filepath)
		image = pygame.transform.scale(image, size)
		self.images[k] = image

	def get(self, image_id):
		return self.images[image_id]


class RotImgDrawer:
	def __init__(self):
		pass

	def draw(self, d_surf, image, pos, angle):
		rot_img_surf = pygame.transform.rotate(image, math.degrees(1.5 * math.pi - angle))
		d_surf.blit(rot_img_surf, (pos[0] - rot_img_surf.get_width() / 2, pos[1] - rot_img_surf.get_height() / 2))