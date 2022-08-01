import unittest
import math
from twilight_mariner import boat
from unittest import mock


class TestBoatController(unittest.TestCase):
	def setUp(self):
		self.image = mock.Mock()
		self.turn_spot_image = mock.Mock()
		self.pos = (0, 0)
		self.vel = 1
		self.angle = math.pi / 4
		self.gear = 1
		self.motor_angle = boat.DEFAULT_TURN_ANGLE
		self.boat = boat.Boat(self.image, self.turn_spot_image, self.pos, self.vel, self.angle, motor_angle=self.motor_angle, gear=self.gear)
		self.physics_object_controller = mock.Mock()
		self.boat_controller = boat.BoatController(self.physics_object_controller)
		
	def testRaiseGear(self):
		result_boat = self.boat_controller.raise_gear(self.boat)
		
		self.assertEqual(self.boat.gear + 1, result_boat.gear)
		
	def testRaiseGearLimit(self):
		self.boat.gear = boat.MAX_GEAR
		
		result_boat = self.boat_controller.raise_gear(self.boat)
		
		self.assertEqual(boat.MAX_GEAR, result_boat.gear)
		
	def testLowerGear(self):
		result_boat = self.boat_controller.lower_gear(self.boat)
		
		self.assertEqual(self.boat.gear - 1, result_boat.gear)
		
	def testLowerGearLimit(self):
		self.boat.gear = boat.MIN_GEAR
		
		result_boat = self.boat_controller.lower_gear(self.boat)
		
		self.assertEqual(boat.MIN_GEAR, result_boat.gear)
		
	def testTurnLeft(self):
		result_boat = self.boat_controller.turn_left(self.boat)
		
		self.assertEqual(self.boat.motor_angle - boat.DEFAULT_TURN_ANGLE, result_boat.motor_angle)
		self.assertEqual(self.boat.turn_gear - 1, result_boat.turn_gear)
		
	def testTurnLeftLimit(self):
		self.boat.motor_angle = -boat.MOTOR_TURN_LIMIT
		self.boat.turn_gear = boat.MIN_TURN_GEAR
		
		result_boat = self.boat_controller.turn_left(self.boat)
		
		self.assertEqual(-boat.MOTOR_TURN_LIMIT, result_boat.motor_angle)
		self.assertEqual(boat.MIN_TURN_GEAR, result_boat.turn_gear)
		
	def testTurnRight(self):
		result_boat = self.boat_controller.turn_right(self.boat)
		
		self.assertEqual(self.boat.motor_angle + boat.DEFAULT_TURN_ANGLE, result_boat.motor_angle)
		self.assertEqual(self.boat.turn_gear + 1, result_boat.turn_gear)
		
	def testTurnRightLimit(self):
		self.boat.motor_angle = boat.MOTOR_TURN_LIMIT
		self.boat.turn_gear = boat.MAX_TURN_GEAR
		
		result_boat = self.boat_controller.turn_right(self.boat)
		
		self.assertEqual(boat.MOTOR_TURN_LIMIT, result_boat.motor_angle)
		self.assertEqual(boat.MAX_TURN_GEAR, result_boat.turn_gear)
	
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
		self.camera = mock.Mock(pos=(1, 1))

		self.boat = mock.Mock(pos=(2, 2), angle=math.pi/4, turn_gear=1)

		self.rot_img_drawer = mock.Mock()
		self.trig_calculator = mock.Mock()
		self.boat_drawer = boat.BoatDrawer(self.rot_img_drawer, self.trig_calculator)
		
	def testDraw(self):
		self.boat_drawer.draw(self.d_surf, self.boat, self.camera)

		offset_boat_pos = (self.boat.pos[0] - self.camera.pos[0], self.boat.pos[1] - self.camera.pos[1])

		turn_spot_pos_1 = self.trig_calculator.calc_point(offset_boat_pos, self.boat.angle, boat.DEFAULT_TURN_SPOT_DISTANCE)
		turn_spot_pos_2 = self.trig_calculator.calc_point(offset_boat_pos, self.boat.angle + boat.DEFAULT_TURN_SPOT_SEPARATION_DEGREE, boat.DEFAULT_TURN_SPOT_DISTANCE)

		expected_call_args = [
			mock.call(self.d_surf, self.boat.image, offset_boat_pos, self.boat.angle),
			mock.call(self.d_surf, self.boat.turn_spot_image, turn_spot_pos_1, self.boat.angle),
			mock.call(self.d_surf, self.boat.turn_spot_image, turn_spot_pos_2, self.boat.angle + boat.DEFAULT_TURN_SPOT_SEPARATION_DEGREE)
		]
		self.assertEqual(expected_call_args, self.rot_img_drawer.draw.call_args_list)
