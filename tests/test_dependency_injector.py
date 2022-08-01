import unittest
import dependency_injector_test_module_1 as test_module_1
import dependency_injector_test_module_2 as test_module_2

from twilight_mariner import dependency_injector


class DependencyInjectorTest(unittest.TestCase):
	def setUp(self):
		self.dependency_injector = dependency_injector.DependencyInjector()

	def testInjectSingleModule(self):
		self.dependency_injector.register_modules(test_module_1)
		self.dependency_injector.inject()

		self.assertIsNotNone(self.dependency_injector.get('TestSimpleController'))
		self.assertIsInstance(self.dependency_injector.get('TestSimpleController'), test_module_1.TestSimpleController)
		
		self.assertIsNotNone(self.dependency_injector.get('TestComplexController'))
		self.assertIsInstance(self.dependency_injector.get('TestComplexController'), test_module_1.TestComplexController)
		self.assertEqual(self.dependency_injector.get('TestSimpleController'), self.dependency_injector.get('TestComplexController').test_simple_controller)
		
		self.assertIsNone(self.dependency_injector.get('TestObj'))

	def testInjectCrossModule(self):
		self.dependency_injector.register_modules(test_module_1, test_module_2)
		self.dependency_injector.inject()

		self.assertIsNotNone(self.dependency_injector.get('TestCrossModuleComplexController'))
		self.assertIsInstance(self.dependency_injector.get('TestCrossModuleComplexController'), test_module_2.TestCrossModuleComplexController)
		self.assertEqual(self.dependency_injector.get('TestComplexController'), self.dependency_injector.get('TestCrossModuleComplexController').test_complex_controller)
