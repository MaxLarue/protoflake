import unittest

from protoflake.descriptors import FileSourceDescriptor
from protoflake.parserfactory import NoSuitableParserFound
from protoflake.parserfactory import ParserFactory
from protoflake.parsers import JsonFlakeParser
from protoflake.parsers import XmlFlakeParser
from protoflake.parsers import YamlFlakeParser


class TestParserFactory(unittest.TestCase):

    def test_it_raises_for_unknown_extension(self):
        with self.assertRaises(NoSuitableParserFound):
            ParserFactory.get_parser(FileSourceDescriptor('/some/file.whatever'))

    def test_it_return_right_parser_for_yaml(self):
        self.assertIsInstance(
            ParserFactory.get_parser(FileSourceDescriptor('./some/file.yml')),
            YamlFlakeParser
        )

    def test_it_return_right_parser_for_yaml_variation(self):
        self.assertIsInstance(
            ParserFactory.get_parser(FileSourceDescriptor('./some/file.yaml')),
            YamlFlakeParser
        )

    def test_it_return_right_parser_for_json(self):
        self.assertIsInstance(
            ParserFactory.get_parser(FileSourceDescriptor('./some/file.json')),
            JsonFlakeParser
        )

    def test_it_return_right_parser_for_xml(self):
        self.assertIsInstance(
            ParserFactory.get_parser(FileSourceDescriptor('./some/file.xml')),
            XmlFlakeParser
        )
