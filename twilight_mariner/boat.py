import math
import copy


MAX_GEAR = 2
MIN_GEAR = -2
MAX_TURN_GEAR = 3
MIN_TURN_GEAR = -3
DEFAULT_TURN_ANGLE = math.pi/128
MOTOR_TURN_LIMIT = DEFAULT_TURN_ANGLE * MAX_TURN_GEAR
DEFAULT_DRAG = 0.97
DEFAULT_ANGULAR_VEL_FORCE_MULTIPLIER = math.pi / 32
DEFAULT_TURN_SPOT_DISTANCE = 70
DEFAULT_TURN_SPOT_SEPARATION_DEGREE = math.pi / 16
DEFAULT_GEAR_DISPLAY_PADDING = 60
DEFAULT_GEAR_DISPLAY_COLOUR = (225, 225, 225)


class Boat:
	def __init__(self, image, turn_spot_image, gear_font, pos, vel=(0, 0), angle=0, angular_vel=0, motor_angle=0, gear=0, turn_gear=0):
		self.image = image
		self.turn_spot_image = turn_spot_image
		self.pos = pos
		self.vel = vel
		self.angle = angle
		self.angular_vel = angular_vel
		self.motor_angle = motor_angle
		self.gear = gear
		self.turn_gear = turn_gear
		self.drag = DEFAULT_DRAG
		self.angular_vel_force_multiplier = DEFAULT_ANGULAR_VEL_FORCE_MULTIPLIER
		self.turn_spot_image = turn_spot_image
		self.gear_font = gear_font


class BoatController:
	def __init__(self, physics_object_controller):
		self.physics_object_controller = physics_object_controller

	def update(self, boat, delta):
		tmp = self.physics_object_controller.apply_force(boat, (boat.gear * math.cos(boat.motor_angle), boat.angle + boat.motor_angle))
		tmp = self.physics_object_controller.apply_angular_force(tmp, boat.gear * math.sin(boat.motor_angle))
		return self.physics_object_controller.update(tmp, delta)

	def turn_left(self, boat):
		new_boat = copy.copy(boat)
		new_boat.motor_angle = max(boat.motor_angle - DEFAULT_TURN_ANGLE, -MOTOR_TURN_LIMIT)
		new_boat.turn_gear = max(boat.turn_gear - 1, MIN_TURN_GEAR)
		return new_boat

	def turn_right(self, boat):
		new_boat = copy.copy(boat)
		new_boat.motor_angle = min(boat.motor_angle + DEFAULT_TURN_ANGLE, MOTOR_TURN_LIMIT)
		new_boat.turn_gear = min(boat.turn_gear + 1, MAX_TURN_GEAR)
		return new_boat

	def raise_gear(self, boat):
		new_boat = copy.copy(boat)
		new_boat.gear = min(boat.gear + 1, MAX_GEAR)
		return new_boat

	def lower_gear(self, boat):
		new_boat = copy.copy(boat)
		new_boat.gear = max(boat.gear - 1, MIN_GEAR)
		return new_boat


class BoatDrawer:
	def __init__(self, img_drawer, rot_img_drawer, text_drawer, trig_calculator):
		self.img_drawer = img_drawer
		self.rot_img_drawer = rot_img_drawer
		self.text_drawer = text_drawer
		self.trig_calculator = trig_calculator

	def draw(self, d_surf, boat, camera):
		boat_centre_pos = (boat.pos[0] - camera.pos[0], boat.pos[1] - camera.pos[1])
		self.rot_img_drawer.draw(d_surf, boat.image, boat_centre_pos, boat.angle)
		self._draw_turn_gear_hud(d_surf, boat, boat_centre_pos)
		self._draw_gear_text(d_surf, boat, boat_centre_pos)

	def _draw_turn_gear_hud(self, d_surf, boat, boat_centre_pos):
		if boat.turn_gear < 0:
			for i in range(0, boat.turn_gear - 1, -1):
				hud_point_pos = self.trig_calculator.calc_point(boat_centre_pos, boat.angle + i * DEFAULT_TURN_SPOT_SEPARATION_DEGREE, DEFAULT_TURN_SPOT_DISTANCE)
				self.img_drawer.draw(d_surf, boat.turn_spot_image, hud_point_pos)
		elif boat.turn_gear > 0:
			for i in range(0, boat.turn_gear + 1):
				hud_point_pos = self.trig_calculator.calc_point(boat_centre_pos, boat.angle + i * DEFAULT_TURN_SPOT_SEPARATION_DEGREE, DEFAULT_TURN_SPOT_DISTANCE)
				self.img_drawer.draw(d_surf, boat.turn_spot_image, hud_point_pos)
		else:
			hud_point_pos = self.trig_calculator.calc_point(boat_centre_pos, boat.angle, DEFAULT_TURN_SPOT_DISTANCE)
			self.img_drawer.draw(d_surf, boat.turn_spot_image, hud_point_pos)

	def _draw_gear_text(self, d_surf, boat, boat_centre_pos):
		gear_text_pos = (boat_centre_pos[0] - DEFAULT_GEAR_DISPLAY_PADDING, boat_centre_pos[1] - DEFAULT_GEAR_DISPLAY_PADDING)
		self.text_drawer.draw(d_surf, boat.gear_font, str(boat.gear), gear_text_pos, DEFAULT_GEAR_DISPLAY_COLOUR)
