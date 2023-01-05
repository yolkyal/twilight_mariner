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


class ImgDrawer:
	def __init__(self):
		pass

	def draw(self, d_surf, image, pos):
		d_surf.blit(image, (pos[0] - image.get_width() / 2, pos[1] - image.get_height() / 2))


class RotImgDrawer:
	def __init__(self, img_drawer):
		self.img_drawer = img_drawer

	def draw(self, d_surf, image, pos, angle):
		rot_img_surf = pygame.transform.rotate(image, math.degrees(1.5 * math.pi - angle))
		self.img_drawer.draw(d_surf, rot_img_surf, pos)