import unittest
import math
import boat
from unittest import mock


class TestBoatController(unittest.TestCase):
	def setUp(self):
		self.boat = mock.Mock(pos=(0, 0), vel=0, angle=math.pi/4, motor_angle=boat.DEFAULT_TURN_ANGLE, angle_vel=0, gear=0)
		self.physics_object_controller = mock.Mock()
		self.boat_controller = boat.BoatController(self.physics_object_controller)
		
	def testRaiseGear(self):
		result_boat = self.boat_controller.raise_gear(self.boat)
		
		self.assertEqual(1, result_boat.gear)
		
	def testRaiseGearLimit(self):
		self.boat.gear = boat.MAX_GEAR
		
		result_boat = self.boat_controller.raise_gear(self.boat)
		
		self.assertEqual(boat.MAX_GEAR, result_boat.gear)
		
	def testLowerGear(self):
		result_boat = self.boat_controller.lower_gear(self.boat)
		
		self.assertEqual(-1, result_boat.gear)
		
	def testLowerGearLimit(self):
		self.boat.gear = boat.MIN_GEAR
		
		result_boat = self.boat_controller.lower_gear(self.boat)
		
		self.assertEqual(boat.MIN_GEAR, result_boat.gear)
		
	def testTurnLeft(self):
		result_boat = self.boat_controller.turn_left(self.boat)
		
		self.assertEqual(self.boat.motor_angle - boat.DEFAULT_TURN_ANGLE, result_boat.motor_angle)
		
	def testTurnLeftLimit(self):
		self.boat.motor_angle = -boat.MOTOR_TURN_LIMIT
		
		result_boat = self.boat_controller.turn_left(self.boat)
		
		self.assertEqual(-boat.MOTOR_TURN_LIMIT, self.boat.motor_angle)
		
	def testTurnRight(self):
		result_boat = self.boat_controller.turn_right(self.boat)
		
		self.assertEqual(self.boat.motor_angle + boat.DEFAULT_TURN_ANGLE, result_boat.motor_angle)
		
	def testTurnRightLimit(self):
		self.boat.motor_angle = boat.MOTOR_TURN_LIMIT
		
		result_boat = self.boat_controller.turn_right(self.boat)
		
		self.assertEqual(boat.MOTOR_TURN_LIMIT, self.boat.motor_angle)

	def testUpdate(self):
		delta = 2
		
		result_boat = self.boat_controller.update(self.boat, delta)
		
		forward_force = (self.boat.gear * math.cos(self.boat.motor_angle), self.boat.angle + self.boat.motor_angle)
		angular_force = self.boat.gear * math.sin(self.boat.motor_angle)
		
		self.physics_object_controller.apply_force.assert_called_once_with(self.boat, forward_force)
		resultant = self.physics_object_controller.apply_force(self.boat, forward_force)
		
		self.physics_object_controller.apply_angular_force.assert_called_once_with(resultant, angular_force)
		resultant = self.physics_object_controller.apply_angular_force(resultant, angular_force)
		
		self.physics_object_controller.update.assert_called_once_with(resultant, delta)
		resultant = self.physics_object_controller.update(resultant, delta)
		
		self.assertEqual(result_boat, resultant)

		
class TestBoatDrawer(unittest.TestCase):
	def setUp(self):
		self.d_surf = mock.Mock()
		self.boat = mock.Mock()
		self.rot_img_drawer = mock.Mock()
		self.boat_drawer = boat.BoatDrawer(self.rot_img_drawer)
		
	def testDraw(self):
		self.boat_drawer.draw(self.d_surf, self.boat)
		
		self.rot_img_drawer.draw.assert_called_once_with(self.d_surf, self.boat.image, self.boat.pos, self.boat.angle)
		

class TestBoatAudioManager(unittest.TestCase):
	def setUp(self):
		self.boat = mock.Mock(gear=2)
		self.sound_manager = mock.Mock()
		self.boat_audio_manager = boat.BoatAudioManager(self.sound_manager)

	def testUpdate(self):
		gear_engine_sound_interval = boat.GEAR_ENGINE_SOUND_INTERVAL_DIVISOR / self.boat.gear

		self.boat_audio_manager.update(self.boat, gear_engine_sound_interval / 2)
		self.sound_manager.play.assert_not_called()

		self.boat_audio_manager.update(self.boat, gear_engine_sound_interval / 2)
		self.sound_manager.play.assert_called_once_with(boat.ENGINE_SOUND_KEY)
		