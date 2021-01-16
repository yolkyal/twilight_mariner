class Camera:
	def __init__(self, pos, anchor_spring):
		self.pos = pos
		self.vel = (0, 0)
		self.angle = 0
		self.angular_vel = (0, 0)
		self.anchor_spring = anchor_spring

	def with_pos(self, pos):
		self.pos = pos

	def with_vel(self, vel):
		self.vel = vel

	def with_angle(self, angle):
		self.angle = angle

	def with_angular_vel(self, angular_vel):
		self.angular_vel = angular_vel


class CameraController:
	def __init__(self, physics_object_controller, spring_controller):
		self.physics_object_controller = physics_object_controller
		self.spring_controller = spring_controller

	def update(self, camera, delta):
		return self.physics_object_controller.update(camera, delta)

	def anchor_to_point(self, camera, point):
		return self.spring_controller.apply_force(camera.anchor_spring, camera, point)
