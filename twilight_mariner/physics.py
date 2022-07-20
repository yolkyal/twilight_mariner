import math
import copy


class Spring:
	def __init__(self, strength, target_length):
		self.strength = strength
		self.target_length = target_length


class PhysicsObjectController:
	def __init__(self):
		pass
		
	def apply_force(self, obj, force):
		new_obj = copy.copy(obj)
		new_obj.vel = (obj.vel[0] + force[0] * math.cos(force[1]), obj.vel[1] + force[0] * math.sin(force[1]))
		return new_obj
		
	def apply_angular_force(self, obj, force):
		new_obj = copy.copy(obj)
		new_obj.angular_vel = obj.angular_vel + force * obj.angular_vel_force_multiplier
		return new_obj
		
	def update(self, obj, delta):
		new_obj = copy.copy(obj)
		new_obj.pos = (obj.pos[0] + obj.vel[0] * delta, obj.pos[1] + obj.vel[1] * delta)
		new_obj.vel = (obj.vel[0] * obj.drag, obj.vel[1] * obj.drag)
		if hasattr(obj, 'angular_vel'):
			new_obj.angular_vel = obj.angular_vel * obj.drag
			new_obj.angle = obj.angle + obj.angular_vel * delta
		return new_obj


class SpringController:
	def __init__(self, physics_object_controller):
		self.physics_object_controller = physics_object_controller

	def apply_force(self, spring, physics_obj, source_pos, target_pos):
		diff_x = target_pos[0] - source_pos[0]
		diff_y = target_pos[1] - source_pos[1]
		current_length = math.sqrt(diff_x**2 + diff_y**2)
		
		extension = current_length - spring.target_length
		magnitude = spring.strength * extension
		direction = math.atan2(diff_y, diff_x)

		return self.physics_object_controller.apply_force(physics_obj, (magnitude, direction))