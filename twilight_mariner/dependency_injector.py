import inspect


class DependencyInjector:
	def __init__(self):
		self.modules = set()
		self.class_instance_dict = {}
	
	def register_modules(self, *modules):
		self.modules.update(modules)
		self.class_types = self.get_class_types()
		self.class_init_params = self.get_class_init_params()
	
	def get_class_types(self):
		class_types = {}
		for module in self.modules:
			for class_name, class_type in inspect.getmembers(module, inspect.isclass):
				class_types[class_name] = class_type
		return class_types
		
	def get_class_init_params(self):
		class_init_params = {}
		for class_name, class_type in self.class_types.items():
			init_params = list(map(snake_case_to_proper_case, inspect.getfullargspec(class_type.__init__).args[1:]))
			class_init_params[class_name] = init_params
		return class_init_params
	
	def inject(self):
		classes_to_inject = self.get_classes_to_inject()
		while classes_to_inject:
			for class_name in set(classes_to_inject):
				init_param_instances = [self.class_instance_dict.get(param) for param in self.class_init_params[class_name]]
				if all(init_param_instances):
					self.class_instance_dict[class_name] = self.class_types[class_name](*init_param_instances)
					classes_to_inject.remove(class_name)
	
	def get_classes_to_inject(self):
		all_classes = set(self.class_instance_dict.keys()) | set(self.class_types.keys())
		classes_to_inject = set()
		for class_name, init_params in self.class_init_params.items():
			if all([param_class in all_classes for param_class in init_params]):
				classes_to_inject.add(class_name)
		return classes_to_inject
	
	def get(self, class_name):
		return self.class_instance_dict.get(class_name)


def snake_case_to_proper_case(s):
	return s.title().replace('_', '')
