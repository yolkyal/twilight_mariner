import pygame, math, sys
from world import World, WorldDrawer, WorldController, WorldIOHandler
from boat import Boat, BoatDrawer, BoatController
from graphics import ImageManager, RotImgDrawer
from physics import PhysicsObjectController


BG_COL = (47,79,79)


def main():
	pygame.init()
	size = width, height = 800, 800
	d_surf = pygame.display.set_mode(size)
	clock = pygame.time.Clock()

	boat_image_id = 0
	image_manager = ImageManager()
	image_manager.put(boat_image_id, 'images/basic_boat.png', (48, 120))
	
	boat_start_pos = (400, 400)
	boat_start_angle = 0
	boat_start_motor_angle = 0
	boat = Boat(image_manager.get(boat_image_id), boat_start_pos, (0, 0), 0, boat_start_angle, boat_start_motor_angle)

	world = World(size, boat)
	world_controller = WorldController(BoatController(PhysicsObjectController()))
	world_io_handler = WorldIOHandler(world_controller)
	
	world_drawer = WorldDrawer(BoatDrawer(RotImgDrawer()))
	
	while True:
		delta_ms = clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
				world = world_io_handler.handle_event(world, event)
				
		world = world_controller.update(world, delta_ms)
		
		d_surf.fill(BG_COL)
		world_drawer.draw(d_surf, world)
		
		pygame.display.update()
	
	
if __name__ == '__main__':
	main()