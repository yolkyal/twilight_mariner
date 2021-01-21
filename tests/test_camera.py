import unittest
from twilight_mariner import camera
from unittest import mock


class TestCameraController(unittest.TestCase):
	def setUp(self):
		self.display_dims = (2, 2)
		self.spring = mock.Mock()
		self.spring_controller = mock.Mock()
		self.physics_object_controller = mock.Mock()
		self.camera = camera.Camera(self.display_dims, self.spring, (0, 0))
		self.camera_controller = camera.CameraController(self.physics_object_controller, self.spring_controller)

	def testUpdate(self):
		delta_s = 2

		result = self.camera_controller.update(self.camera, delta_s)

		self.physics_object_controller.update.assert_called_once_with(self.camera, delta_s)
		self.assertEqual(self.physics_object_controller.update(self.camera, delta_s), result)

	def testAnchorToPoint(self):
		target_point = (20, 20)

		result = self.camera_controller.anchor_to_point(self.camera, target_point)

		expected_source_point = (self.camera.pos[0] + self.display_dims[0] / 2, self.camera.pos[1] + self.display_dims[1] / 2)

		self.spring_controller.apply_force.assert_called_once_with(self.spring, self.camera, expected_source_point, target_point)
		self.assertEqual(result, self.spring_controller.apply_force(self.spring, self.camera, expected_source_point, target_point))
