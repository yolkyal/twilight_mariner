import pygame


DEFAULT_WATER_RIPPLE_COLOR = (100, 0, 0)
DEFAULT_WATER_RIPPLE_SPEED = 2
DEFAULT_WATER_RIPPLE_FADE_RATE = 0.999
DEFAULT_WATER_RIPPLE_OPACITY_LIMIT = 1


class WaterRipple:
	def __init__(self, pos, size, color, remove=False):
		self.pos = pos
		self.size = size
		self.color = color
		self.remove = remove


class WaterRippleDrawer:
	def __init__(self):
		pass

	def draw(self, d_surf, water_ripple):
		rounded_color = self._calc_rounded_color(water_ripple.color)
		pygame.draw.circle(d_surf, rounded_color, water_ripple.pos, water_ripple.size)

	def _calc_rounded_color(self, color):
		return (color[0], color[1], color[2], int(color[3]))

class WaterRippleController:
	def __init__(self):
		pass

	def update(self, water_ripple):
		new_color = self._calc_new_color(water_ripple.color)
		return WaterRipple(water_ripple.pos, water_ripple.size * DEFAULT_WATER_RIPPLE_SPEED, new_color, new_color[3] <= DEFAULT_WATER_RIPPLE_OPACITY_LIMIT)

	def _calc_new_color(self, color):
		return (color[0], color[1], color[2], color[3] * DEFAULT_WATER_RIPPLE_FADE_RATE)
