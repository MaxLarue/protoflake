import unittest
from unittest.mock import Mock

from flakeservice import FlakeService


class TestFlakeService(unittest.TestCase):

    def setUp(self) -> None:
        self.discovery_service = Mock()
        self.discovery_service.get_definition.return_value = 'new'
        self.builder = Mock()
        self.service = FlakeService(self.discovery_service, self.builder)

    def test_it_is_possible_to_create_a_simple_flake(self):
        flake_mock = Mock()
        self.builder.has.return_value = False
        self.builder.get_new.return_value = flake_mock
        flake = self.service.get('test_flake')
        self.assertEqual(flake_mock, flake)

    def test_it_uses_the_definition_from_discovery_to_build_the_flake(self):
        definition_mock = Mock()
        self.builder.has.return_value = False
        self.discovery_service.get_definition.return_value = definition_mock
        flake = self.service.get('some id')
        self.builder.get_new.assert_called_with(definition_mock)

    def test_it_returns_the_already_existing_flake_if_builder_already_created_it(self):
        flake = Mock()
        self.builder.has.return_value = True
        self.builder.get_ref.return_value = flake
        from_service = self.service.get('some id')
        self.assertEqual(flake, from_service)
