import unittest

from protoflake.flakefactory import FlakeFactory
from protoflake.flakefactory import FlakeAttributeOverwriting


class TestFlakeFactory(unittest.TestCase):

    def setUp(self) -> None:
        class TestClass(object):
            pass

        class WithAttr(object):
            from_class = 2

            def __init__(self):
                self.from_constructor = 1
        self.test_class = TestClass
        self.with_attrs = WithAttr

    def test_with_empty_data(self):
        flake = FlakeFactory.build_flake(self.test_class, {})
        self.assertIsInstance(flake, self.test_class)

    def test_with_some_data(self):
        flake = FlakeFactory.build_flake(self.test_class, {'prop': 5})
        self.assertEqual(flake.prop, 5)

    def test_mixin_with_usual_attributes(self):
        flake = FlakeFactory.build_flake(self.with_attrs, {'from_flake': 3})
        self.assertEqual(flake.from_constructor, 1)
        self.assertEqual(flake.from_class, 2)
        self.assertEqual(flake.from_flake, 3)

    def test_it_wont_override_data(self):
        with self.assertRaises(FlakeAttributeOverwriting):
            FlakeFactory.build_flake(self.with_attrs, {'from_class': 5})
