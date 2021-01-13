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
		self.physics_object.with_vel.assert_called_once_with(expected_vel)
		self.assertEqual(result_obj, self.physics_object.with_vel(expected_vel))
		
	def testApplyAngularForce(self):
		force = 2
		
		result_obj = self.physics_object_controller.apply_angular_force(self.physics_object, force)
		
		expected_angular_vel = self.angular_vel + force * self.angular_vel_force_multiplier
		self.physics_object.with_angular_vel.assert_called_once_with(expected_angular_vel)
		self.assertEqual(result_obj, self.physics_object.with_angular_vel(expected_angular_vel))
		
	def testUpdate(self):
		delta = 2
		
		result_obj = self.physics_object_controller.update(self.physics_object, delta)
	
		expected_pos = (self.pos[0] + self.vel[0] * delta, self.pos[1] + self.vel[1] * delta)
		expected_vel = (self.vel[0] * self.drag, self.vel[1] * self.drag)
		expected_angular_vel = self.angular_vel * self.drag
		expected_angle = self.angle + self.angular_vel * delta
		
		self.physics_object.with_pos.assert_called_once_with(expected_pos)
		resultant = self.physics_object.with_pos(expected_pos)
		
		resultant.with_vel.assert_called_with(expected_vel)
		resultant = resultant.with_vel(expected_vel)
		
		resultant.with_angular_vel.assert_called_with(expected_angular_vel)
		resultant = resultant.with_angular_vel(expected_angular_vel)
		
		resultant.with_angle.assert_called_with(expected_angle)
		resultant = resultant.with_angle(expected_angle)
	
		self.assertEqual(resultant, result_obj)


class TestSpringForceCalculator(unittest.TestCase):
	def setUp(self):
		self.strength = 2
		self.target_length = 3
		self.spring = physics.Spring(self.strength, self.target_length)
		self.spring_force_calculator = physics.SpringForceCalculator()

	def testGetAppliedForce(self):
		source = (0, 0)
		target = (5, 5)

		result = self.spring_force_calculator.get_applied_force(self.spring, source, target)

		diff_x = target[0] - source[0]
		diff_y = target[1] - source[1]
		current_length = math.sqrt(diff_x**2 + diff_y**2)
		expected_mag = self.strength * (self.target_length - current_length)
		expected_direction = math.atan2(diff_y, diff_x)

		self.assertEqual((expected_mag, expected_direction), result)