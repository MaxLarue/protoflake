import unittest
from unittest.mock import Mock
from unittest.mock import call

from flakefactory import FlakeFactory
from descriptorbuilder import DescriptorBuilder
from flakebuilder import FlakeBuilder


class TestFlakeBuilder(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.flake_factory = FlakeFactory()
        self.proto_registry = Mock()
        self.flake_registry = Mock()
        self.builder = FlakeBuilder(
            self.flake_factory,
            self.flake_registry,
            self.proto_registry
        )
        self.descriptor_builder = DescriptorBuilder()

        class FakeProto:
            pass

        self.proto_registry.get.return_value = FakeProto
        self.flake_registry.has.return_value = False


class TestSimpleFlakeBuilder(TestFlakeBuilder):

    def test_it_builds_a_simple_flake(self):
        simple_descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'first flake',
            'proto': 'fake.class',
            'some_int': 1,
            'some_bool': True,
            'some_float': 1.5,
            'some_string': 'Hello World'
        })
        flake = self.builder.get_new(simple_descriptor)
        self.assertEqual(1, flake.some_int)
        self.assertEqual(True, flake.some_bool)
        self.assertEqual(1.5, flake.some_float)
        self.assertEqual('Hello World', flake.some_string)

    def test_with_list_property(self):
        simple_descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'first flake',
            'proto': 'fake.class',
            'some_list': [
                1, 2, 3
            ]
        })
        flake = self.builder.get_new(simple_descriptor)
        self.assertEqual(flake.some_list, [1, 2, 3])


class TestNestedFlakeBuilder(TestFlakeBuilder):

    def test_it_builds_nested_flakes(self):
        simple_descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'first flake',
            'proto': 'fake.class',
            'child': {
                'id': 'child flake',
                'proto': 'fake.class',
            },
        })
        flake = self.builder.get_new(simple_descriptor)
        self.assertEqual(flake.id, 'first flake')
        self.assertEqual(flake.child.id, 'child flake')

    def test_it_saved_both_nested_flakes_to_the_registry(self):
        simple_descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'first flake',
            'proto': 'fake.class',
            'child': {
                'id': 'child flake',
                'proto': 'fake.class',
            },
        })
        flake = self.builder.get_new(simple_descriptor)
        expected_calls = [
            call('child flake', flake.child),
            call('first flake', flake),
        ]
        self.flake_registry.set.assert_has_calls(expected_calls)

    def test_it_has_set_attrs_correctly_on_both(self):
        simple_descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'first flake',
            'proto': 'fake.class',
            'field': 1,
            'child': {
                'id': 'child flake',
                'proto': 'fake.class',
                'field': 2,
            },
        })
        flake = self.builder.get_new(simple_descriptor)
        self.assertEqual(1, flake.field)
        self.assertEqual(2, flake.child.field)


class TestNestedFlakeBuilderDifferentProto(TestFlakeBuilder):

    def setUp(self) -> None:
        super().setUp()

        class TestFirst:
            @staticmethod
            def is_first():
                return True

            @staticmethod
            def is_second():
                return False

        class TestSecond:
            @staticmethod
            def is_first():
                return False

            @staticmethod
            def is_second():
                return True

        self.first_test_class = TestFirst
        self.second_test_class = TestSecond

    def test_it_created_different_class_for_each(self):
        descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'parent',
            'proto': 'test.first',
            'child': {
                'id': 'child',
                'proto': 'test.second',
            }
        })
        # NB: the child is instantiated first
        self.proto_registry.get.side_effect = (self.second_test_class, self.first_test_class)
        flake = self.builder.build_from_descriptor(descriptor)
        self.assertTrue(flake.is_first())
        self.assertFalse(flake.is_second())
        self.assertTrue(flake.child.is_second())
        self.assertFalse(flake.child.is_first())

    def test_doubly_nested_flakes(self):
        descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'parent',
            'proto': 'test.first',
            'child': {
                'id': 'child',
                'proto': 'test.first',
                'child': {
                    'id': 'child child',
                    'proto': 'tes.first',
                },
            },
        })
        flake = self.builder.build_from_descriptor(descriptor)
        self.assertEqual(flake.id, 'parent')
        self.assertEqual(flake.child.id, 'child')
        self.assertEqual(flake.child.child.id, 'child child')


class TestReferenceFlakeBuilder(TestFlakeBuilder):

    def setUp(self) -> None:
        super().setUp()
        self.flake_mock = Mock()
        # parent is not known, child is
        self.flake_registry.has.side_effect = False, True
        self.flake_registry.get.return_value = self.flake_mock

    def test_it_will_use_a_reference_to_an_already_created_flake(self):
        descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'parent',
            'proto': 'test.first',
            'child': {
                'id': 'child',
                'is_flake_ref': True,
            }
        })
        flake = self.builder.build_from_descriptor(descriptor)
        self.assertEqual(flake.child, self.flake_mock)

    def test_asking_to_build_an_already_existing_flake(self):
        descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'some',
            'proto': 'some.class',
        })
        self.flake_registry.has('some')
        flake = self.builder.build_from_descriptor(descriptor)
        self.assertEqual(flake, self.flake_mock)


class TestListOfNestedFlakes(TestFlakeBuilder):

    def test_list_of_nested_flakes(self):
        descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'parent',
            'proto': 'test.first',
            'children': [
                {
                    'id': 'child-one',
                    'proto': 'test.first',
                },
                {
                    'id': 'child-two',
                    'proto': 'test.first',
                },
            ]
        })
        flake = self.builder.build_from_descriptor(descriptor)
        self.assertEqual('parent', flake.id)
        self.assertEqual(2, len(flake.children))
        self.assertEqual(flake.children[0].id, 'child-one')
        self.assertEqual(flake.children[1].id, 'child-two')


class TestNestedFlakeThatAlreadyExist(TestFlakeBuilder):

    def test_setting_a_ref_to_himself(self):
        descriptor = self.descriptor_builder.build_flake_descriptor({
            'id': 'parent',
            'proto': 'test.first',
            'child': {
                'is_flake_ref': True,
                'id': 'parent'
            }
        })
        fake_flake = Mock()
        self.flake_registry.get.return_value = fake_flake
        self.flake_registry.has.side_effect = False, True
        flake = self.builder.build_from_descriptor(descriptor)
        self.assertEqual(fake_flake, flake.child)


class TestFlakeBuilderHas(TestFlakeBuilder):

    def test_it_tells_us_if_flake_has_already_been_built(self):
        self.flake_registry.has.return_value = True
        self.assertTrue(self.builder.has('something'))
