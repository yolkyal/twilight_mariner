import pygame, math, sys
from world import World, WorldDrawer, WorldController, WorldIOHandler
from boat import Boat, BoatDrawer, BoatController
from graphics import ImageManager, RotImgDrawer
from physics import Spring, SpringController, PhysicsObjectController
from camera import Camera, CameraController
from trig import TrigCalculator


BG_COL = (47,79,79)


def main():
	pygame.init()
	size = width, height = 800, 800
	d_surf = pygame.display.set_mode(size)
	clock = pygame.time.Clock()

	image_manager = ImageManager()
	image_manager.put('BOAT_IMAGE', 'images/basic_boat.png', (48, 120))
	image_manager.put('WATERY_LIGHT', 'images/watery_light.png', (64, 64))
	image_manager.put('BOAT_TURN_SPOT', 'images/boat_turn_spot.png', (16, 16))
	
	boat_start_pos = (400, 400)
	boat_start_angle = 0
	boat_start_motor_angle = 0
	boat = Boat(image_manager.get('BOAT_IMAGE'), boat_start_pos, (0, 0), 0, boat_start_angle, boat_start_motor_angle)

	camera_anchor_spring = Spring(0.1, 100)
	camera = Camera(size, camera_anchor_spring, (60, 60))

	world = World(size, camera, boat)
	world_controller = WorldController(BoatController(PhysicsObjectController()), CameraController(PhysicsObjectController(), SpringController(PhysicsObjectController())))
	world_io_handler = WorldIOHandler(world_controller)
	
	world_drawer = WorldDrawer(BoatDrawer(RotImgDrawer(), TrigCalculator(), image_manager.get('BOAT_TURN_SPOT')))
	
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

		light_pos = (300 - world.camera.pos[0], 300 - world.camera.pos[1])
		d_surf.blit(image_manager.get('WATERY_LIGHT'), light_pos)
		world_drawer.draw(d_surf, world)
		
		pygame.display.update()
	
	
if __name__ == '__main__':
	main()