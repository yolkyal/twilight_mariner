import math


MAX_GEAR = 2
MIN_GEAR = -2
DEFAULT_TURN_ANGLE = math.pi/64
MOTOR_TURN_LIMIT = DEFAULT_TURN_ANGLE * 5
DEFAULT_DRAG = 0.97
DEFAULT_ANGULAR_VEL_FORCE_MULTIPLIER = math.pi / 32


class Boat:
	def __init__(self, image, pos, vel, angular_vel, angle, motor_angle, gear=0):
		self.image = image
		self.pos = pos
		self.vel = vel
		self.angular_vel = angular_vel
		self.angle = angle
		self.motor_angle = motor_angle
		self.gear = gear
		self.drag = DEFAULT_DRAG
		self.angular_vel_force_multiplier = DEFAULT_ANGULAR_VEL_FORCE_MULTIPLIER
		
	def with_pos(self, pos):
		return Boat(self.image, pos, self.vel, self.angular_vel, self.angle, self.motor_angle, self.gear)

	def with_vel(self, vel):
		return Boat(self.image, self.pos, vel, self.angular_vel, self.angle, self.motor_angle, self.gear)
		
	def with_angle(self, angle):
		return Boat(self.image, self.pos, self.vel, self.angular_vel, angle, self.motor_angle, self.gear)

	def with_angular_vel(self, angular_vel):
		return Boat(self.image, self.pos, self.vel, angular_vel, self.angle, self.motor_angle, self.gear)

		
class BoatController:
	def __init__(self, physics_object_controller):
		self.physics_object_controller = physics_object_controller
		
	def update(self, boat, delta):
		tmp = self.physics_object_controller.apply_force(boat, (boat.gear * math.cos(boat.motor_angle), boat.angle + boat.motor_angle))
		tmp = self.physics_object_controller.apply_angular_force(tmp, boat.gear * math.sin(boat.motor_angle))
		return self.physics_object_controller.update(tmp, delta)
		
	def turn_left(self, boat):
		return Boat(boat.image, boat.pos, boat.vel, boat.angular_vel, boat.angle, max(boat.motor_angle - DEFAULT_TURN_ANGLE, -MOTOR_TURN_LIMIT), boat.gear)
		
	def turn_right(self, boat):
		return Boat(boat.image, boat.pos, boat.vel, boat.angular_vel, boat.angle, min(boat.motor_angle + DEFAULT_TURN_ANGLE, MOTOR_TURN_LIMIT), boat.gear)
		
	def raise_gear(self, boat):
		return Boat(boat.image, boat.pos, boat.vel, boat.angular_vel, boat.angle, boat.motor_angle, min(boat.gear + 1, MAX_GEAR))

	def lower_gear(self, boat):
		return Boat(boat.image, boat.pos, boat.vel, boat.angular_vel, boat.angle, boat.motor_angle, max(boat.gear - 1, MIN_GEAR))


class BoatDrawer:
	def __init__(self, rot_img_drawer):
		self.rot_img_drawer = rot_img_drawer

	def draw(self, d_surf, boat, camera):
		offset_pos = (boat.pos[0] - camera.pos[0], boat.pos[1] - camera.pos[1])
		self.rot_img_drawer.draw(d_surf, boat.image, offset_pos, boat.angle)

		
ENGINE_SOUND_KEY = 0
GEAR_ENGINE_SOUND_INTERVAL_DIVISOR = 1


class BoatAudioManager:
	def __init__(self, sound_manager):
		self.sound_manager = sound_manager
		self.sound_last_played_map = {ENGINE_SOUND_KEY: 0}

	def update(self, boat, delta):
		if boat.gear == 0: return

		engine_sound_interval = self.sound_last_played_map[ENGINE_SOUND_KEY] + delta
		if engine_sound_interval >= GEAR_ENGINE_SOUND_INTERVAL_DIVISOR / abs(boat.gear):
			self.sound_manager.play(ENGINE_SOUND_KEY)
			self.sound_last_played_map[ENGINE_SOUND_KEY] = 0
		else:
			self.sound_last_played_map[ENGINE_SOUND_KEY] = engine_sound_interval