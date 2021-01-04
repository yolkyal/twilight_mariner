import unittest, math
from twilight_mariner import graphics
from unittest import mock


class TestRotImgDrawer(unittest.TestCase):
	def setUp(self):
		self.d_surf = mock.Mock()
		self.image = mock.Mock()
		self.rot_img_drawer = graphics.RotImgDrawer()

	@mock.patch('pygame.transform.rotate')
	def testDraw(self, mock_transform_rotate):
		pos, angle = (0, 0), 2
		rot_img_surf = mock.Mock()
		rot_img_surf.get_width.return_value = 16
		rot_img_surf.get_height.return_value = 32
		mock_transform_rotate.return_value = rot_img_surf

		self.rot_img_drawer.draw(self.d_surf, self.image, pos, angle)

		mock_transform_rotate.assert_called_once_with(self.image, math.degrees(1.5 * math.pi - angle))
		rot_img_surf.get_width.assert_called_once()
		rot_img_surf.get_height.assert_called_once()
		self.d_surf.blit.assert_called_with(rot_img_surf, (pos[0] - rot_img_surf.get_width() / 2, pos[1] - rot_img_surf.get_height() / 2))
		