import math

class Spring:
	def __init__(self, strength, target_length):
		self.strength = strength
		self.target_length = target_length


class SpringForceCalculator:
	def init__(self):
		pass

	def get_applied_force(self, spring, obj, target):
		diff_x = target[0] - obj[0]
		diff_y = target[1] - obj[1]
		current_length = math.sqrt(diff_x**2 + diff_y**2)
		extension = spring.target_length - current_length
		mag = spring.strength * extension
		direction = math.atan2(diff_y, diff_x)

		return (mag, direction)


class PhysicsObjectController:
	def __init__(self):
		pass
		
	def apply_force(self, obj, force):
		return obj.with_vel((obj.vel[0] + force[0] * math.cos(force[1]), obj.vel[1] + force[0] * math.sin(force[1])))
		
	def apply_angular_force(self, obj, force):
		return obj.with_angular_vel(obj.angular_vel + force * obj.angular_vel_force_multiplier)
		
	def update(self, obj, delta): 
		return obj.with_pos((obj.pos[0] + obj.vel[0] * delta, obj.pos[1] + obj.vel[1] * delta)).with_vel((obj.vel[0] * obj.drag, obj.vel[1] * obj.drag)).with_angular_vel(obj.angular_vel * obj.drag).with_angle(obj.angle + obj.angular_vel * delta)