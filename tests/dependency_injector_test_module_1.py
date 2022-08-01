class TestObj:
	def __init__(self, first, second):
		self.first = first
		self.second = second


class TestSimpleController:
	def __init__(self):
		pass


class TestComplexController:
	def __init__(self, test_simple_controller):
		self.test_simple_controller = test_simple_controller
