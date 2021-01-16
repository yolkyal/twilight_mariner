import unittest
from twilight_mariner import camera
from unittest import mock


class TestCameraController(unittest.TestCase):
	def setUp(self):
		self.spring = mock.Mock()
		self.spring_controller = mock.Mock()
		self.physics_object_controller = mock.Mock()
		self.camera = camera.Camera((0, 0), self.spring)
		self.camera_controller = camera.CameraController(self.physics_object_controller, self.spring_controller)

	def testUpdate(self):
		delta_s = 2

		result = self.camera_controller.update(self.camera, delta_s)

		self.physics_object_controller.update.assert_called_once_with(self.camera, delta_s)
		self.assertEqual(self.physics_object_controller.update(self.camera, delta_s), result)

	def testAnchorToPoint(self):
		target_point = (10, 10)

		result = self.camera_controller.anchor_to_point(self.camera, target_point)

		self.spring_controller.apply_force.assert_called_once_with(self.spring, self.camera, target_point)
		self.assertEqual(result, self.spring_controller.apply_force(self.spring, self.camera, target_point))
