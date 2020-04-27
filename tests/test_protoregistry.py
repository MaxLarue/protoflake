import unittest
from unittest.mock import patch
from unittest.mock import Mock

from protoregistry import ProtoRegistry
from protoregistry import ProtoModuleNotFound
from protoregistry import ProtoClassNotFound
from protoregistry import ProtoClassNotAClass


FAKE_ATTR = 'hello'


class TestProtoRegistry(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = ProtoRegistry()

    def test_it_can_retrieve_itself(self):
        self.assertEqual(self.registry.get('protoregistry', 'ProtoRegistry'), ProtoRegistry)

    @patch('protoregistry.inspect.isclass')
    @patch('protoregistry.importlib')
    def test_it_only_retrieve_modules_once_for_the_same_class(self, importlib_mock, isclass_mock):
        isclass_mock.return_value = True
        import_mock = Mock()
        importlib_mock.import_module = import_mock
        module_name = 'fake.module'
        module_mock = Mock()
        class_name = 'MyClass'
        class_mock = Mock()
        setattr(module_mock, class_name, class_mock)
        import_mock.return_value = module_mock
        self.assertEqual(self.registry.get(module_name, class_name), class_mock)
        import_mock.assert_called_once()
        self.registry.get(module_name, class_name)
        import_mock.assert_called_once()
        import_mock.assert_called_with(module_name)

    @patch('protoregistry.inspect.isclass')
    @patch('protoregistry.importlib')
    def test_it_only_retrieve_modules_once_for_different_class_same_module(self, importlib_mock, isclass_mock):
        isclass_mock.return_value = True
        import_mock = Mock()
        importlib_mock.import_module = import_mock
        module_name = 'fake.module'
        module_mock = Mock()
        class_one_name = 'ClassOne'
        class_one_mock = Mock()
        class_two_name = 'ClassTwo'
        class_two_mock = Mock()
        setattr(module_mock, class_one_name, class_one_mock)
        setattr(module_mock, class_two_name, class_two_mock)
        import_mock.return_value = module_mock
        self.assertEqual(self.registry.get(module_name, class_one_name), class_one_mock)
        self.assertEqual(self.registry.get(module_name, class_two_name), class_two_mock)
        import_mock.assert_called_once()
        import_mock.assert_called_with(module_name)

    def test_it_throws_proto_module_not_found_if_module_not_found(self):
        with self.assertRaises(ProtoModuleNotFound):
            self.registry.get('some.thing.that.will.never.exist', 'AClass')

    @patch('protoregistry.importlib')
    def test_it_throws_proto_class_not_found_if_module_does_not_have_class(self, importlib_mock):
        import_mock = Mock()
        import_mock.return_value = 'some thing without class attribute'
        importlib_mock.import_module = import_mock
        with self.assertRaises(ProtoClassNotFound):
            self.registry.get('some.fake.module', 'ClassThatDoesNotExist')

    def test_it_throws_proto_class_not_a_class_if_module_attribute_is_not_a_class(self):
        with self.assertRaises(ProtoClassNotAClass):
            self.registry.get('tests.test_protoregistry', 'FAKE_ATTR')
