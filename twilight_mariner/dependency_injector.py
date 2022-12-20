import inspect


class DependencyInjector:
	def __init__(self):
		self._registered_modules = set()
		self._registered_classes = {}
		self._class_init_params = {}
		self._injectable_classes = set()
		self._injected_objects = {}
	
	def register_modules(self, *modules):
		self._registered_modules.update(modules)
		self._register_classes()
		self._register_class_init_params()
		self._register_injectable_classes()
	
	def inject(self):
		classes_to_inject = self._injectable_classes - set(self._injected_objects.keys())
		while classes_to_inject:
			class_name = classes_to_inject.pop(0)
			init_param_objects = [self._injected_objects.get(param) for param in self._class_init_params[class_name]]
			if all(init_param_objects):
				self._injected_objects[class_name] = self.registered_classes[class_name](*init_param_objects)
			else:
				classes_to_inject.append(class_name)
	
	def get(self, class_name):
		return self._injected_objects.get(class_name)
	
	def _register_classes(self):
		for module in self._registered_modules:
			self._registered_classes.update({class_name: class_type for class_name, class_type in inspect.getmembers(module, inspect.isclass)})
	
	def _register_class_init_params(self):
		for class_name, class_type in self.registered_classes.items():
			class_init_params = list(map(snake_case_to_proper_case, inspect.getfullargspec(class_type.__init__).args[1:]))
			self._class_init_params.update({class_name: class_init_params})
	
	def _register_injectable_classes(self):
		for class_name, init_params in self._class_init_params.items():
			if all([param_class in self.registered_classes for param_class in init_params]):
				self._injectable_classes.add(class_name)


def snake_case_to_proper_case(s):
	return s.title().replace('_', '')
