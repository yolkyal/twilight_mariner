import unittest
from twilight_mariner import water
from unittest import mock


class TestWaterRippleController(unittest.TestCase):
	def setUp(self):
		self.pos = (0, 0)
		self.size = 10
		self.color = (100, 100, 100, 100)
		self.water_ripple = water.WaterRipple(self.pos, self.size, self.color)
		self.water_ripple_controller = water.WaterRippleController()

	def testUpdate(self):
		result = self.water_ripple_controller.update(self.water_ripple)

		self.assertEqual(self.pos, result.pos)
		self.assertEqual(self.size * water.DEFAULT_WATER_RIPPLE_SPEED, result.size)
		self.assertEqual((100, 100, 100, 100 * water.DEFAULT_WATER_RIPPLE_FADE_RATE), result.color)

	def testUpdateExpire(self):
		self.water_ripple = water.WaterRipple(self.pos, self.size, (100, 100, 100, water.DEFAULT_WATER_RIPPLE_OPACITY_LIMIT))

		result = self.water_ripple_controller.update(self.water_ripple)

		self.assertTrue(result.remove)


class TestWaterRippleDrawer(unittest.TestCase):
	def setUp(self):
		self.d_surf = mock.Mock()
		self.pos = (0, 0)
		self.size = 10
		self.color = (100, 100, 100, 100.1)
		self.water_ripple = water.WaterRipple(self.pos, self.size, self.color)
		self.water_ripple_drawer = water.WaterRippleDrawer()

	@mock.patch('pygame.draw.circle')
	def testDraw(self, mock_draw_circle):
		self.water_ripple_drawer.draw(self.d_surf, self.water_ripple)

		mock_draw_circle.assert_called_once_with(self.d_surf, (100, 100, 100, 100), self.pos, self.size)
