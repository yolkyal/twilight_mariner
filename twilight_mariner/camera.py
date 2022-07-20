class Camera:
	def __init__(self, display_dims, anchor_spring, pos, vel=(0, 0)):
		self.display_dims = display_dims
		self.anchor_spring = anchor_spring
		self.pos = pos
		self.vel = vel
		self.drag = 0.95


class CameraController:
	def __init__(self, physics_object_controller, spring_controller):
		self.physics_object_controller = physics_object_controller
		self.spring_controller = spring_controller

	def update(self, camera, delta):
		return self.physics_object_controller.update(camera, delta)

	def anchor_to_point(self, camera, point):
		return self.spring_controller.apply_force(camera.anchor_spring, camera, (camera.pos[0] + camera.display_dims[0] / 2, camera.pos[1] + camera.display_dims[1] / 2), point)