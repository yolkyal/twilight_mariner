import math


class SimplePhysicsObject:
	def __init__(self, pos):
		self.pos = pos
		self.vel = (0, 0)
		self.angle = 0
		self.angular_vel = (0, 0)

	def with_pos(self, pos):
		self.pos = pos

	def with_vel(self, vel):
		self.vel = vel

	def with_angle(self, angle):
		self.angle = angle

	def with_angular_vel(self, angular_vel):
		self.angular_vel = angular_vel


class Spring:
	def __init__(self, strength, target_length):
		self.strength = strength
		self.target_length = target_length


class PhysicsObjectController:
	def __init__(self):
		pass
		
	def apply_force(self, obj, force):
		return obj.with_vel((obj.vel[0] + force[0] * math.cos(force[1]), obj.vel[1] + force[0] * math.sin(force[1])))
		
	def apply_angular_force(self, obj, force):
		return obj.with_angular_vel(obj.angular_vel + force * obj.angular_vel_force_multiplier)
		
	def update(self, obj, delta): 
		return obj.with_pos((obj.pos[0] + obj.vel[0] * delta, obj.pos[1] + obj.vel[1] * delta)).with_vel((obj.vel[0] * obj.drag, obj.vel[1] * obj.drag)).with_angular_vel(obj.angular_vel * obj.drag).with_angle(obj.angle + obj.angular_vel * delta)


class SpringController:
	def __init__(self, physics_object_controller):
		self.physics_object_controller = physics_object_controller

	def apply_force(self, spring, obj, target_pos):
		diff_x = target_pos[0] - obj.pos[0]
		diff_y = target_pos[1] - obj.pos[1]
		current_length = math.sqrt(diff_x**2 + diff_y**2)
		extension = spring.target_length - current_length
		mag = spring.strength * extension
		direction = math.atan2(diff_y, diff_x)

		return self.physics_object_controller.apply_force(obj, (mag, direction))
