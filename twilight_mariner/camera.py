class Camera:
	def __init__(self, display_dims, pos=(0, 0)):
		self.display_dims = display_dims
		self.pos = pos


class CameraController:
	def __init__(self):
		pass

	def update(self, camera, focus_object):
		new_pos = (focus_object.pos[0] - camera.display_dims[0] / 2, focus_object.pos[1] - camera.display_dims[1] / 2)
		return Camera(camera.display_dims, new_pos)
