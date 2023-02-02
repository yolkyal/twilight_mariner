import inspect
from collections import deque


class DependencyInjector:

	def __init__(self):
		self._classes = {}
		self._class_init_params = {}
		self._injectable_classes = set()
		self._injected_objects = {}
	
	def register_modules(self, *modules):
		self._register_classes(modules)
		self._register_class_init_params()
		self._register_injectable_classes()
	
	def inject(self):
		classes_to_inject = deque(self._injectable_classes - self._injected_objects.keys())
		while classes_to_inject:
			class_name = classes_to_inject.popleft()
			init_param_objects = [self._injected_objects.get(param) for param in self._class_init_params[class_name]]
			if all(init_param_objects):
				self._injected_objects[class_name] = self._classes[class_name](*init_param_objects)
			else:
				classes_to_inject.append(class_name)
	
	def get(self, class_name):
		return self._injected_objects.get(class_name)
	
	def _register_classes(self, modules):
		self._classes.update({class_name: class_type for module in modules for class_name, class_type in classes(module)})
	
	def _register_class_init_params(self):
		for class_name, class_type in self._classes.items():
			class_init_params = list(map(snake_case_to_proper_case, init_params(class_type)))
			self._class_init_params.update({class_name: class_init_params})
	
	def _register_injectable_classes(self):
		for class_name, init_params in self._class_init_params.items():
			if all([param in self._classes for param in init_params]):
				self._injectable_classes.add(class_name)


def classes(module):
	return inspect.getmembers(module, inspect.isclass)


def init_params(class_type):
	return inspect.getfullargspec(class_type.__init__).args[1:]


def snake_case_to_proper_case(s):
	return s.title().replace('_', '')
