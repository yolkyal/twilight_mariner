class Camera:
	def __init__(self, display_dims, anchor_spring, pos, vel=(0, 0)):
		self.display_dims = display_dims
		self.anchor_spring = anchor_spring
		self.pos = pos
		self.vel = vel
		self.angle = 0
		self.angular_vel = 0
		self.drag = 0.95

	def with_pos(self, pos):
		return Camera(self.display_dims, self.anchor_spring, pos, self.vel)

	def with_vel(self, vel):
		return Camera(self.display_dims, self.anchor_spring, self.pos, vel)

	def with_angle(self, angle):
		return self

	def with_angular_vel(self, angular_vel):
		return self


class CameraController:
	def __init__(self, physics_object_controller, spring_controller):
		self.physics_object_controller = physics_object_controller
		self.spring_controller = spring_controller

	def update(self, camera, delta):
		return self.physics_object_controller.update(camera, delta)

	def anchor_to_point(self, camera, point):
		return self.spring_controller.apply_force(camera.anchor_spring, camera, (camera.pos[0] + camera.display_dims[0] / 2, camera.pos[1] + camera.display_dims[1] / 2), point)
