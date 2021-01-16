import pygame


class World:
	def __init__(self, size, camera, boat):
		self.size = size
		self.camera = camera
		self.boat = boat
		

class WorldController:
	def __init__(self, boat_controller, camera_controller):
		self.boat_controller = boat_controller
		self.camera_controller = camera_controller
		
	def update(self, world, delta_ms):
		return World(world.size, self.camera_controller.update(world.camera, delta_ms / 1000), self.boat_controller.update(world.boat, delta_ms / 1000))
		
	def raise_boat_gear(self, world):
		return World(world.size, world.camera, self.boat_controller.raise_gear(world.boat))
		
	def lower_boat_gear(self, world):
		return World(world.size, world.camera, self.boat_controller.lower_gear(world.boat))
		
	def turn_boat_left(self, world):
		return World(world.size, world.camera, self.boat_controller.turn_left(world.boat))
		
	def turn_boat_right(self, world):
		return World(world.size, world.camera, self.boat_controller.turn_right(world.boat))
		
		
class WorldDrawer:
	def __init__(self, boat_drawer):
		self.boat_drawer = boat_drawer
		
	def draw(self, d_surf, world):
		self.boat_drawer.draw(d_surf, world.boat)


class WorldIOHandler:
	def __init__(self, world_controller):
		self.world_controller = world_controller

	def handle_event(self, world, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_j:
				return self.world_controller.raise_boat_gear(world)
			elif event.key == pygame.K_l:
				return self.world_controller.lower_boat_gear(world)
			elif event.key == pygame.K_a:
				return self.world_controller.turn_boat_left(world)
			elif event.key == pygame.K_d:
				return self.world_controller.turn_boat_right(world)
		return world