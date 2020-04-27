import unittest
from unittest.mock import Mock

from flakeregistry import FlakeRegistry
from flakeregistry import FlakeAlreadyExist


class TestFlakeRegistry(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.registry = FlakeRegistry()
        self.fake_flake_id = 'some flake'
        self.fake_flake = Mock()
        self.registry.set(self.fake_flake_id, self.fake_flake)

    def test_it_has_by_id(self):
        self.assertTrue(self.registry.has(self.fake_flake_id))

    def test_it_gets_by_id(self):
        self.assertEqual(self.fake_flake, self.registry.get(self.fake_flake_id))

    def test_multi_id(self):
        self.registry.set('another id', Mock())
        self.assertNotEqual(self.fake_flake, self.registry.get('another id'))

    def test_overwriting_raise_flake_already_exist(self):
        with self.assertRaises(FlakeAlreadyExist):
            self.registry.set(self.fake_flake_id, Mock())
