import pygame, math, sys
from dependency_injector import DependencyInjector
import world, boat, camera, graphics, physics, trig 


BG_COL = (47,79,79)


def inject_classes():
	dependency_injector = DependencyInjector()
	dependency_injector.register_modules(world, boat, camera, graphics, physics, trig)
	dependency_injector.inject()
	return dependency_injector


def create_world(size, image_manager):
	boat_start_pos = (400, 400)
	_boat = boat.Boat(image_manager.get('BOAT_IMAGE'), image_manager.get('BOAT_TURN_SPOT'), boat_start_pos)

	_camera = camera.Camera(size)

	return world.World(size, _camera, _boat)


def main():
	pygame.init()
	size = width, height = 800, 800
	d_surf = pygame.display.set_mode(size)
	clock = pygame.time.Clock()
	
	context = inject_classes()

	image_manager = context.get('ImageManager')
	image_manager.put('BOAT_IMAGE', 'images/basic_boat.png', (48, 120))
	image_manager.put('WATERY_LIGHT', 'images/watery_light.png', (64, 64))
	image_manager.put('BOAT_TURN_SPOT', 'images/boat_turn_spot.png', (8, 8))

	_world = create_world(size, image_manager)

	world_drawer = context.get('WorldDrawer')
	world_controller = context.get('WorldController')
	world_io_handler = context.get('WorldIOHandler')

	while True:
		delta_ms = clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
				_world = world_io_handler.handle_event(_world, event)
				
		_world = world_controller.update(_world, delta_ms)
		
		d_surf.fill(BG_COL)

		light_pos = (300 - _world.camera.pos[0], 300 - _world.camera.pos[1])
		d_surf.blit(image_manager.get('WATERY_LIGHT'), light_pos)
		world_drawer.draw(d_surf, _world)
		
		pygame.display.update()
	
	
if __name__ == '__main__':
	main()