import unittest
from unittest.mock import Mock

from protoflake.filediscoverer import FileDiscoverer


class TestFileDiscoverer(unittest.TestCase):

    def setUp(self) -> None:
        self.parser_factory = Mock()

    def test_it_uses_parser_factory_to_find_parser(self):
        fake_flake = Mock()
        parser = Mock()
        parser.from_file.return_value = [fake_flake]
        self.parser_factory.get_parser.return_value = parser
        discoverer = FileDiscoverer(self.parser_factory, [
            'some_file.json',
            'some_file.yaml',
            'some_file.yml',
            'some_file.xml',
        ])
        flakes = discoverer.discover()
        self.assertEqual(4, len(flakes))
        self.assertEqual([fake_flake, fake_flake, fake_flake, fake_flake], flakes)
