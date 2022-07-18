import math

class TrigCalculator:
	def __init__(self):
		pass

	def calc_point(self, point, angle, magnitude):
		return (point[0] + magnitude * math.cos(angle), point[1] + magnitude * math.sin(angle))