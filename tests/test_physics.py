import unittest
import math
from twilight_mariner import physics
from unittest import mock


class TestPhysicsObjectController(unittest.TestCase):
	def setUp(self):
		self.pos = (1, 2)
		self.vel = (3, 4)
		self.angle = math.pi / 2
		self.angular_vel = math.pi / 4
		self.drag = 0.9
		self.angular_vel_force_multiplier = math.pi / 1024
		self.physics_object = mock.Mock(pos=self.pos, vel=self.vel, angular_vel=self.angular_vel, angle=self.angle, drag=self.drag, angular_vel_force_multiplier=self.angular_vel_force_multiplier)
		self.physics_object_controller = physics.PhysicsObjectController()
		
	def testApplyForce(self):
		force = (1, 2) # radial
		
		result_obj = self.physics_object_controller.apply_force(self.physics_object, force)
		
		expected_vel = (self.vel[0] + force[0] * math.cos(force[1]), self.vel[1] + force[0] * math.sin(force[1]))
		self.assertEqual(expected_vel, result_obj.vel)
		self.assertEqual(self.vel, self.physics_object.vel)
		
	def testApplyAngularForce(self):
		force = 2
		
		result_obj = self.physics_object_controller.apply_angular_force(self.physics_object, force)
		
		expected_angular_vel = self.angular_vel + force * self.angular_vel_force_multiplier
		self.assertEqual(expected_angular_vel, result_obj.angular_vel)
		self.assertEqual(self.angular_vel, self.physics_object.angular_vel)
		
	def testUpdate(self):
		delta = 2
		
		result_obj = self.physics_object_controller.update(self.physics_object, delta)
	
		expected_pos = (self.pos[0] + self.vel[0] * delta, self.pos[1] + self.vel[1] * delta)
		expected_vel = (self.vel[0] * self.drag, self.vel[1] * self.drag)
		expected_angular_vel = self.angular_vel * self.drag
		expected_angle = self.angle + self.angular_vel * delta
	
		self.assertEqual(expected_pos, result_obj.pos)
		self.assertEqual(expected_vel, result_obj.vel)
		self.assertEqual(expected_angular_vel, result_obj.angular_vel)
		self.assertEqual(expected_angle, result_obj.angle)
		
		self.assertEqual(self.pos, self.physics_object.pos)
		self.assertEqual(self.vel, self.physics_object.vel)
		self.assertEqual(self.angular_vel, self.physics_object.angular_vel)
		self.assertEqual(self.angle, self.physics_object.angle)


class TestSpringController(unittest.TestCase):
	def setUp(self):
		self.strength = 2
		self.target_length = 3
		self.spring = physics.Spring(self.strength, self.target_length)
		self.physics_object_controller = mock.Mock()
		self.spring_controller = physics.SpringController(self.physics_object_controller)

	def testGetAppliedForce(self):
		physics_obj = mock.Mock(pos=(0, 0))
		source_pos = (1, 1)
		target_pos = (2, 2)

		result = self.spring_controller.apply_force(self.spring, physics_obj, source_pos, target_pos)

		diff_x = target_pos[0] - source_pos[0]
		diff_y = target_pos[1] - source_pos[1]
		current_length = math.sqrt(diff_x**2 + diff_y**2)
		expected_mag = self.strength * (current_length - self.target_length)
		expected_direction = math.atan2(diff_y, diff_x)

		self.physics_object_controller.apply_force.assert_called_once_with(physics_obj, (expected_mag, expected_direction))
		self.assertEqual(result, self.physics_object_controller.apply_force(physics_obj, (expected_mag, expected_direction)))
