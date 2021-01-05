import math


class PhysicsObjectController:
	def __init__(self):
		pass
		
	def apply_force(self, obj, force):
		return obj.with_vel((obj.vel[0] + force[0] * math.cos(force[1]), obj.vel[1] + force[0] * math.sin(force[1])))
		
	def apply_angular_force(self, obj, force):
		return obj.with_angular_vel(obj.angular_vel + force * obj.angular_vel_force_multiplier)
		
	def update(self, obj, delta):
		return obj.with_pos((obj.pos[0] + obj.vel[0] * delta, obj.pos[1] + obj.vel[1] * delta)).with_vel((obj.vel[0] * obj.drag, obj.vel[1] * obj.drag)).with_angular_vel(obj.angular_vel * obj.drag).with_angle(obj.angle + obj.angular_vel * delta)

	def get_resultant_pos(self, obj, delta):
		return (obj.pos[0] + obj.vel[0] * delta, obj.pos[1] + obj.vel[1] * delta)

	def get_resultant_vel(self, obj, delta):
		return (obj.vel[0] * obj.drag, obj.vel[1] * obj.drag)

	def get_resultant_angle(self, obj, delta):
		return obj.angle + obj.angular_vel * delta

	def get_resultant_angular_vel(self, obj):
		return obj.angular_vel * obj.drag