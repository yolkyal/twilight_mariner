import unittest
import pygame
from twilight_mariner import world
from unittest import mock


class TestWorldController(unittest.TestCase):
	def setUp(self):
		self.world = mock.Mock()
		self.boat_controller = mock.Mock()
		self.camera_controller = mock.Mock()
		self.world_controller = world.WorldController(self.boat_controller, self.camera_controller)
	
	def testUpdate(self):
		delta_ms = 2000
		delta_s = 2
	
		result_world = self.world_controller.update(self.world, delta_ms)

		anchored_camera = self.camera_controller.anchor_to_point(self.world.camera, self.world.boat)
		
		self.boat_controller.update.assert_called_once_with(self.world.boat, delta_s)
		self.camera_controller.update.assert_called_once_with(anchored_camera, delta_s)
		self.assertEqual(result_world.boat, self.boat_controller.update(self.world.boat, delta_s))
		self.assertEqual(result_world.camera, self.camera_controller.update(anchored_camera, delta_s))
		
	def testRaiseBoatGear(self):
		result_world = self.world_controller.raise_boat_gear(self.world)
		
		self.assertEqual(result_world.boat, self.boat_controller.raise_gear(self.world.boat))
		
	def testLowerBoatGear(self):
		result_world = self.world_controller.lower_boat_gear(self.world)
		
		self.assertEqual(result_world.boat, self.boat_controller.lower_gear(self.world.boat))
		
	def testTurnBoatLeft(self):
		result_world = self.world_controller.turn_boat_left(self.world)
		
		self.assertEqual(result_world.boat, self.boat_controller.turn_left(self.world.boat))
		
	def testTurnBoatRight(self):
		result_world = self.world_controller.turn_boat_right(self.world)
		
		self.assertEqual(result_world.boat, self.boat_controller.turn_right(self.world.boat))
		

class TestWorldDrawer(unittest.TestCase):
	def setUp(self):
		self.d_surf = mock.Mock()
		self.world = mock.Mock()
		self.boat_drawer = mock.Mock()
		self.world_drawer = world.WorldDrawer(self.boat_drawer)
		
	def testDraw(self):
		self.world_drawer.draw(self.d_surf, self.world)
		
		self.boat_drawer.draw.assert_called_once_with(self.d_surf, self.world.boat, self.world.camera)
		

class TestWorldIOHandler(unittest.TestCase):
	def setUp(self):
		self.world = mock.Mock()
		self.world_controller = mock.Mock()
		self.world_io_handler = world.WorldIOHandler(self.world_controller)

	def testHandleEventKeyDownJ(self):
		event = mock.Mock(type=pygame.KEYDOWN, key=pygame.K_j)

		result_world = self.world_io_handler.handle_event(world, event)
		
		self.assertEqual(result_world, self.world_controller.raise_boat_gear(world))

	def testHandleEventKeyDownL(self):
		event = mock.Mock(type=pygame.KEYDOWN, key=pygame.K_l)

		result_world = self.world_io_handler.handle_event(world, event)
		
		self.assertEqual(result_world, self.world_controller.lower_boat_gear(world))

	def testHandleEventKeyDownA(self):
		event = mock.Mock(type=pygame.KEYDOWN, key=pygame.K_a)

		result_world = self.world_io_handler.handle_event(world, event)
		
		self.assertEqual(result_world, self.world_controller.turn_boat_left(world))

	def testHandleEventKeyDownD(self):
		event = mock.Mock(type=pygame.KEYDOWN, key=pygame.K_d)

		result_world = self.world_io_handler.handle_event(world, event)
		
		self.assertEqual(result_world, self.world_controller.turn_boat_right(world))
