import unittest, math
from twilight_mariner import graphics
from unittest import mock


class TestImgDrawer(unittest.TestCase):
	def setUp(self):
		self.d_surf = mock.Mock()
		self.image = mock.Mock()
		self.img_drawer = graphics.ImgDrawer()

	def testDraw(self):
		pos = (0, 0)
		self.image.get_width.return_value = 16
		self.image.get_height.return_value = 32

		self.img_drawer.draw(self.d_surf, self.image, pos)

		self.d_surf.blit.assert_called_with(self.image, (pos[0] - self.image.get_width() / 2, pos[1] - self.image.get_height() / 2))


class TestRotImgDrawer(unittest.TestCase):
	def setUp(self):
		self.d_surf = mock.Mock()
		self.image = mock.Mock()
		self.img_drawer = mock.Mock()
		self.rot_img_drawer = graphics.RotImgDrawer(self.img_drawer)

	@mock.patch('pygame.transform.rotate')
	def testDraw(self, mock_transform_rotate):
		pos, angle = (0, 0), 2
		rot_img_surf = mock.Mock()
		mock_transform_rotate.return_value = rot_img_surf

		self.rot_img_drawer.draw(self.d_surf, self.image, pos, angle)

		mock_transform_rotate.assert_called_once_with(self.image, math.degrees(1.5 * math.pi - angle))
		self.img_drawer.draw.assert_called_once_with(self.d_surf, rot_img_surf, pos)