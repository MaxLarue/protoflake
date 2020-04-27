import unittest
from unittest.mock import Mock

from protoflake.discoveryservice import DiscoveryService
from protoflake.descriptorbuilder import DescriptorBuilder


class TestDiscoveryService(unittest.TestCase):

    def setUp(self) -> None:
        self.file_discoverer = Mock()
        self.file_discoverer_class = Mock()
        self.file_discoverer_class.return_value = self.file_discoverer
        self.list_discoverer = Mock()
        self.list_discoverer_class = Mock()
        self.list_discoverer_class.return_value = self.list_discoverer
        self.service = DiscoveryService(
            self.file_discoverer_class,
            self.list_discoverer_class,
        )
        self.descriptor_builder = DescriptorBuilder()

    def test_it_is_possible_to_discover_flakes_from_files(self):
        self.file_discoverer.discover.return_value = [
            self.descriptor_builder.build_flake_descriptor({'proto': 'test.class', 'id': 'first'}),
            self.descriptor_builder.build_flake_descriptor({'proto': 'test.class', 'id': 'second'}),
        ]
        self.service.from_files(['/some/file.json'])
        self.assertEqual(2, len(self.service.definitions.values()))
        self.assertEqual('first', self.service.get_definition('first').id)
        self.assertEqual('second', self.service.get_definition('second').id)

    def test_it_is_possible_to_discover_flakes_from_code_input(self):
        self.list_discoverer.discover.return_value = [
            self.descriptor_builder.build_flake_descriptor({'proto': 'test.class', 'id': 'first'}),
            self.descriptor_builder.build_flake_descriptor({'proto': 'test.class', 'id': 'second'}),
        ]
        self.service.from_list([
            {'proto': 'test.class', 'id': 'first'},
            {'proto': 'test.class', 'id': 'second'},
        ])
        self.assertEqual(2, len(self.service.definitions.values()))
        self.assertEqual('first', self.service.get_definition('first').id)
        self.assertEqual('second', self.service.get_definition('second').id)
