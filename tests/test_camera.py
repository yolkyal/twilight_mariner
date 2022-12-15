import unittest
from twilight_mariner import camera
from unittest import mock


class TestCameraController(unittest.TestCase):
	def setUp(self):
		self.display_dims_x = 2
		self.display_dims_y = 4
		self.camera = camera.Camera((self.display_dims_x, self.display_dims_y))
		self.camera_controller = camera.CameraController()

	def testUpdate(self):
		focus_object_x = 4
		focus_object_y = 16
		focus_object = mock.Mock(pos=(focus_object_x, focus_object_y))

		result_camera = self.camera_controller.update(self.camera, focus_object)

		self.assertEqual(result_camera.pos, (focus_object_x - self.display_dims_x / 2, focus_object_y - self.display_dims_y / 2))
